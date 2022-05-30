import json
import datetime

from django.views       import View
from django.http        import JsonResponse
from django.db.models   import Q
from django.shortcuts   import redirect

from reviews.models     import Review, Comment
from products.models    import Product
from orders.models      import Order, OrderItem
from products.models    import OptionProduct, Product
from users.models       import User
from utils              import login_decorator

class ReviewSearchView(View):
    def get(self, request):
        try:
            search_keyword = request.GET.get('q', None)
            search_time_keyword = request.GET.get('time', None)
            search_type = request.GET.get('type', None)

            q = Q()

            if search_time_keyword == '5분':
                q=Q(created_at__lt = datetime.datetime.now() - datetime.timedelta(minutes=5))
            if search_time_keyword == '10분':
                q=Q(created_at__lt = datetime.datetime.now() - datetime.timedelta(minutes=10))
            if search_time_keyword == '15분':
                q=Q(created_at__lt = datetime.datetime.now() - datetime.timedelta(minutes=15))
            if search_time_keyword == '20분':
                q=Q(created_at__lt = datetime.datetime.now() - datetime.timedelta(minutes=20))

            if search_type == '제목':
                q &= Q(title__icontains = search_keyword )
            if search_type == '내용':
                q &= Q(context__icontains= search_keyword )
            if search_type == '글쓴이':
                q &= Q(user__id__icontains = search_keyword )
            if search_type == '아이디':
                q &= Q(id__icontains = search_keyword )
            if search_type == '상품정보':
                q &= Q(product__name__icontains = search_keyword)

            searched_reviews = Review.objects.filter(q).distinct()

            review_list =[{
                "review_id"        : review.id,
                "review_product"   : review.product.name,
                "review_title"     : review.title,
                "review_thumb_nail": review.product.thumbnail_image_url,
                "review_name"      : review.user.username,
                "review_date"      : review.updated_at,
                "review_view_count": review.view_count
            } for review in searched_reviews]

            return JsonResponse({"message" : review_list}, status=200)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)