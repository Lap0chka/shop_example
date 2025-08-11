import logging
from typing import Optional

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction
from django_email_verification import send_email

logger = logging.getLogger(__name__)
User = get_user_model()


def update_user_email(user: User, new_email: Optional[str]) -> User:
    """
    Update user's email and deactivate the account until confirmation.
    This function expects that email validation (format and availability) has been
    performed beforehand.
    """
    if not new_email:
        return user

    if user.email == new_email:
        logger.warning(
            f"Attempted to set the same email for user_id={user.id}",
        )
        raise ValidationError("New email and current email are the same.")

    logger.info("Updating email for user id=%s to %s and deactivating until confirmation.",)

    with transaction.atomic():
        user.email = new_email
        user.is_active = False
        user.save(update_fields=["email", "is_active"])
        transaction.on_commit(lambda: send_email(user))

    return user


def change_user_password(user: User, new_password: Optional[str]) -> User:
    """
    Change user's password if a non-empty password is provided and it differs from the current one.
    """
    if not new_password:
        return user

    if user.check_password(new_password):
        logger.warning("New password matches current password for user id=%s.",
                       getattr(user, "id", None))
        raise ValidationError("New password must be different from the current password.")

    logger.info("Changing password for user id=%s.", getattr(user, "id", None))
    user.set_password(new_password)
    user.save(update_fields=["password"])
    return user
