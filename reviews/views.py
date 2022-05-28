import json
import datetime

from django.views       import View
from django.http        import JsonResponse
from django.db.models   import Q

from reviews.models     import Review, Comment
from orders.models      import Order, OrderItem
from products.models    import OptionProduct, Product
from users.models       import User
from users.utils        import jwt_expression


class ReviewView(View):
    @jwt_expression
    def get(self, request):
        try:
            total_option_product      = []
            total_option_product_id   = []
            total_option_product_name = []
            h=[]
            c=[]
            total_option=[]
            total_order=Order.objects.filter(user_id=request.user).select_related('user').prefetch_related('orderitem_set')
            
            for total_option_product in total_order:
                total_option.append(list(total_option_product.orderitem_set.values('option_product_id')
            ))

            answer=sum(total_option,[])

            a=list(map(dict,set(tuple(sorted(d.items())) for d in answer)))
      
            [h.append(a[i]['option_product_id']) for i in range(len(a))]
          
            [c.append(OptionProduct.objects.get(id=j).product.name) for j in h]
            
            return JsonResponse({"message" : list(set(c))}, status=200)
        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

    @jwt_expression
    def post(self, request):
        try:
            data = json.loads(request.body)

            user     = User.objects.get(id=request.user)
            title    = data["title"]
            context  = data["context"]
            password = data["password"]
            password = data["product"]
            product  = Product.objects.get(name = product).id
            
            if Review.objects.filter(product_id=product).exists():
                return JsonResponse({'message':'REVIEW_ALREADY_EXIST'}, status=404)

            Review.objects.create(
                    user       = user,
                    title      = title,
                    context    = context,
                    password   = password,
                    view_count = 0,
                    product    = product
                    )

            return JsonResponse({"message" : "SUCCESS"}, status=200)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

    @jwt_expression
    def delete(self, request, review_id):
        review = Review.objects.get(id=review_id)
        review.delete()
        return redirect('/reviews')

    @jwt_expression
    def path(self, request, review_id):
        review         = Review.objects.get(id=review_id)
        review.title   = request.POST.get('title')
        review.context = request.POST.get('context')
        review.save

class ReviewDetailView(View):
    def get(self, request, review_id):
            try:
                results = []
                review  = Review.objects.get(id=review_id)
                
                comments = []
                
                for comment in Comment.objects.select_related('review').filter(review_id=review.id):
                    comments.append({
                        'comment_writer'    : comment.user.name,
                        'comment_created_at': comment.created_at,
                        'content'           : comment.content
                    })
                                    
                if Review.objects.filter(id=review_id).exists():
                    review.view_count = review.view_count+1
                    review.save()
                
                product = []
                product.append({
                    'product_name'           : review.product.name,
                    'product_price'          : review.product.price,
                    'product_thumbnail_image': review.product.thumbnail_image_url
                })

                results.append({
                    'title'           : review.title,
                    'review_writer'   : review.user.name, 
                    'title_created_at': review.created_at,
                    'view_count'      : review.view_count,
                    'comment'         : comments,
                    'product'         : product
                })

                return JsonResponse({"message" : results}, status=200)

            except KeyError :
                return JsonResponse({"message" : "KEY_ERROR"}, status=400)

class WholeReviewView(View):
    def get(self, request):
        try:

            review_list = Review.objects.order_by("-created_at")

            review_list =[{
                "review_id"        : review.id,
                "review_product"   : review.product.name,
                "review_title"     : review.title,
                "review_thumb_nail": review.product.thumbnail_image_url,
                "review_name"      : review.user.username,
                "review_date"      : review.updated_at,
                "review_view_count": review.view_count
            } for review in reviews]

            return JsonResponse({"message" : review_list}, status=200)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

class ReviewSearchView(View): 
    def get(self, request):
        try:
            search_keyword = request.GET.get('q', None)
            search_time_keyword = request.GET.get('time', None)
            search_type = request.GET.get('type', None)

            reviews = Review.objects.order_by("-created_at")

            if search_time_keyword == '5분':
                q &= Q(created_at__lt = datetime.datetime.now() - datetime.timedelta(minutes=5))

            if search_time_keyword == '10분':
                q &= Q(created_at__lt = datetime.datetime.now() - datetime.timedelta(minutes=10))

            if search_time_keyword == '15분':
                q &= Q(created_at__lt = datetime.datetime.now() - datetime.timedelta(minutes=15))

            if search_time_keyword == '20분':
                q &= Q(created_at__lt = datetime.datetime.now() - datetime.timedelta(minutes=20))
            
            if search_time_keyword == '제목':
                q &= Q(title__icontains = search_keyword )
            
            if search_time_keyword == '내용':
                q &= Q(context__icontains= search_keyword )
            
            if search_time_keyword == '글쓴이':
                q &= Q(user_id__user__icontains = search_keyword )
            
            if search_time_keyword == '아이디':
                q &= Q(id__icontains = search_keyword )

            if search_time_keyword == '상품정보':
                q &= Q(product_id__products__icontains = search_keyword)

            searched_reviews = reviews.filter(q).distinct()

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
        
class CommentView(View):
    @jwt_expression
    def post(self, request, review_id):
        try:
            data = json.loads(request.body)

            user         = User.objects.get(id=request.user)
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
        
