from django.http        import JsonResponse

import jwt

from my_settings        import SECRET_KEY, ALGORITHM
from .models            import User

def jwt_expression(func):
    def get_token(self, request, *args, **kwargs):
        try:
            # print(request.__dir__())
            access_token = request.headers.get('Authorization')
            payload      = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)
            user         = User.objects.get(id=payload['id']).id
            request.user = user
            return  func(self, request, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return JsonResponse({"message": "EXPIRED_TOKEN"}, status = 400)

        except User.DoesNotExist:
            return JsonResponse({"message" : "INVALID_ID"}, status=400)

    return get_token