from django.contrib import admin
from .models import customer,product,cart,Payment,orderplaced,Wishlist

# Register your models here.
@admin.register(product)
class productModelAdmin(admin.ModelAdmin):
    list_display=['id','title','discount_price','category','product_image']
@admin.register(customer)
class customerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','locality','city','state','zipcode']

@admin.register(cart)
class cartModelAdmin(admin.ModelAdmin):
    list_display=['id','user','Product','quantity']

@admin.register(Payment)
class paymentModelAdmin(admin.ModelAdmin):
    list_display=['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']

@admin.register(orderplaced)
class orderplacedModelAdmin(admin.ModelAdmin):
    list_display=['id','user','Customer','Product','quantity','ordered_data','status','payment']

@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display=['id','user','Product']