from pydantic import BaseModel


class NhanhTokenStatusResponse(BaseModel):
    connected: bool
    business_id: str | None = None
    expired_at: int | None = None
    message: str


class NhanhInventoryRequest(BaseModel):
    product_ids: list[int] | None = None
    category_ids: list[int] | None = None
    depot_ids: list[int] | None = None
    page: int = 1
    page_size: int = 50


class NhanhDepotInventory(BaseModel):
    depot_id: int
    remain: int = 0
    available: int = 0


class NhanhInventoryItem(BaseModel):
    product_id: int
    remain: int = 0
    shipping: int = 0
    damaged: int = 0
    holding: int = 0
    available: int = 0
    warranty: int = 0
    depots: list[NhanhDepotInventory] = []


class NhanhInventoryResponse(BaseModel):
    items: list[NhanhInventoryItem]
    total_pages: int = 0
    current_page: int = 1


# --- Product search ---


class NhanhProductSearchRequest(BaseModel):
    ids: list[int] | None = None
    name: str | None = None
    barcode: str | None = None
    category_id: int | None = None
    brand_id: int | None = None
    price_from: float | None = None
    price_to: float | None = None
    status: int | None = None
    parent_id: int | None = None
    imei: str | None = None
    page: int = 1
    page_size: int = 50
    sort_by: str | None = None  # id, price, name, inventory
    sort_order: str = "desc"  # asc, desc


class NhanhProductItem(BaseModel):
    id: int
    parent_id: int | None = None
    name: str = ""
    code: str = ""
    barcode: str = ""
    price: float = 0
    import_price: float = 0
    category_id: int | None = None
    brand_id: int | None = None
    status: int = 0
    remain: int = 0
    available: int = 0
    image: str = ""


class NhanhProductListResponse(BaseModel):
    items: list[NhanhProductItem]
    next_cursor_id: int | None = None


# --- Product detail ---


class NhanhProductDetailRequest(BaseModel):
    product_ids: list[int]


# --- Product category ---


class NhanhCategorySearchRequest(BaseModel):
    ids: list[int] | None = None
    name: str | None = None
    code: str | None = None
    status: int | None = None  # 1 = Active, 2 = Inactive
    page_size: int = 50


class NhanhCategoryItem(BaseModel):
    id: int
    parent_id: int | None = None
    code: str = ""
    name: str = ""
    order: int = 0
    image: str = ""
    content: str = ""
    status: int = 0


class NhanhCategoryListResponse(BaseModel):
    items: list[NhanhCategoryItem]
    next_cursor: dict | None = None


class NhanhSyncResponse(BaseModel):
    sync_type: str  # "full" or "incremental"
    total_created: int
    total_updated: int
    total_pages_fetched: int
    total_matched: int = 0
    total_unmatched: int = 0
    message: str = "Sync completed successfully"


# --- Datasheet matching ---


class DatasheetMatchResultItem(BaseModel):
    nhanh_id: int
    product_name: str
    datasheet_path: str | None
    match_layer: str  # "code_exact" | "llm" | "unmatched"
    confidence: str = "high"


class DatasheetMatchResponse(BaseModel):
    total_products: int
    total_matched: int
    total_unmatched: int
    results: list[DatasheetMatchResultItem]


class DatasheetMatchStatusResponse(BaseModel):
    total_products: int
    matched: int
    unmatched: int
    match_rate: float  # 0.0 - 1.0
