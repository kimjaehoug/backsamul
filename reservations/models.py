# models.py
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    studentid = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)  # 비밀번호 (해시화 필요)

    def __str__(self):
        return f"{self.name} - {self.studentid}"

class Seat(models.Model):
    seat = models.CharField(max_length=20, unique=True)  # 예: "Locker1-R1C1"
    status = models.CharField(max_length=20, default='available')  # 상태: available, reserved
    name = models.CharField(max_length=100, blank=True, null=True)  # 예약자 이름
    studentid = models.CharField(max_length=20, blank=True, null=True)  # 예약자 학번
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.seat} - {self.status}"