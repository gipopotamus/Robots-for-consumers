from django.db.models.signals import Signal
from django.dispatch import receiver
from .models import Order
from robots.models import Robot
from customers.models import Customer

order_created = Signal()


@receiver(order_created)
def send_notification_when_robot_available(sender, order, **kwargs):
    # Попробуйте получить робота с указанным серийным номером
    try:
        robot = Robot.objects.get(serial=order.robot_serial)
    except Robot.DoesNotExist:
        # Робота нет, не отправляем уведомление
        return

    # Робот доступен, отправьте уведомление заказчику
    send_notification_to_customer(order.customer, robot)


def send_notification_to_customer(customer, robot):
    # Текст уведомления
    message = f"Добрый день!\n"
    message += f"Недавно вы оставили заказ на робота модели {robot.model}, версии {robot.version}.\n"
    message += f"Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами."

    from django.core.mail import send_mail

    subject = "Робот доступен в наличии"
    message = message
    from_email = "your@email.com"  # Замените на вашу электронную почту
    recipient_list = [customer.email]

    send_mail(subject, message, from_email, recipient_list)
