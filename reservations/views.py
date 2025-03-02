# views.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Seat
from .serializers import UserSerializer, SeatSerializer
import bcrypt  # 비밀번호 해시화 라이브러리 (설치 필요: pip install bcrypt)


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        studentid = serializer.validated_data['studentid']
        if User.objects.filter(studentid=studentid).exists():
            return Response({'error': '이미 존재하는 학번입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 비밀번호 해시화
        password = serializer.validated_data['password'].encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        # 사용자 생성
        user = User(
            name=serializer.validated_data['name'],
            studentid=studentid,
            password=hashed_password.decode('utf-8')
        )
        user.save()
        return Response({'message': '가입 성공'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# reservations/views.py
# reservations/views.py
@api_view(['POST'])
def login(request):
    try:
        print("Received login data:", request.data)  # 요청 데이터 로그
        # 로그인에서는 중복 체크가 필요하지 않으므로, Serializer를 사용하지 않고 직접 데이터 처리
        if not request.data.get('studentid') or not request.data.get('name') or not request.data.get('password'):
            return Response({'error': '학번, 이름, 비밀번호는 필수 입력 항목입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        studentid = request.data.get('studentid')
        name = request.data.get('name')
        password = request.data.get('password').encode('utf-8')

        print("Validating user with student_id:", studentid, "name:", name)  # 유효성 검사 로그
        try:
            user = User.objects.get(studentid=studentid, name=name)
            print("Found user:", user)  # 사용자 찾음 로그
            if bcrypt.checkpw(password, user.password.encode('utf-8')):
                print("Password match successful")  # 비밀번호 일치 로그
                return Response({
                    'message': '로그인 성공',
                    'name': user.name,
                    'studentid': user.studentid
                }, status=status.HTTP_200_OK)
            else:
                print("Password mismatch")  # 비밀번호 불일치 로그
                return Response({'error': '비밀번호가 잘못되었습니다.'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            print("User not found")  # 사용자 없음 로그
            return Response({'error': '사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print("Error in login:", str(e))
        return Response({'error': '서버 오류가 발생했습니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# reservations/views.py
# reservations/views.py
@api_view(['POST'])
def reserve_seat(request):
    try:
        print("Received reserve data:", request.data)
        print("Received reserve data type:", type(request.data))
        print("Received reserve data keys:", list(request.data.keys()))

        # 데이터에서 필수 키 확인
        if 'seat' not in request.data or 'name' not in request.data or 'studentid' not in request.data:
            return Response({'error': '좌석(seat), 이름(name), 학번(student_id)는 필수 입력 항목입니다.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = SeatSerializer(data=request.data, partial=True)
        print("Serializer valid?", serializer.is_valid())
        print("Serializer initial data:", serializer.initial_data)
        if serializer.is_valid():
            seat = serializer.validated_data.get('seat', None)
            print("Validated data:", serializer.validated_data)
            if not seat:
                return Response({'error': '좌석 정보가 유효하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

            print("Validated seat:", seat, type(seat))
            # 요청 데이터에서 student_id 가져오기
            studentid = request.data.get('studentid')
            if not studentid or not studentid.strip():
                return Response({'error': '학번은 필수 입력 항목입니다.'}, status=status.HTTP_400_BAD_REQUEST)

            # 동일한 student_id로 이미 예약된 사물함이 있는지 확인
            if Seat.objects.filter(studentid=studentid, status='reserved').exists():
                return Response({'error': '이미 예약된 사물함이 있습니다. 한 사람당 하나의 사물함만 예약 가능합니다.'},
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                existing_seat = Seat.objects.get(seat=seat)
                print("Found seat:", existing_seat)
                if existing_seat.status == 'reserved':
                    return Response({"error": "이미 예약된 좌석입니다."}, status=status.HTTP_400_BAD_REQUEST)

                # 기존 좌석 상태 업데이트
                existing_seat.status = 'reserved'
                existing_seat.name = request.data.get('name')
                existing_seat.studentid = studentid
                existing_seat.save()
                print("Reservation successful for seat:", seat)
                return Response({"message": "예약 성공"}, status=status.HTTP_200_OK)
            except Seat.DoesNotExist:
                print("Seat not found:", seat)
                return Response({"error": "좌석을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        print("Serializer errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print("Error in reserve_seat:", str(type(e)), str(e), request.data)
        return Response({'error': f'서버 오류가 발생했습니다: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# reservations/views.py
@api_view(['POST'])
def cancel_seat(request):
    try:
        print("Received cancel data:", request.data)
        print("Received cancel data type:", type(request.data))
        print("Received cancel data keys:", list(request.data.keys()))

        # 데이터에서 필수 키 확인 (studentid, password, name)
        if 'studentid' not in request.data or 'password' not in request.data or 'name' not in request.data:
            return Response({'error': '학번(studentid), 비밀번호(password), 이름(name)은 필수 입력 항목입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        studentid = request.data.get('studentid')
        password = request.data.get('password').encode('utf-8')
        name = request.data.get('name')

        if not studentid or not password or not name or not studentid.strip() or not name.strip():
            return Response({'error': '학번, 비밀번호, 이름은 필수 입력 항목이며 비워둘 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # User 모델에서 해당 studentid와 name으로 사용자 조회
            user = User.objects.get(studentid=studentid, name=name)
            print("Found user for cancellation:", user)

            # 비밀번호 검증
            if not bcrypt.checkpw(password, user.password.encode('utf-8')):
                print("Password mismatch for cancellation")
                return Response({'error': '비밀번호가 잘못되었습니다.'}, status=status.HTTP_401_UNAUTHORIZED)

            # 해당 studentid로 예약된 모든 reserved 상태의 사물함 찾기
            reserved_seats = Seat.objects.filter(studentid=studentid, status='reserved')
            if not reserved_seats.exists():
                print("No reserved seats found for studentid:", studentid)
                return Response({"error": "예약된 좌석을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

            # 모든 예약된 사물함 상태 초기화 (취소)
            for seat in reserved_seats:
                print("Canceling seat:", seat)
                seat.status = 'available'
                seat.name = None
                seat.studentid = None
                seat.save()

            print("All reservations canceled for studentid:", studentid)
            return Response({"message": "모든 예약 취소 성공"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            print("User not found for cancellation:", studentid, name)
            return Response({"error": "사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("Error querying user or seats:", str(e))
            return Response({"error": "서버 오류가 발생했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        print("Error in cancel_seat:", str(type(e)), str(e), request.data)
        return Response({'error': f'서버 오류가 발생했습니다: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# reservations/views.py
@api_view(['GET'])
def get_seats(request):
    seats = Seat.objects.all()
    serializer = SeatSerializer(seats, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)