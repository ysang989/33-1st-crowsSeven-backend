from django.views       import View
from django.http        import JsonResponse
from django.db.models   import Q

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
            product          = Product.objects.get(id = product_id)
            option_products  = OptionProduct.objects.filter(product_id = product_id)

            if OptionProduct.objects.filter(Q(product_id=product_id) & Q(shoe_size_id=None) & Q(phone_type_id=None) & Q(airpot_type_id=None)):
                option_existence = False

            else: 
                option_existence = True
            
            option_list = {}
            option_type = option_products[0]

            if option_type.shoe_size:
                option_list['option_type'] = 'shoe_size',

            if option_type.phone_type:
                option_list['option_type'] = 'phone_type',

            if option_type.airpot_type:
                option_list['option_type'] = 'airpot_type'

            option_list['option'] = []

            for option_product in option_products:
                option_list['option'].append({
                    'shoe_size_name'   : option_product.shoe_size.size if option_product.shoe_size else None,
                    'phone_type_name'  : option_product.phone_type.name if option_product.phone_type else None,
                    'airpot_type_name' : option_product.airpot_type.name if option_product.airpot_type else None,
                    'stock'            : option_product.stock,
                    'option_product_id': option_product.id
                })
                
            results={
                'id'                 : product.id,
                'name'               : product.name,
                'description'        : product.description,
                'thumbnail_image_url': product.thumbnail_image_url,
                'the_newest'         : product.the_newest,
                'price'              : product.price,
                'option_list'        : option_list['option'],
                'option_type'        : option_list.get('option_type'),
                'option_existence'   : option_existence,
            }

            return JsonResponse({'message' : results}, status=200)
            
        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

