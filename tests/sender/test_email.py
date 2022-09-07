from unittest.mock import MagicMock

from aiosmtplib import SMTP

from fmn.sender.email import EmailHandler


async def test_email_connect(mocker):
    smtp = MagicMock(spec=SMTP)
    smtp_class = mocker.patch("fmn.sender.email.SMTP", return_value=smtp)
    handler = EmailHandler({"smtp_host": "smtp.example.com", "smtp_port": 487})

    await handler.setup()

    smtp_class.assert_called_once_with("smtp.example.com", 487)
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
