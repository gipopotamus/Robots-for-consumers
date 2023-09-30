from django.urls import path
from . import views

urlpatterns = [
    # Добавляем URL-маршрут для создания робота
    path('create_robot/', views.create_robot, name='create_robot'),
]
