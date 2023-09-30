import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import RobotCreationForm
from .models import Robot


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
                robot.save()
                return JsonResponse({'message': 'Robot created successfully'}, status=201)
            else:
                return JsonResponse({'errors': form.errors}, status=400)

        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
