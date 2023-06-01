from django.utils.translation import gettext_lazy as _


class CustomMessages:
    INVALID_CREDENTIALS_ERROR = _("Incorrect email or password")
    INACTIVE_ACCOUNT_ERROR = _("This account is disabled")
    INVALID_TOKEN_ERROR = _("Invalid token")
    INVALID_UID_ERROR = _("User does not exist")
    STALE_TOKEN_ERROR = _("Stale token")
    PASSWORD_MISMATCH_ERROR = _("The password fields do not match")
    USERNAME_MISMATCH_ERROR = _("The {0} fields do not match")
    INVALID_PASSWORD_ERROR = _("Incorrect password")
    EMAIL_NOT_FOUND = _("User with this email does not exist")
    CANNOT_CREATE_USER_ERROR = _("Unable to create account")
