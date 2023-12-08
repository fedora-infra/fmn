# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from unittest.mock import MagicMock

from aiosmtplib import SMTP, SMTPServerDisconnected

from fmn.sender.email import EmailHandler


async def test_email_connect(mocker):
    smtp = MagicMock(spec=SMTP)
    smtp_class = mocker.patch("fmn.sender.email.SMTP", return_value=smtp)
    handler = EmailHandler({"smtp_host": "smtp.example.com", "smtp_port": 487})

    await handler.setup()

    smtp_class.assert_called_once_with(hostname="smtp.example.com", port=487)
    smtp.connect.assert_called_once_with()

    await handler.stop()

    smtp.quit.assert_called_once_with()


async def test_email_handle():
    smtp = MagicMock(spec=SMTP)
    handler = EmailHandler({"from": "FMN <fmn@example.com>"})
    handler._smtp = smtp

    await handler.handle(
        {"headers": {"To": "dest@example.com", "Subject": "Testing"}, "body": "This is a test"}
    )

    smtp.send_message.assert_called_once()

    sent = smtp.send_message.call_args[0][0]
    assert sent["To"] == "dest@example.com"
    assert sent["Subject"] == "Testing"
    assert sent.get_body().get_content() == "This is a test\n"
    assert sent.get_content_type() == "text/plain"


async def test_email_disconnected():
    smtp = MagicMock(spec=SMTP)
    handler = EmailHandler({"from": "FMN <fmn@example.com>"})
    handler._smtp = smtp
    smtp.send_message.side_effect = [SMTPServerDisconnected("Nope!"), lambda m: None]

    await handler.handle(
        {"headers": {"To": "dest@example.com", "Subject": "Testing"}, "body": "This is a test"}
    )

    assert smtp.send_message.call_count == 2
    smtp.connect.assert_called_once_with()


async def test_email_handle_with_footer():
    smtp = MagicMock(spec=SMTP)
    handler = EmailHandler({"from": "FMN <fmn@example.com>"})
    handler._smtp = smtp

    await handler.handle(
        {
            "headers": {"To": "dest@example.com", "Subject": "Testing"},
            "body": "This is a test",
            "footer": "This is a footer.",
        }
    )

    smtp.send_message.assert_called_once()

    sent = smtp.send_message.call_args[0][0]
    assert sent["To"] == "dest@example.com"
    assert sent["Subject"] == "Testing"
    assert sent.get_body().get_content() == "This is a test\n\n-- \nThis is a footer.\n"
    assert sent.get_content_type() == "text/plain"
