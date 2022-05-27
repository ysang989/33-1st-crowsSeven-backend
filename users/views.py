import json, re 

import bcrypt, jwt
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
            REGEX_PASSWORD    = '^[A-Za-z0-9]{4,16}$'
            REGEX_PHONENUMBER = '\d{10,11}'
            REGEX_BIRTHDATE   = '^(19[0-9][0-9]|20\d{2})(0[0-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])$'

            if not re.match(REGEX_USERNAME, username):
                return JsonResponse({"message":"INVALID_USERNAME"}, status=400)

            if not re.match(REGEX_EMAIL, email):
                return JsonResponse({"maessage":"INVALID_EMAIL"}, status=400)
 
            if not re.match(REGEX_PASSWORD, password):
                return JsonResponse({"message":"INVALID_PASSWORD"}, status=400)

            if not re.match(REGEX_PHONENUMBER, phone_number):
                return JsonResponse({"message":"INVALID_PHONENUMBER"}, status=400)

            if not re.match(REGEX_BIRTHDATE, birth_date):
                return JsonResponse({"message":"INVALID_BIRTHDATE"}, status=400)
            
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

class LoginView(View):
    def post(self,request):
        try:
            input_data = json.loads(request.body)

            username = input_data["username"]
            password = input_data["password"]


            user = User.objects.get(username=username)
            if not bcrypt.checkpw(password.encode("UTF-8"), user.password.encode("UTF-8")):
                return JsonResponse({"messange": "INVALID_PASSWORD"}, status=401)

            access_token = jwt.encode({"id" : user.id}, settings.SECRET_KEY, settings.ALGORITHM)
            return JsonResponse({"access_token": access_token}, status=200) 

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"},status=401)