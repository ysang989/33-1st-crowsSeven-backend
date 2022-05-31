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

            return JsonResponse({"message" : "SUCCESS"}, status=200)

        except review.DoesNotExist:
            return JsonResponse({"message" : "REVIEW_NOT_EXISTED"})

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

        
class WholeReviewView(View):
    def get(self, request):
        try:
            limit         = int(request.GET.get('limit', 5))
            offset        = int(request.GET.get('offset',0))

            reviews = Review.objects.order_by("-created_at")[offset:offset+limit]

            review_list =[{
                "review_id"        : review.id,
                "review_product"   : review.product.name[0]+"***",
                "review_title"     : review.title,
                "review_thumb_nail": review.product.thumbnail_image_url,
                "review_name"      : review.user.username,
                "review_date"      : review.updated_at,
                "review_view_count": review.view_count
            } for review in reviews]

            return JsonResponse({"message" : review_list}, status=200)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)