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
    def get(self, request, id):
        try:
            results            = []
            option_information = []

            option_products  = OptionProduct.objects.filter(product_id = id)
            option_existence = True

            count_per_shoe_size   = {}
            count_per_airpot_type = {}
            count_per_phone_type  = {}
            
            for shoe_size in range(1,len(ShoeSize.objects.all())+1):
                for option_product in option_products.filter(shoe_size=shoe_size):
                    count_per_shoe_size[option_product.shoe_size.size] = option_products.get(shoe_size = shoe_size).stock

            for airpot_type in range(1,len(AirpotType.objects.all())+1):
                for option_product in option_products.filter(airpot_type = airpot_type):
                    count_per_airpot_type[option_product.airpot_type.name] = option_products.get(airpot_type = airpot_type).stock

            for phone_type in range(1,len(PhoneType.objects.all())+1):
                for option_product in option_products.filter(phone_type = phone_type):
                    count_per_phone_type[option_product.phone_type.name] = option_products.get(phone_type = phone_type).stock
            
            if not option_products[0].shoe_size and not option_products[0].airpot_type and not option_products[0].phone_type:
                option_information.append({
                    'single_product': OptionProduct.objects.get(product_id=id).stock
                })
                option_existence=False
                
            option_information.append({
                'count_per_phone_type' : count_per_phone_type,
                'count_per_airpot_type': count_per_airpot_type,
                'count_per_shoe_size'  : count_per_shoe_size,
            })
            
            results.append({
            'name'               : option_products[0].product.name,
            'description'        : option_products[0].product.description,
            'thumbnail_image_url': option_products[0].product.thumbnail_image_url,
            'the_newest'         : option_products[0].product.the_newest,
            'price'              : option_products[0].product.price,
            'option_information' : option_information,
            'option_existence'   : option_existence
            })

            return JsonResponse({"message" : results}, status=200)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
