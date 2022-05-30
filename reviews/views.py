import json

from django.views       import View
from django.http        import JsonResponse
from django.db.models   import Q

from reviews.models     import Review

class ReviewSearchView(View):
    def get(self, request):
        try:
            search_keyword = request.GET.get('q', None)
            search_time_keyword = request.GET.get('time', None)
            search_type = request.GET.get('type', None)

            q = Q()

            if search_time_keyword == '일주일':
                q &= Q(created_at__gte = datetime.datetime.now() - datetime.timedelta(days=7))
            if search_time_keyword == '한달':
                q &= Q(created_at__gte = datetime.datetime.now() - datetime.timedelta(months=1))
            if search_time_keyword == '세달':
                q &= Q(created_at__gte = datetime.datetime.now() - datetime.timedelta(months=3))
            if search_time_keyword == '전체':
                q &= Review.objects.all()

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