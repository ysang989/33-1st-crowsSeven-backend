import json,re,bcrypt,jwt

from django.views import View
from django.http  import JsonResponse
from django.conf  import settings

from .models import User

class SignupView(View):
    def post(self, request):
        try:
            input_data = json.loads(request.body)

            username           = input_data["username"]
            password           = input_data["password"]
            name               = input_data["name"]
            address            = input_data["address"]
            email              = input_data["email"]
            birth_date         = input_data["birth_date"]
            phone_number       = input_data["phone_number"]
            optional_agreement = input_data["optional_agreement"]

            REGEX_USERNAME    = '[a-z0-9]{4,16}$'
            REGEX_EMAIL       = '[a-zA-Z0-9_-]+@[a-z]+.[a-z]+$'
            REGEX_PASSWORD    = '^(?!((?:[A-Za-z]+)|(?:[~!@#$%^&*()_+=]+)|(?=[0-9]+))$)[A-Za-z\d~!@#$%^&*()_+=]{8,16}$'
            REGEX_PHONENUMBER = '\d{10,11}'
            REGEX_BIRTHDATE   = '^(19[0-9][0-9]|20\d{2})(0[0-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])$'

            if not re.match(REGEX_USERNAME, username):
                return JsonResponse({"message":"아이디 형식에 영문소문자/숫자, 4~16자가 포함되어야합니다."}, status=400)

            if not re.match(REGEX_EMAIL, email):
                return JsonResponse({"maessage":"이메일 형식에 @와 .이 포함되어있지않습니다."}, status=400)
 
            if not re.match(REGEX_PASSWORD, password):
                return JsonResponse({"message":"비밀번호 형식에 영문 대소문자/숫자/특수문자 중 2가지 이상 조합, 8자~16자 포함되어야합니다."}, status=400)

            if not re.match(REGEX_PHONENUMBER, phone_number):
                return JsonResponse({"message":"휴대전화 형식에 숫자 10~11자리만 포함되어야합니다."}, status=400)

            if not re.match(REGEX_BIRTHDATE, birth_date):
                return JsonResponse({"message":"생년월일 형식에 8자리만 포함되어야합니다."}, status=400)
            
            if User.objects.filter(username=username).exists():
                return JsonResponse({"message":"이미 회원가입된 이메일입니다."}, status=400)
            
            hashed_password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode("UTF-8")

            User.objects.create(
                username           = username,
                password           = hashed_password,
                name               = name,
                address            = address,
                email              = email,
                birth_date         = birth_date,
                phone_number       = phone_number,
                optional_agreement = optional_agreement
            )
            return JsonResponse({"message" : "SUCCESS"}, status=201)
        
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

