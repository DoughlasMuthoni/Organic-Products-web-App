from django.contrib import admin

# Register your models here.
from core.forms import ProductForm, VendorForm
from core.models import  Product, Category, Vendors,ProductImages,CartOrder, CartOrderItems, Wishlist,ProductReview,Address 



class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    form = ProductForm  # Use the custom form
    inlines = [ProductImagesAdmin]  # Inline for product images

    # Fields to display in the list view of the admin panel
    list_display = [
        'user', 
        'title', 
        'image', 
        'price', 
        'category', 
        'vendor', 
        'featured', 
        'product_status',  # Dropdown field for product status
        'pid', 
        'date', 
        'digital',
        'sku',
        'updated',  # Optionally display the last update date
    ]

    # Fields to include in search functionality
    search_fields = [
        'title', 
        'product_status', 
        'vendor__name',  # Search by vendor name (assuming Vendor has a 'name' field)
        'category__name',  # Search by category name (assuming Category has a 'name' field)
        'tags__name',  # Search by tags (if using TaggableManager)
    ]

    # Optionally, you can filter by product status or other fields in the sidebar.
    list_filter = [
        'product_status', 
        'featured', 
        'in_stock', 
        'category', 
        'vendor'
    ]

    # Customize ordering if needed (for example, to order by the creation date)
    ordering = ['-date']

    # Optionally, limit what fields are displayed in the edit form in the admin
    fieldsets = (
        (None, {
            'fields': ('title', 'user', 'category', 'vendor', 'description', 'price','old_price', 'tags', 'image', 'stock_count', 'life', 'type', 'featured', 'product_status', 'status', 'in_stock', 'mfd', 'digital')
        }),
    )
class  CategoryAdmin(admin.ModelAdmin):
    list_display = [ 'title', 'category_image']

class VendorAdmin(admin.ModelAdmin):
    form = VendorForm  # Use the custom form for vendor management
    list_display = ['title', 'contact', 'address', 'authentic_rating', 'shipping_on_time', 'date']
    search_fields = ['title', 'contact', 'address']
    list_filter = ['authentic_rating', 'shipping_on_time']
    
    # Optional: You can add filtering options here (e.g., date, shipping_on_time)
    ordering = ['-date']

class CartOrderAdmin(admin.ModelAdmin):
    list_display =[ 'user', 'price', 'paid_status', 'order_date']

class CartOrderItemAdmin(admin.ModelAdmin):
    list_display =[ 'order', 'invoice_no', 'item', 'image', 'qty', 'price', 'total', 'product_status']

class ProductReviewAdmin(admin.ModelAdmin):
    list_display =[ 'user', 'product', 'review', 'rating']

class  WishlistAdmin(admin.ModelAdmin):
    list_display =[ 'user', 'product', 'date']


class  AddressAdmin(admin.ModelAdmin):
    list_display = [ 'user', 'address', 'status']


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vendors, VendorAdmin)
admin.site.register(CartOrderItems, CartOrderItemAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Address, AddressAdmin)
