from unittest import mock

import pytest

from authx import EmailClient


@pytest.mark.asyncio
@mock.patch("aiosmtplib.send", mock.AsyncMock(return_value=None))
async def test_email_client():
    email_client = EmailClient(None, None, None, None, "", "", "")
    await email_client.send_confirmation_email("", "")
    await email_client.send_forgot_password_email("", "")
