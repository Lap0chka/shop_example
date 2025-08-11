import logging

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)

User = get_user_model()

def validate_email_available(value: str) -> None:
    """
    Validate that the provided email address is not already associated with an existing user.
    """
    logger.debug("Validating email availability for: %s", value)
    if User.objects.filter(email__iexact=value).exists():
        logger.warning("Email '%s' is already in use.", value)
        raise ValidationError("Email is already in use.")


def validate_password_change(user: User, current_password: str, new_password1: str,
                             new_password2: str) -> None:
    """
    Validate a password change request by checking password match, presence of
    current password, and correctness of the current password.
    """
    logger.debug("Validating password change for user: %s", )

    if new_password1 or new_password2:
        if new_password1 != new_password2:
            logger.error("New passwords do not match for user: %s", user)
            raise ValidationError("New passwords do not match.")

        if not current_password:
            logger.error("Current password not provided for user: %s", user)
            raise ValidationError("Current password is required to change password.")

        if not user.check_password(current_password):
            logger.error("Incorrect current password for user: %s", user)
            raise ValidationError("Current password is incorrect.")
