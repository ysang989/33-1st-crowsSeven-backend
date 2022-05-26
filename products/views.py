from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

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
            
            for i in range(1,len(ShoeSize.objects.all())+1):
                for j in option_products.filter(shoe_size=i):
                    count_per_shoe_size[j.shoe_size.size] = option_products.get(shoe_size = i).stock

            for i in range(1,len(AirpotType.objects.all())+1):
                for j in option_products.filter(airpot_type = i):
                    count_per_airpot_type[j.airpot_type.name] = option_products.get(airpot_type = i).stock

            for i in range(1,len(PhoneType.objects.all())+1):
                for j in option_products.filter(phone_type = i):
                    count_per_phone_type[j.phone_type.name] = option_products.get(phone_type = i).stock
            
            if not option_products[0].shoe_size and not option_products[0].airpot_type and not option_products[0].phone_type:
                option_information.append({
                    '단일재고': OptionProduct.objects.get(product_id=id).stock
                })
                option_existence=False
                
            option_information.append({
                '아이폰기종별재고': count_per_phone_type,
                '에어팟기종별재고': count_per_airpot_type,
                '신발사이즈별재고': count_per_shoe_size,
            })
            
            results.append({
            '제품이름' : option_products[0].product.name,
            '제품설명' : option_products[0].product.description,
            '제품이미지': option_products[0].product.thumbnail_image_url,
            '신상여부' : option_products[0].product.the_newest,
            '제품가격' : option_products[0].product.price,
            '옵션정보' : option_information,
            '옵션유무' : option_existence
            })

            return JsonResponse({"message" : results}, status=200)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
