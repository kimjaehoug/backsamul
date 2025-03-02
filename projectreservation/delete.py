from reservations.models import Seat  # 'your_app'은 모델이 정의된 앱 이름으로 변경
Seat.objects.all().delete()