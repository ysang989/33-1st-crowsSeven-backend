import json

from django.views       import View
from django.http        import JsonResponse

from reviews.models     import Review, Comment
from products.models    import OptionProduct, Product
from users.models       import User
from users.utils        import jwt_expression

class ReviewView(View):
    @jwt_expression
    def post(self, request, option_product_id):
        try:
            data = json.loads(request.body)
            user           = User.objects.get(id=request.user)
            title          = data["title"]
            context        = data["context"]
            password       = data["password"]
            option_product = OptionProduct.objects.get(id = option_product_id)

           
            Review.objects.create(
                    user           = user,
                    title          = title,
                    context        = context,
                    password       = password,
                    view_count     = 0,
                    option_product = option_product
                    )
        

            return JsonResponse({"message" : "SUCCESS"}, status=200)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

    


        
        # except Review.objects.get(option_product=option_product).Exist:
        #     return JsonResponse({"message" : "ALREADY_EXISTS"}, status=400)


        
    def get(self, request, option_product_id):
            try:
                results = []
                review = Review.objects.get(option_product_id=option_product_id)
                
                comments = {}
                
                for comment in Comment.objects.select_related('review').filter(review_id=review.id):
                    comments[comment.name]= comment.content
                                    
                if Review.objects.filter(option_product_id=option_product_id).exists():
                    review.view_count = review.view_count+1
                    review.save()

                results.append({
                    '제목' : review.title,
                    '작성일': review.created_at,
                    '조회수': review.view_count,
                    '댓글' : comments,
                })

                return JsonResponse({"message" : results}, status=200)

            except KeyError :
                return JsonResponse({"message" : "KEY_ERROR"}, status=400)

class CommentView(View):
    @jwt_expression
    def post(self, request, option_product_id):
        try:
            data = json.loads(request.body)

            user         = User.objects.get(id=request.user)
            review       = Review.objects.get(option_product_id=option_product_id)
            name         = data["name"]
            content      = data["content"]
            password     = data["password"]

            Comment.objects.create(
                user     = user,
                review    = review,
                name     = name,
                content  = content,
                password = password
            )

            return JsonResponse({"message" : "SUCCESS"}, status=200)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
        
