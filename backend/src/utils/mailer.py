"""SMTP mailer.

Sending mail must never break the request that triggered it, so every failure
here is logged and swallowed. The caller gets back a simple (sent, error)
tuple and decides what to do.
"""

import logging
import os
import smtplib
import ssl
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USER)

FRONTEND_URI = os.getenv("FRONTEND_URI", "http://localhost:3000")


def smtp_configured() -> bool:
    return bool(SMTP_HOST and SMTP_USER and SMTP_PASSWORD and FROM_EMAIL)


def send_email(to: str, subject: str, body: str) -> tuple[bool, str]:
    """Send a plain text email. Returns (sent, error_message)."""
    if not smtp_configured():
        return False, "SMTP is not configured"

    if not to:
        return False, "No recipient email"

    message = EmailMessage()
    message["From"] = FROM_EMAIL
    message["To"] = to
    message["Subject"] = subject
    message.set_content(body)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20) as server:
            server.ehlo()
            server.starttls(context=ssl.create_default_context())
            server.ehlo()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(message)
        return True, ""
    except Exception as exc:
        logger.warning("SMTP send failed to %s: %s", to, exc)
        return False, str(exc)


def send_password_setup_email(to: str, username: str, role: str, token: str) -> tuple[bool, str]:
    """Email a new user the link where they choose their own password."""
    link = f"{FRONTEND_URI.rstrip('/')}/set-password?token={token}"

    subject = "Your AstraVidya account is ready"
    body = f"""Hello {username},

An account has been created for you on the AstraVidya portal.

  Role      : {role}
  Username  : {username}

Please choose your password using the link below. It is valid for 2 hours.

  {link}

After setting your password you can sign in at:
  {FRONTEND_URI.rstrip('/')}/login

If you were not expecting this email you can safely ignore it.

--
AstraVidya Institute of Technology
"""

    return send_email(to, subject, body)


def send_password_reset_email(to: str, username: str, token: str) -> tuple[bool, str]:
    subject = "Reset your AstraVidya password"
    link = f"{FRONTEND_URI.rstrip('/')}/set-password?token={token}"

    body = f"""Hello {username},

We received a request to reset the password for your AstraVidya account.

Choose a new password here (valid for 2 hours):

  {link}

If you did not ask for this, you can ignore this email - your password has not
been changed.

--
AstraVidya Institute of Technology
"""

    return send_email(to, subject, body)