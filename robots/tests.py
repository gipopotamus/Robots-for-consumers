import json
from django.test import TestCase, Client
from django.utils import timezone
from .models import Robot


class RobotAPITest(TestCase):
    def setUp(self):
        self.client = Client()

        self.robot_data = {
            "model": "R2",
            "version": "D2",
            "created": timezone.now(),
            "serial": "R2-D2"
        }
        self.robot = Robot.objects.create(**self.robot_data)

    def test_create_robot(self):
        data = {
            "model": "R2",
            "version": "D2",
            "created": "2022-12-31 23:59:59"
        }

        response = self.client.post('/create_robot/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)  # Ожидаем успешный статус создания

        # Проверяем, что робот был создан в базе данных
        robot = Robot.objects.get(serial="R2D2")
        self.assertEqual(robot.model, "R2")
        self.assertEqual(robot.version, "D2")

    def test_create_robot_invalid_data(self):
        data = {
            "model": "InvalidModel",
            "version": "X",
            "created": "2023-01-01 00:00:00"
        }

        response = self.client.post('/create_robot/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)  # Ожидаем статус ошибки валидации

    def test_create_robot_missing_data(self):
        data = {}  # Недостающие данные

        response = self.client.post('/create_robot/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)  # Ожидаем статус ошибки валидации

    def test_create_robot_invalid_json(self):
        invalid_json = "Invalid JSON"  # Некорректный JSON

        response = self.client.post('/create_robot/', invalid_json, content_type='application/json')
        self.assertEqual(response.status_code, 400)  # Ожидаем статус ошибки разбора JSON
