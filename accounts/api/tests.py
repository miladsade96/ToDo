import pytest
from mail_templated import EmailMessage
from .utilities import EmailThread


@pytest.fixture()
def email_message():
    email_obj = EmailMessage(
        template_name="email/activation_email.tpl",
        context={"token": "token"},
        from_email="from@admin.com",
        to=["to@user.com"],
    )
    return email_obj
