"""HTML email templates for BOM assistant notifications.

Provides a shared base layout and content builders for
BOM and escalation emails.
"""

from __future__ import annotations

from datetime import datetime, timezone

from src.agents.tools.schemas import EscalationCategory, GenerateBomOutput


def _render_email_shell(
    *,
    header_title: str,
    header_subtitle: str,
    header_bg: str,
    content_html: str,
    footer_note: str,
    max_width: int = 700,
) -> str:
    """Wrap email content in the shared HTML shell (header + body + footer)."""
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background-color: #f1f5f9; -webkit-font-smoothing: antialiased;">

<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color: #f1f5f9; padding: 2rem 1rem;">
<tr><td align="center">
<table role="presentation" width="{max_width}" cellpadding="0" cellspacing="0" style="max-width: {max_width}px; width: 100%; background: #ffffff; border-radius: 1rem; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.07), 0 2px 4px -2px rgba(0,0,0,0.05);">

    <!-- Header -->
    <tr>
        <td style="background: {header_bg}; padding: 2rem 2rem 1.5rem;">
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
                <tr>
                    <td>
                        <div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; color: rgba(255,255,255,0.7); margin-bottom: 0.5rem;">Starlinks BOM Assistant</div>
                        <h1 style="margin: 0; font-size: 1.5rem; font-weight: 700; color: #ffffff; letter-spacing: -0.025em;">{header_title}</h1>
                        <p style="margin: 0.5rem 0 0; font-size: 0.875rem; color: rgba(255,255,255,0.85);">{header_subtitle}</p>
                    </td>
                </tr>
            </table>
        </td>
    </tr>

    <!-- Body -->
    <tr>
        <td style="padding: 2rem;">
            {content_html}
        </td>
    </tr>

    <!-- Footer -->
    <tr>
        <td style="background: #f8fafc; padding: 1.25rem 2rem; border-top: 1px solid #e2e8f0;">
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
                <tr>
                    <td style="font-size: 0.75rem; color: #94a3b8; line-height: 1.5;">
                        Email này được gửi tự động từ <strong style="color: #64748b;">Starlinks BOM Assistant</strong>.<br>
                        {footer_note}
                    </td>
                </tr>
            </table>
        </td>
    </tr>

</table>
</td></tr>
</table>

</body>
</html>"""


def build_bom_email_body(bom: GenerateBomOutput) -> str:
    """Build an HTML email body for a BOM notification."""
    timestamp = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")

    customer_html = f"""
            <div style="margin-bottom: 1.5rem;">
                <div style="font-size: 0.6875rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #94a3b8; margin-bottom: 0.5rem;">Khách hàng</div>
                <div style="font-size: 0.9375rem; color: #1e293b; font-weight: 500;">{bom.customer_name}</div>
                <div style="font-size: 0.8125rem; color: #64748b; margin-top: 0.25rem;">SĐT: {bom.customer_phone}</div>
            </div>"""

    rows_html = ""
    for item in bom.line_items:
        price = f"${item.unit_price_usd:.2f}" if item.unit_price_usd else "\u2014"
        rows_html += f"""
                <tr>
                    <td style="padding: 0.625rem 0.75rem; border-bottom: 1px solid #e2e8f0; text-align: center; font-size: 0.8125rem; color: #64748b;">{item.line}</td>
                    <td style="padding: 0.625rem 0.75rem; border-bottom: 1px solid #e2e8f0; font-size: 0.8125rem; font-weight: 600; color: #1e293b; font-family: 'SF Mono', SFMono-Regular, Menlo, Consolas, monospace;">{item.sku}</td>
                    <td style="padding: 0.625rem 0.75rem; border-bottom: 1px solid #e2e8f0; font-size: 0.8125rem; color: #334155;">{item.description}</td>
                    <td style="padding: 0.625rem 0.75rem; border-bottom: 1px solid #e2e8f0; font-size: 0.8125rem; color: #334155;">{item.vendor_compatibility}</td>
                    <td style="padding: 0.625rem 0.75rem; border-bottom: 1px solid #e2e8f0; text-align: center; font-size: 0.8125rem; font-weight: 600; color: #1e293b;">{item.quantity}</td>
                    <td style="padding: 0.625rem 0.75rem; border-bottom: 1px solid #e2e8f0; text-align: right; font-size: 0.8125rem; color: #334155;">{price}</td>
                </tr>"""

    assumptions_html = ""
    if bom.assumptions:
        items_html = "".join(
            f'<li style="margin-bottom: 0.25rem; font-size: 0.8125rem; color: #334155;">{a}</li>'
            for a in bom.assumptions
        )
        assumptions_html = f"""
            <div style="margin-bottom: 1.5rem;">
                <div style="font-size: 0.6875rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #94a3b8; margin-bottom: 0.5rem;">Giả định</div>
                <ul style="margin: 0; padding-left: 1.25rem; line-height: 1.6;">{items_html}</ul>
            </div>"""

    summary_html = f"""
            <div style="margin-bottom: 1.5rem; background: #f8fafc; border-left: 4px solid #2563eb; border-radius: 0 0.5rem 0.5rem 0; padding: 1rem 1.25rem;">
                <div style="font-size: 0.6875rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #94a3b8; margin-bottom: 0.5rem;">Tóm tắt</div>
                <div style="font-size: 0.875rem; line-height: 1.6; color: #334155;">{bom.summary}</div>
            </div>"""

    content_html = f"""
            <!-- Success Banner -->
            <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 0.5rem; padding: 0.75rem 1rem; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.125rem;">&#9989;</span>
                <span style="color: #16a34a; font-weight: 600; font-size: 0.875rem;">BOM đã được tạo thành công</span>
            </div>

            {customer_html}

            <!-- Line Items Table -->
            <div style="margin-bottom: 1.5rem;">
                <div style="font-size: 0.6875rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #94a3b8; margin-bottom: 0.75rem;">Chi tiết BOM</div>
                <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border: 1px solid #e2e8f0; border-radius: 0.75rem; overflow: hidden;">
                    <tr style="background: #f8fafc;">
                        <th style="padding: 0.625rem 0.75rem; font-size: 0.6875rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; text-align: center; border-bottom: 2px solid #e2e8f0;">#</th>
                        <th style="padding: 0.625rem 0.75rem; font-size: 0.6875rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; text-align: left; border-bottom: 2px solid #e2e8f0;">SKU</th>
                        <th style="padding: 0.625rem 0.75rem; font-size: 0.6875rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; text-align: left; border-bottom: 2px solid #e2e8f0;">Mô tả</th>
                        <th style="padding: 0.625rem 0.75rem; font-size: 0.6875rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; text-align: left; border-bottom: 2px solid #e2e8f0;">Vendor</th>
                        <th style="padding: 0.625rem 0.75rem; font-size: 0.6875rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; text-align: center; border-bottom: 2px solid #e2e8f0;">SL</th>
                        <th style="padding: 0.625rem 0.75rem; font-size: 0.6875rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; text-align: right; border-bottom: 2px solid #e2e8f0;">Đơn giá</th>
                    </tr>
                    {rows_html}
                </table>
            </div>

            {assumptions_html}
            {summary_html}

            <!-- Attachment Note -->
            <div style="background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 0.5rem; padding: 1rem 1.25rem; margin-bottom: 0.5rem;">
                <div style="display: flex; align-items: flex-start; gap: 0.5rem;">
                    <span style="font-size: 1.125rem;">&#128206;</span>
                    <div>
                        <div style="font-weight: 600; font-size: 0.875rem; color: #1e40af; margin-bottom: 0.25rem;">File Excel đính kèm</div>
                        <div style="font-size: 0.8125rem; color: #3b82f6; line-height: 1.5;">File BOM chi tiết đã được đính kèm trong email này. Nếu có thắc mắc hoặc muốn tiến hành đặt hàng, vui lòng phản hồi email.</div>
                    </div>
                </div>
            </div>"""

    return _render_email_shell(
        header_title="Danh sách vật tư (BOM)",
        header_subtitle=bom.customer_name,
        header_bg="linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%)",
        content_html=content_html,
        footer_note=timestamp,
    )


def build_escalation_email(
    *,
    reason: str,
    category: EscalationCategory,
    conversation_summary: str,
    user_email: str | None,
    session_id: str,
) -> tuple[str, str]:
    """Build the escalation email subject and HTML body."""
    timestamp = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")

    category_labels = {
        EscalationCategory.OFF_TOPIC: "Yêu cầu ngoài phạm vi",
        EscalationCategory.TOO_COMPLEX: "Vấn đề phức tạp",
        EscalationCategory.CUSTOMER_COMPLAINT: "Khiếu nại từ khách hàng",
        EscalationCategory.PRICING_REQUEST: "Yêu cầu báo giá",
        EscalationCategory.URGENT_TECHNICAL: "Sự cố kỹ thuật khẩn cấp",
        EscalationCategory.OTHER: "Khác",
    }
    category_colors = {
        EscalationCategory.OFF_TOPIC: ("#f0fdf4", "#16a34a", "#bbf7d0"),
        EscalationCategory.TOO_COMPLEX: ("#fefce8", "#ca8a04", "#fef08a"),
        EscalationCategory.CUSTOMER_COMPLAINT: ("#fef2f2", "#dc2626", "#fecaca"),
        EscalationCategory.PRICING_REQUEST: ("#eff6ff", "#2563eb", "#bfdbfe"),
        EscalationCategory.URGENT_TECHNICAL: ("#fef2f2", "#dc2626", "#fecaca"),
        EscalationCategory.OTHER: ("#f8fafc", "#64748b", "#e2e8f0"),
    }
    category_label = category_labels.get(category, category.value)
    badge_bg, badge_color, badge_border = category_colors.get(
        category, ("#f8fafc", "#64748b", "#e2e8f0")
    )

    is_urgent = category in (
        EscalationCategory.CUSTOMER_COMPLAINT,
        EscalationCategory.URGENT_TECHNICAL,
    )
    header_bg = "#dc2626" if is_urgent else "#1e3a5f"

    urgent_banner = ""
    if is_urgent:
        urgent_banner = """
            <div style="background: #fef2f2; border: 1px solid #fecaca; border-radius: 0.5rem; padding: 0.75rem 1rem; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.25rem;">&#9888;&#65039;</span>
                <span style="color: #dc2626; font-weight: 600; font-size: 0.875rem;">Cần xử lý gấp — Vui lòng phản hồi trong thời gian sớm nhất</span>
            </div>"""

    subject = f"[Chuyển tiếp] {category_label} — Starlinks BOM Assistant"

    content_html = f"""
            {urgent_banner}

            <!-- Category & Reason Cards -->
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 1.5rem;">
                <tr>
                    <td style="padding-bottom: 1rem;">
                        <div style="font-size: 0.6875rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #94a3b8; margin-bottom: 0.5rem;">Phân loại</div>
                        <span style="display: inline-block; padding: 0.375rem 1rem; border-radius: 2rem; font-size: 0.875rem; font-weight: 600; background: {badge_bg}; color: {badge_color}; border: 1px solid {badge_border};">{category_label}</span>
                    </td>
                </tr>
                <tr>
                    <td>
                        <div style="font-size: 0.6875rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #94a3b8; margin-bottom: 0.5rem;">Lý do chuyển tiếp</div>
                        <div style="font-size: 0.9375rem; line-height: 1.6; color: #1e293b; background: #f8fafc; border-radius: 0.5rem; padding: 1rem; border: 1px solid #e2e8f0;">{reason}</div>
                    </td>
                </tr>
            </table>

            <!-- Info Grid -->
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 1.5rem; border: 1px solid #e2e8f0; border-radius: 0.75rem; overflow: hidden;">
                <tr>
                    <td width="50%" style="padding: 1rem 1.25rem; border-bottom: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; vertical-align: top;">
                        <div style="font-size: 0.6875rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #94a3b8; margin-bottom: 0.25rem;">Email khách hàng</div>
                        <div style="font-size: 0.875rem; color: #1e293b; font-weight: 500;">{user_email or "Không có thông tin"}</div>
                    </td>
                    <td width="50%" style="padding: 1rem 1.25rem; border-bottom: 1px solid #e2e8f0; vertical-align: top;">
                        <div style="font-size: 0.6875rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #94a3b8; margin-bottom: 0.25rem;">Mã phiên</div>
                        <div style="font-size: 0.8125rem; color: #64748b; font-family: 'SF Mono', SFMono-Regular, Menlo, Consolas, monospace;">{session_id}</div>
                    </td>
                </tr>
            </table>

            <!-- Conversation Summary -->
            <div style="margin-bottom: 0.5rem;">
                <div style="font-size: 0.6875rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #94a3b8; margin-bottom: 0.75rem;">Tóm tắt cuộc hội thoại</div>
                <div style="background: #f8fafc; border-left: 4px solid #2563eb; border-radius: 0 0.5rem 0.5rem 0; padding: 1.25rem; font-size: 0.9375rem; line-height: 1.7; color: #334155; white-space: pre-wrap;">{conversation_summary}</div>
            </div>"""

    body = _render_email_shell(
        header_title="Yêu cầu chuyển tiếp hỗ trợ",
        header_subtitle=timestamp,
        header_bg=header_bg,
        content_html=content_html,
        footer_note="Vui lòng liên hệ khách hàng để hỗ trợ tiếp.",
        max_width=600,
    )

    return subject, body
