from django.contrib import admin

# Register your models here.
from core.models import Product, Category, Vendors,ProductImages,Address 



class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin] 
    list_display = ['user', 'title','image', 'price', 'category','vendor','featured', 'product_status','pid']

class  CategoryAdmin(admin.ModelAdmin):
    list_display = [ 'title', 'category_image']

class  VendorsAdmin(admin.ModelAdmin):
    list_display = [ 'title', 'vendor_image']




class  AddressAdmin(admin.ModelAdmin):
    list_display = [ 'user', 'address', 'status']


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vendors, VendorsAdmin)
admin.site.register(Address, AddressAdmin)