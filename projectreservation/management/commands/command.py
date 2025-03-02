from reservations.models import Seat  # 'reservations'는 실제 앱 이름으로 변경

lockers = ['Locker1', 'Locker2', 'Locker3', 'Locker4']
for locker in lockers:
    for row in range(1, 4):  # 9행 (1부터 9까지)
        for col in range(1, 10):  # 3열 (1부터 3까지)
            seat_id = f"{locker}-R{row}C{col}"
            Seat.objects.get_or_create(
                seat=seat_id,
                defaults={'status': 'available', 'name': None, 'studentid': None}
            )

print("Successfully created seats")  # 성공 메시지 출력