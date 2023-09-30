import openpyxl
from django.http import HttpResponse
from django.utils import timezone
from .models import Robot
from collections import defaultdict

def generate_excel_report(request):
    try:
        # Получаем текущую дату и время
        current_date = timezone.now()

        # Определяем начало и конец периода для последней недели
        end_date = current_date
        start_date = current_date - timezone.timedelta(days=7)

        # Получаем данные из базы данных за последнюю неделю
        robot_data = Robot.objects.filter(created__range=(start_date, end_date))

        # Проверяем, есть ли данные о роботах за последнюю неделю
        if not robot_data.exists():
            return HttpResponse("No data about robots", content_type="text/plain")

        # Создаем новый Excel-файл
        wb = openpyxl.Workbook()

        # Используем defaultdict для группировки данных по модели и версии
        data_by_model_version = defaultdict(int)

        for robot in robot_data:
            model_version = f"{robot.model} - {robot.version}"
            data_by_model_version[model_version] += 1

        # Создаем лист Excel для каждой модели с детализацией по версии
        for model_version, count in data_by_model_version.items():
            model, version = model_version.split(" - ")
            ws = wb.create_sheet(title=f"{model} - {version}")

            # Создаем заголовок для листа
            ws.append(["Модель", "Версия", "Количество за неделю"])
            ws.append([model, version, count])

        # Удаляем стандартный лист, который создается по умолчанию
        del wb['Sheet']

        # Сохраняем Excel-файл в HttpResponse
        response = HttpResponse(content_type="application/ms-excel")
        response['Content-Disposition'] = f'attachment; filename="robot_summary_report.xlsx"'
        wb.save(response)

        return response

    except Exception as e:
        return HttpResponse(f"Произошла ошибка: {str(e)}", content_type="text/plain")
