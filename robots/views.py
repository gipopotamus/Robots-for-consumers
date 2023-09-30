import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from orders.signals import order_created, send_notification_to_customer
from .forms import RobotCreationForm
from .models import Robot
from orders.models import Order
from django.db import transaction

@csrf_exempt
def create_robot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = RobotCreationForm(data)

            if form.is_valid():
                model = form.cleaned_data['model']
                version = form.cleaned_data['version']
                serial = f"{model}{version}"
                robot = form.save(commit=False)
                robot.serial = serial

                # Попробуйте создать робот внутри транзакции
                with transaction.atomic():
                    robot.save()
                    # Проверьте наличие заказов на этот робот и пометьте их как выполненные
                    waiting_orders = Order.objects.filter(robot_serial=robot.serial, is_fulfilled=False)
                    for order in waiting_orders:
                        order.fulfill_order()  # Помечаем заказ как выполненный
                        send_notification_to_customer(order.customer, robot)

                return JsonResponse({'message': 'Robot created successfully'}, status=201)
            else:
                return JsonResponse({'errors': form.errors}, status=400)

        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
