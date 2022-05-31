import json

from django.views       import View
from django.http        import JsonResponse

from reviews.models     import Review, Comment
from users.models       import User
from utils              import login_decorator

class CommentView(View):
    @login_decorator
    def post(self, request, review_id):
        try:
            data = json.loads(request.body)
            
            user         = request.user
            review       = Review.objects.get(id=review_id)
            name         = data["name"]
            content      = data["content"]
            password     = data["password"]

            Comment.objects.create(
                user     = user,
                review   = review,
                name     = name,
                content  = content,
                password = password
            )

            return JsonResponse({"message" : "SUCCESS"}, status=200)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)