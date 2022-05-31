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
            product          = Product.objects.get(id=product_id)
            option_products  = OptionProduct.objects.filter(product_id=product_id)
            option_product   = option_products[0]
            option_existence = False if OptionProduct.objects.filter(Q(product_id=product_id) & Q(shoe_size_id=None) & Q(phone_type_id=None) & Q(airpot_type_id=None)) else True

            option_list = []
            option_type = '' 
            option_name = ''

            for option_product in option_products:
                if option_product.shoe_size:
                    option_type = 'shoe_size'
                    option_name = option_product.shoe_size.name
                    option_list.append({
                        'option_name' : option_name if option_name else None,
                        'stock'       : option_product.stock
                    })

                elif option_product.phone_type:
                    option_type = 'phone_type'
                    option_name = option_product.phone_type.name
                    option_list.append({
                        'option_name' : option_name if option_name else None,
                        'stock'       : option_product.stock
                    })

                elif option_product.airpot_type:
                    option_type = 'airpot_type'
                    option_name = option_product.airpot_type.name
                    option_list.append({
                        'option_name'      : option_name if option_name else None,
                        'stock'            : option_product.stock,
                        'option_product_id': option_product.id
                    })

            results={
                'id'                  : product.id,
                'name'                : product.name,
                'description'         : product.description,
                'thumbnail_image_url' : product.thumbnail_image_url,
                'the_newest'          : product.the_newest,
                'price'               : product.price,
                'option_type'         : option_type if option_type else None,
                'option_list'         : option_list,
                'option_existence'    : option_existence,
            }
           
            return JsonResponse({'results' : results}, status=200)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

class ProductSearchView(View):
    def get(self, request):
        try:
            # query parameter
            # QueryDict
            keyword = request.GET.get("keyword")
            # Q()
            # keyword의 존재 여부에 따라 filter 안에 조건을 더할지 말지
            objects = Product.objects.filter(name__contains=keyword)
            results = [{
                "product": object.name
            } for object in objects]

            return JsonResponse({"context" : results}, status=200)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
