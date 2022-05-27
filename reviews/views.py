import json

from django.views       import View
from django.http        import JsonResponse

from reviews.models     import Review, Comment
from products.models    import OptionProduct, Product
from users.models       import User
from users.utils        import jwt_expression

class ReviewView(View):
    @jwt_expression
    def post(self, request, product_id):
        try:
            data = json.loads(request.body)

            user           = request.user
            title          = data["title"]
            context        = data["context"]
            password       = data["password"]
            option_product = Product.objects.get(id = product_id).id

            Review.objects.create(
                user           = user,
                title          = title,
                context        = context,
                password       = password,
                viewpoint      = 0,
                option_product = option_product
            )

            return JsonResponse({"message" : "SUCCESS"}, status=200)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
        
#     def get(self, request, id):
#             try:
#                 results = []

#                 comments = {}
#                 for comment in Comment.objects.select_related('review').filter(review=id):
#                     comments[comment.name]= comment.content                
#                 # [comments[comment.datacomment.context) for comment in Comment.objects.select_related('review').filter(review=id)]                    
#                 review = Review.objects.get(id=id)
#                 if Review.objects.filter(id=id).exists():
#                     review.view_count = review.view_count+1
#                     review.save()

#                 results.append({
#                     '제목' : review.title,
#                     '작성일': review.created_at,
#                     '조회수': review.view_count,
#                     '댓글' : comments,
#                 })

#                 return JsonResponse({"message" : results}, status=200)

#             except KeyError :
#                 return JsonResponse({"message" : "KEY_ERROR"}, status=400)

# class CommentView(View):
#     @jwt_expression
#     def post(self, request, id):
#         try:
#             data = json.loads(request.body)

#             user         = request.user
#             review       = Review.objects.get(id=id).id
#             name         = data["name"]
#             content      = data["content"]
#             password     = data["password"]

#             Comment.objects.create(
#                 user     = user,
#                 reiew    = review,
#                 name     = name,
#                 content  = content,
#                 password = password
#             )

#             return JsonResponse({"message" : "SUCCESS"}, status=200)

#         except KeyError :
#             return JsonResponse({"message" : "KEY_ERROR"}, status=400)
        
