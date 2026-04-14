"""Async email service using SMTP.

Provides a simple interface for sending emails with optional file attachments.
"""

import ssl
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from pathlib import Path

import aiosmtplib
from loguru import logger

from src.configs import SETTINGS


async def send_email(
    to_email: str,
    subject: str,
    body: str,
    is_html: bool = False,
    attachment_path: Path | None = None,
) -> None:
    """Send an email via SMTP.

    Args:
        to_email: Recipient email address.
        subject: Email subject line.
        body: Email body (plain text or HTML).
        is_html: Whether the body is HTML.
        attachment_path: Optional file to attach.

    Raises:
        ValueError: If SMTP is not configured.
        aiosmtplib.errors.SMTPException: On SMTP errors.
    """
    if not SETTINGS.smtp.server or not SETTINGS.smtp.username:
        raise ValueError("SMTP is not configured. Set SMTP__SERVER and SMTP__USERNAME in .env")

    msg = MIMEMultipart()
    msg["From"] = SETTINGS.smtp.username
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html" if is_html else "plain"))

    if attachment_path and attachment_path.exists():
        with open(attachment_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            "attachment",
            filename=attachment_path.name,
        )
        msg.attach(part)

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with aiosmtplib.SMTP(
        hostname=SETTINGS.smtp.server,
        port=SETTINGS.smtp.port,
        tls_context=ssl_context,
        start_tls=True,
    ) as server:
        await server.login(SETTINGS.smtp.username, SETTINGS.smtp.password)
        await server.send_message(msg)

    logger.info(f"Email sent to {to_email}: {subject}")
