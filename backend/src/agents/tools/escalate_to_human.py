"""Escalation tool for the BOM assistant agent.

Sends an email notification to the support team when the agent
cannot handle the user's request.
"""

from langchain_core.tools import tool
from loguru import logger

from src.agents.tools.utils.email_templates import build_escalation_email
from src.agents.tools.schemas import EscalateInput, EscalationCategory
from src.configs import SETTINGS
from src.services.email_service import send_email


@tool(args_schema=EscalateInput)
async def escalate_to_human(
    reason: str,
    category: EscalationCategory,
    conversation_summary: str,
) -> str:
    """Escalate the conversation to a human support agent via email.

    Use this tool when you cannot adequately help the customer. Escalation cases include:
    - The request is outside your scope (not about optical transceivers or BOM generation)
    - The customer needs specific pricing or discount information
    - The customer has a complaint or is unhappy with the service
    - The technical question is too complex or requires hands-on support
    - The customer explicitly asks to speak with a human

    Args:
        reason: Brief explanation of why the conversation is being escalated.
        category: The escalation category.
        conversation_summary: Summary of the conversation including what the customer needs.

    Returns:
        Confirmation message that the escalation was sent.
    """
    if not SETTINGS.escalation_email:
        return (
            "Chức năng chuyển tiếp chưa được cấu hình. "
            "Vui lòng liên hệ trực tiếp đội ngũ kinh doanh Starlinks qua kênh hỗ trợ thông thường."
        )

    try:
        # Access context from the tool's runtime config
        config = escalate_to_human.config if hasattr(escalate_to_human, "config") else {}
        context = config.get("configurable", {}).get("context", None)
        user_email = getattr(context, "user_email", None) if context else None
        session_id = getattr(context, "session_id", "unknown") if context else "unknown"

        subject, body = build_escalation_email(
            reason=reason,
            category=category,
            conversation_summary=conversation_summary,
            user_email=user_email,
            session_id=session_id,
        )

        await send_email(
            to_email=SETTINGS.escalation_email,
            subject=subject,
            body=body,
            is_html=True,
        )

        logger.info(f"Escalation sent: category={category.value}, session={session_id}")
        return (
            f"Đã gửi email chuyển tiếp thành công đến đội hỗ trợ.\n"
            f"- **Phân loại:** {category.value}\n"
            f"- **Lý do:** {reason}\n\n"
            f"Đội ngũ hỗ trợ sẽ liên hệ lại trong thời gian sớm nhất."
        )

    except Exception as e:
        logger.exception(f"Failed to send escalation email: {e}")
        return (
            f"Không thể gửi email chuyển tiếp: {e}. "
            f"Vui lòng liên hệ trực tiếp đội ngũ kinh doanh Starlinks."
        )
