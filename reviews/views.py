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

class ReviewDetailView(View):
    def get(self, request, review_id):
        try:
            results = []
            review  = Review.objects.get(id=review_id)
            
            comments=[{
                    'comment_writer'    : comment.user.name[0]+"***",
                    'comment_created_at': comment.created_at,
                    'content'           : comment.content
                } for comment in Comment.objects.select_related('review').filter(review_id=review.id)]

            if Review.objects.filter(id=review_id).exists():
                review.view_count = review.view_count+1
                review.save()

            product = [{
                'product_name'           : review.product.name,
                'product_price'          : review.product.price,
                'product_thumbnail_image': review.product.thumbnail_image_url
            }]

            related_reviews      = Reviews.objects.exclude(id=review_id)
            related_review=[{
                'review_id'        : have_relation_review.id,
                'review_product'   : have_relation_review.product.name,
                'review_title'     : have_relation_review.title,
                'review_writer'    : have_relation_review.user.name[0]+"***",
                'review_created_at': have_relation_review.created_at,
                'review_view_poitn': have_relation_review.view_count
            } for have_relation_review in related_reviews]

            results.append({
                'title'           : review.title,
                'review_writer'   : review.user.name[0]+"***",
                'title_created_at': review.created_at,
                'view_count'      : review.view_count,
                'comment'         : comments,
                'product'         : product,
                'related_review'  : related_review
            })
            return JsonResponse({"message" : results}, status=200)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
