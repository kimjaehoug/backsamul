# serializers.py
from rest_framework import serializers
from .models import User, Seat

# reservations/serializers.py
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['name', 'studentid', 'password']

    def validate_student_id(self, value):
        print("Validating studentid:", value)  # 디버깅 로그 추가
        if not value or not value.strip():
            raise serializers.ValidationError("학번은 필수 입력 항목입니다.")
        if not value.isdigit():
            raise serializers.ValidationError("학번은 숫자만 입력해야 합니다.")
        return value

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("이름은 비워둘 수 없습니다.")
        return value

# reservations/serializers.py
# reservations/serializers.py
# reservations/serializers.py
# reservations/serializers.py
# reservations/serializers.py
class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['seat', 'status', 'name', 'studentid', 'created_at']  # name 필드 추가
        extra_kwargs = {
            'seat': {'required': True, 'read_only': False, 'validators': []},  # unique 검증 비활성화
            'status': {'read_only': True},  # 상태는 읽기 전용
            'name': {'required': False, 'allow_null': True},  # 이름은 선택적, 예약 시만 설정
            'studentid': {'required': False, 'allow_null': True},  # 학번은 선택적, 예약 시만 설정
            'created_at': {'read_only': True},
        }

    def to_internal_value(self, data):
        print("To internal value data:", data)  # 데이터 파싱 전 로그
        # seat, name, studentid 값을 강제로 포함시켜 validated_data에 추가
        if 'seat' in data:
            data['seat'] = str(data['seat']).strip()
        if 'name' in data:
            data['name'] = str(data['name']).strip()
        if 'studentid' in data:
            data['studentid'] = str(data['studentid']).strip()
        return super().to_internal_value(data)

    def validate_seat(self, value):
        print("Validating seat:", value, type(value))
        if not value or not value.strip():
            raise serializers.ValidationError("좌석은 필수 입력 항목입니다.")
        if not isinstance(value, str):
            raise serializers.ValidationError("좌석은 문자열이어야 합니다.")
        if not Seat.objects.filter(seat=value).exists():
            raise serializers.ValidationError("존재하지 않는 좌석입니다.")
        return value