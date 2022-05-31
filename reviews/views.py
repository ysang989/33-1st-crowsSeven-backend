import json

from django.views       import View
from django.http        import JsonResponse
from django.db.models   import Q

from reviews.models     import Review, Comment
from users.models       import User

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

            if Review.objects.filter(id = review_id).exists():
                review.view_count = review.view_count+1
                review.save()

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
