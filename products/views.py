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
            keyword = request.GET.get("keyword", None)
            limit   = int(request.GET.get("limit", 12))
            offset  = int(request.GET.get("offset", 0))

            q = Q()

            if keyword == None:
                return JsonResponse({"message": 'INVALIED_KEYWORD'}, status = 400)

            if keyword:
                q &= Q(name__contains=keyword)

            products = Product.objects.filter(q)[offset:offset+limit]
            results = [{
                "id"       : product.id,
                "thumbnail": product.thumbnail_image_url,
                "name"     : product.name,
                "price"    : product.price
            } for product in products]

            return JsonResponse({"products" : results}, status=200)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
