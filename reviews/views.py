import json
import datetime

from django.views       import View
from django.http        import JsonResponse
from django.db.models   import Q

from reviews.models     import Review
from utils              import login_decorator
from django.shortcuts   import redirect

class ReviewView(View):
    @login_decorator
    def delete(self, request, review_id):
        try:
            review = Review.objects.get(id=review_id)
            review.delete()

            return redirect('/reviews')
            
        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)