from django.core.mail import send_mail
from django.conf import settings

def send_order_confirmation_email(user_email, order):
    subject = f"Order #{order.id} Confirmation"
    message = f"""
    Hi {order.user.username},

    Your order has been successfully placed! 🎉

    Order ID: {order.id}
    Total Price: ${order.total_price}
    Status: {order.status}

    Thank you for shopping with us!

    - The E-Commerce Team
    """
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])

def send_payment_receipt_email(user_email, payment):
    subject = f"Payment Receipt for Order #{payment.order.id}"
    message = f"""
    Hi {payment.user.username},

    We have received your payment for Order #{payment.order.id}.

    Amount Paid: ${payment.amount}
    Payment Method: {payment.payment_method}
    Transaction ID: {payment.transaction_id}
    Status: {payment.status}

    Thank you for your purchase! 🎉

    - The E-Commerce Team
    """
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
