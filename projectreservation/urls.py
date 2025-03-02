# urls.py
from django.urls import path
from reservations import views

urlpatterns = [
    path('api/register/', views.register, name='register'),
    path('api/login/', views.login, name='login'),
    path('api/reserve/', views.reserve_seat, name='reserve_seat'),
    path('api/seats/', views.get_seats, name='get_seats'),
    path('api/cancel/', views.cancel_seat, name='cancel_seat'),  # 예약 취소 엔드포인트 추가
]