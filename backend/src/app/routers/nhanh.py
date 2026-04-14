from urllib.parse import urlencode

from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from loguru import logger

from src.app.auth import get_current_user
from src.app.dependencies import get_nhanh_product_repository, get_nhanh_service
from src.app.schemas.nhanh import (
    DatasheetMatchResponse,
    DatasheetMatchResultItem,
    DatasheetMatchStatusResponse,
    NhanhProductListResponse,
    NhanhProductSearchRequest,
    NhanhSyncResponse,
    NhanhTokenStatusResponse,
)
from src.configs import SETTINGS
from src.db.models.users import User
from src.db.repositories.nhanh import NhanhProductRepository
from src.services.nhanh.client import NhanhApiError
from src.services.nhanh.service import NhanhService

router = APIRouter(prefix="/nhanh", tags=["nhanh"])


@router.get("/authorize")
async def authorize():
    """Redirect user to Nhanh.vn OAuth authorization page."""
    if not SETTINGS.nhanh.app_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Nhanh app_id is not configured",
        )

    params = urlencode({
        "version": "2.0",
        "appId": SETTINGS.nhanh.app_id,
        "returnLink": SETTINGS.nhanh.redirect_url,
    })
    return RedirectResponse(url=f"https://nhanh.vn/oauth?{params}")


@router.get("/callback")
async def oauth_callback(
    accessCode: str | None = None,
    error: str | None = None,
    svc: NhanhService = Depends(get_nhanh_service),
):
    """OAuth callback — exchanges access code for token and persists it."""
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"OAuth authorization failed: {error}",
        )
    if not accessCode:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing accessCode parameter",
        )

    try:
        token = await svc.exchange_and_save_token(accessCode)
    except NhanhApiError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to exchange Nhanh access code: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to exchange access code with Nhanh.vn",
        )

    return {
        "message": "Connected to Nhanh.vn successfully",
        "business_id": token.business_id,
        "expired_at": token.expired_at,
    }


@router.get("/token/status", response_model=NhanhTokenStatusResponse)
async def token_status(svc: NhanhService = Depends(get_nhanh_service)):
    """Check if we have a valid Nhanh.vn token."""
    return await svc.get_token_status()


@router.post("/products", response_model=NhanhProductListResponse)
async def search_products(
    body: NhanhProductSearchRequest | None = None,
    svc: NhanhService = Depends(get_nhanh_service),
):
    """Search / list products from Nhanh.vn."""
    try:
        return await svc.search_products(body)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except NhanhApiError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e))


@router.post("/products/sync", response_model=NhanhSyncResponse)
async def sync_products(
    force_full: bool = False,
    current_user: User = Depends(get_current_user),
    svc: NhanhService = Depends(get_nhanh_service),
    product_repo: NhanhProductRepository = Depends(get_nhanh_product_repository),
):
    """Sync products from Nhanh.vn to local database.

    By default, performs incremental sync (only products updated since last sync).
    Pass force_full=true to re-fetch all products.

    Note: updatedAt only covers product info changes (name, price, etc.),
    NOT inventory. Register webhooks for inventory updates.
    """
    try:
        result = await svc.sync_all_products(product_repo, force_full=force_full)
        return NhanhSyncResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except NhanhApiError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e))


@router.post("/webhook")
async def webhook(
    request: Request,
    authorization: str | None = Header(None),
):
    """
    Receive webhook events from Nhanh.vn.
    Events: webhooksEnabled, appUninstalled, productAdd, productUpdate,
    productDelete, inventoryChange, orderAdd, orderUpdate, orderDelete.
    """
    expected_token = SETTINGS.nhanh.webhooks_verify_token
    if expected_token and authorization != expected_token:
        logger.warning("Nhanh webhook rejected: invalid verify token")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid verify token")

    body = await request.json()
    event = body.get("event")
    business_id = body.get("businessId")

    logger.info(f"Nhanh webhook received: event={event}, businessId={business_id}")

    match event:
        case "webhooksEnabled":
            logger.info("Nhanh webhook verification successful")
        case "productAdd":
            logger.info(f"Nhanh: product added for business {business_id}")
        case "productUpdate":
            logger.info(f"Nhanh: product updated for business {business_id}")
        case "productDelete":
            logger.info(f"Nhanh: product deleted for business {business_id}")
        case "inventoryChange":
            logger.info(f"Nhanh: inventory changed for business {business_id}")
        case "orderAdd":
            logger.info(f"Nhanh: order added for business {business_id}")
        case "orderUpdate":
            logger.info(f"Nhanh: order updated for business {business_id}")
        case "orderDelete":
            logger.info(f"Nhanh: order deleted for business {business_id}")
        case "appUninstalled":
            logger.warning(f"Nhanh: app uninstalled by business {business_id}")
        case _:
            logger.warning(f"Nhanh webhook: unknown event '{event}'")

    return JSONResponse(status_code=200, content={"success": True})


@router.post("/products/match-datasheets", response_model=DatasheetMatchResponse)
async def match_datasheets(
    rematch_all: bool = False,
    current_user: User = Depends(get_current_user),
    svc: NhanhService = Depends(get_nhanh_service),
    product_repo: NhanhProductRepository = Depends(get_nhanh_product_repository),
):
    """Match Nhanh products to datasheet files.

    By default, only matches products that don't have a datasheet_path yet.
    Pass rematch_all=true to re-run matching on all products.
    """
    results = await svc.match_datasheets(product_repo, rematch_all=rematch_all)
    await product_repo.session.commit()

    matched = sum(1 for r in results if r.datasheet_path)
    return DatasheetMatchResponse(
        total_products=len(results),
        total_matched=matched,
        total_unmatched=len(results) - matched,
        results=[
            DatasheetMatchResultItem(
                nhanh_id=r.nhanh_id,
                product_name=r.product_name,
                datasheet_path=r.datasheet_path,
                match_layer=r.match_layer,
                confidence=r.confidence,
            )
            for r in results
        ],
    )


@router.get("/products/match-status", response_model=DatasheetMatchStatusResponse)
async def match_status(
    current_user: User = Depends(get_current_user),
    product_repo: NhanhProductRepository = Depends(get_nhanh_product_repository),
):
    """Get the current datasheet matching status (matched vs unmatched counts)."""
    stats = await product_repo.get_match_status()
    return DatasheetMatchStatusResponse(**stats)
