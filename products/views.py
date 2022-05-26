from django.views       import View
from django.http        import JsonResponse

from products.models    import (
    OptionProduct,
    Product,
    Material,
    PhoneType,
    AirpotType,
    ShoeSize,
    ProductCategory,
    DetailImage
)

class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product          = Product.objects.get(id=product_id)
            option_products  = OptionProduct.objects.filter(product_id=product_id)
            option_existence = True

            count_per_shoe_size   = {}
            count_per_airpot_type = {}
            count_per_phone_type  = {}

            for option_product in option_products:
                if option_product.airpot_type:
                    count_per_shoe_size[option_product.airpot_type.name]=option_product.stock
                else:
                    pass
                if option_product.phone_type:
                    count_per_shoe_size[option_product.phone_type.name]=option_product.stock
                else:
                    pass
                if option_product.shoe_size:
                    count_per_shoe_size[option_product.shoe_size.size]=option_product.stock
                else:
                    pass
            
            results={
                'id'                 : product.id,
                'name'               : product.name,
                'description'        : product.description,
                'thumbnail_image_url': product.thumbnail_image_url,
                'the_newest'         : product.the_newest,
                'price'              : product.price,
                'option_type' : {'count_per_shoe_size': count_per_shoe_size,
                                'count_per_airpot_type' : count_per_airpot_type,
                                'count_per_phone_type' :  count_per_phone_type
                                },
                'option_existence'  : option_existence
            }

            if not option_product.shoe_size and not option_product.airpot_type and not option_product.phone_type:
                results['single_product']= option_product.stock
                results['option_existence']=False
           
            return JsonResponse({'results' : results}, status=200)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
