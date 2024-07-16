from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from payment.models import Order, ShippingAddress


@shared_task()
def send_order_confirmation(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Order {order.id} payment Confirmation'
    receipt_data = ShippingAddress.objects.get(user=order.user)
    receipt_email = receipt_data.email
    message = f'Your order and payment has been confirmed. Your order number is {order.id}.'

    mail_to_sender = send_mail(
        subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=[receipt_email],
    )
    return mail_to_sender
