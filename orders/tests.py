from django.test import TestCase
from django.urls import reverse
from django.http import JsonResponse
from django.utils import timezone

from robots.models import Robot
from orders.models import Order
from customers.models import Customer
from django.core import mail


class OrderTestCase(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(email='test@example.com')
        self.robot_data = {
            'serial': 'R2D2',
            'model': 'R2',
            'version': 'D2',
            'created': timezone.now()
        }

    def test_create_robot_after_manual_order(self):
        # Создаем ордер вручную для робота, которого еще нет в наличии
        non_existing_robot_serial = 'R2D2'
        order = Order.objects.create(customer=self.customer, robot_serial=non_existing_robot_serial)

        # Создаем робота, симулируя его появление в наличии
        response = self.client.post(reverse('create_robot'), data=self.robot_data, content_type='application/json')
        self.assertEqual(response.status_code, 201)

        # Проверяем, что уведомление было отправлено
        self.assertEqual(len(mail.outbox), 1)
        sent_mail = mail.outbox[0]
        self.assertEqual(sent_mail.subject, "Робот доступен в наличии")
        self.assertIn("Этот робот теперь в наличии. Если вам подходит этот вариант", sent_mail.body)
