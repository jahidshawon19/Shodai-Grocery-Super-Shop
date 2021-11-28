from django.contrib import admin

from .models import *
# Register your models here.

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['name', 'phone','email','address', 'city','area', 'zipcode']
    search_fields = ['phone']
    list_filter = ['name', 'address', 'city']
    list_per_page = 10

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'id','product_name', 'category', 'brand', 'selling_price', 'discounted_price']
    search_fields = ['product_name']
    list_filter = ['category', 'brand']
    list_per_page = 10

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'quantity', 'order_date', 'status']    
    search_fields = ['customer']
    list_filter = ['order_date', 'status']
    list_per_page = 10


@admin.register(Banner)
class BannerModelAdmin(admin.ModelAdmin):
    list_display = ['image_tag']