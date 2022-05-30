import json

from django.views       import View
from django.http        import JsonResponse

from reviews.models     import Review
from utils              import login_decorator


class ReviewView(View):
    @login_decorator
    def patch(self, request, review_id):
        try:
            data    = json.loads(request.body)
            title   = data["title"]
            context = data["context"]
            review  = Review.objects.filter(id=review_id)
            review.update(title = title, context=context)
            
            return JsonResponse({"message" : "SUCCESS"}, status=201)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
