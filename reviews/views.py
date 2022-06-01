import json
import datetime

from django.views       import View
from django.http        import JsonResponse
from django.db.models   import Q

from reviews.models     import Review

class ReviewSearchView(View):
    def get(self, request):
        try:
            day                 = request.GET.get('days')
            search_type         = request.GET.get('type', None)
            search_type_keyword = request.GET.get('q', None)

            search_keyword = Q()

            days = {
                "일주일" : 7,
                "한달"  : 30,
                "세달"  : 90,
            }

            if day in days:
                search_keyword &= Q(created_at__gte = datetime.datetime.now() - datetime.timedelta(days=int(days[day])))
            
            search_dict = {
                "title"  : "title__icontains",
                "content": "context__icontains",
                "author" : "user__name__icontains",
                "id"     : "user__id__icontains",
                "product": "product__name__icontains",
            }

            search_filter    = {search_dict[search_type] : search_type_keyword} if search_type_keyword and search_type else {}

            searched_reviews = Review.objects.filter(search_keyword, **search_filter).distinct()

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

class ReviewDetailView(View):
    def get(self, request, review_id):
        try:
            results = []
            review  = Review.objects.get(id=review_id)
            comments=[{
                    'comment_id'        : comment.id,
                    'comment_writer'    : comment.user.name[0]+"***",
                    'comment_created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'content'           : comment.content
                } for comment in Comment.objects.filter(review_id=review.id)]

            product = [{
                'product_name'           : review.product.name,
                'product_price'          : review.product.price,
                'product_thumbnail_image': review.product.thumbnail_image_url,
                'new_product'            : review.product.the_newest,
            }]

            related_reviews      = Review.objects.filter(~Q(id=review_id) & Q(product_id = review.product))
            related_review=[{
                'review_id'        : have_relation_review.id,
                'review_product'   : have_relation_review.product.name,
                'review_title'     : have_relation_review.title,
                'review_writer'    : have_relation_review.user.name[0]+"***",
                'review_created_at': have_relation_review.created_at.strftime('%Y-%m-%d'),
                'review_view_point': have_relation_review.view_count
            } for have_relation_review in related_reviews]

            if Review.objects.filter(id = review_id).exists():
                review.view_count = review.view_count+1
                review.save()

            results.append({
                'detail_review_id': review.id,
                'title'           : review.title,
                'review_writer'   : review.user.name[0]+"***",
                'title_created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'view_count'      : review.view_count,
                'comment'         : comments,
                'product'         : product,
                'related_review'  : related_review
            })
            return JsonResponse({"message" : results}, status=200)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

class ReviewView(View):
    @login_decorator
    def patch(self, request, review_id):
        try:
            data           = json.loads(request.body)
            title          = data["title"]
            context        = data["context"]
            review         = Review.objects.get(id = review_id)
            review.title   = title
            review.context = context

            review.save()
    
            return JsonResponse({"message" : "SUCCESS"}, status=201)

        except Review.DoesNotExist:
            return JsonResponse({"message" : "REVIEW_NOT_EXISTED"})

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

    @login_decorator
    def post(self, request, product_id):
        try:
            data       = json.loads(request.body)
            title      = data["title"]
            context    = data["context"]
            password   = data["password"]

            if Review.objects.filter(product_id=product_id , user_id = request.user).exists():
                return JsonResponse({'message':'REVIEW_ALREADY_EXIST'}, status=404)
            
            Review.objects.create(
                user       = request.user,
                title      = title,
                context    = context,
                password   = password,
                view_count = 0,
                product    = Product.objects.get(id=product_id),
            )

            return JsonResponse({"message" : "SUCCESS"}, status=201)
        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

class ReviewView(View):
    @login_decorator
    def delete(self, request, review_id):
        try:
            review = Review.objects.get(id=review_id)
            review.delete()

            return JsonResponse({"message" : "SUCCESS"}, status=200)

        except Review.DoesNotExist:
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
