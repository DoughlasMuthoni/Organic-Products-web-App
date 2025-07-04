from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from taggit.managers import TaggableManager
from user_authens.models import User
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

STATUS_CHOICE ={
    ("Processing", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
}


STATUS ={
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
}

RATING ={
    ("1", "⭐☆☆☆☆"),
    ("2", "⭐⭐☆☆"),
    ("3", "⭐⭐⭐☆☆"),
    ("4", "⭐⭐⭐⭐☆"),
    ("5", "⭐⭐⭐⭐⭐"),
}






def user_directory_path(instance, filename):
    # Check if the user is authenticated
    if instance.user.is_authenticated:
        return 'user_{0}/{1}'.format(instance.user.id, filename)
    else:
        # Handle the case for an anonymous user
        return 'anonymous/{0}'.format(filename)  # You can adjust this as needed



# models.py

class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=30, prefix="cat", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="category")  # Static path for images

    class Meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % (self.image.url))

    def __str__(self):
        return self.title


class Tags(models.Model):
    pass
class Vendors(models.Model):
    vid = ShortUUIDField(unique =True, length =10, max_length=30, alphabet ="abcdefgh12345")
    title = models.CharField(max_length=100) 
    image = models.ImageField(upload_to=user_directory_path, default="category.png")
    cover_image = models.ImageField(upload_to=user_directory_path, default="category.png")
    description = RichTextUploadingField(null=True, blank =True)
    address = models.TextField(max_length=100, default= "123 Machakos")
    contact = models.TextField(max_length=100, default= "+254 707 (264) 913")
    chat_resp_time = models.TextField(max_length=100, default="100")
    shipping_on_time = models.TextField(max_length=100, default="100")
    authentic_rating = models.CharField(max_length=100, default="100")
    days_return = models.CharField(max_length=100, default="100")
    warranty_period = models.CharField(max_length=100, default="100")
    # the vendor shop will be deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    class meta :
        verbose_name_plural = "Vendors"


    def vendor_image(self):
        return mark_safe('<img src = "%s" width ="50" height ="50"/> % (self.image.url)')
    
    def __str__(self) :
        return self.title
        
class Product (models.Model):
    pid = ShortUUIDField(unique =True, length =10, max_length=30, alphabet ="abcdefgh12345")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="category")
    title = models.CharField(max_length=100) 
    vendor = models.ForeignKey(Vendors, on_delete=models.SET_NULL, null=True, related_name="vendors")
    image = models.ImageField(upload_to="category", default="product.png")
    description =RichTextUploadingField(null=True, blank =True, default="This is a product")
    price = models.DecimalField(max_digits=12, decimal_places=2, default="1.99") 
    old_price = models.DecimalField(max_digits=12, decimal_places=2, default="2.99")
    mfd = models.DateTimeField(auto_now_add=False, null=True, blank=True) 
    type = models.CharField(max_length=100, default="organic",null=True, blank=True) 
    stock_count = models.CharField(max_length=100, default="8",null=True, blank=True) 
    life = models.CharField(max_length=100, default="100 months",null=True, blank=True) 
    tags =TaggableManager( blank=True)
    product_status = models.CharField(choices=STATUS, max_length=100, default= "in_review" )
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    sku = ShortUUIDField(unique =True, length =4, max_length=10, prefix="sku", alphabet ="1234567890 ")
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(null=True, blank=True)




    class Meta:
        verbose_name_plural = "products"


    def product_image(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="50" height="50"/>')
        return "No Image Available"

    
    def get_percentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price
    
  
class ProductImages(models.Model):
    image = models.ImageField(upload_to="product-images", default="product.jpg")
    product = models.ForeignKey(Product,related_name="product_images", on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)

class Meta :
    verbose_name_plural = "product Images"
        
#############cart orderitems and address ########################
#############cart orderitems and address ########################
from django.utils.timezone import now
class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2, default="1.99") 
    paid_status = models.BooleanField(default=False)
    order_date = models.DateField(auto_now_add=False, default=now)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=200, default="Processing")


    class Meta :
        verbose_name_plural = "Cart Orders"

class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=200, default="Processing")
    item = models.CharField(max_length=200)
    invoice_no = models.CharField(max_length=200)
    image = models.ImageField(upload_to='order_images/')  # Updated field
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=100.00) 
    total = models.DecimalField(max_digits=10, decimal_places=2, default=100.00) 

    class Meta:
        verbose_name_plural = "Cart Order Items"

    def order_image(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="50" height="50"/>')
        return "No Image Available"


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True) 
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class meta :
        verbose_name_plural = "Product Reviews"

    def __str__(self) :
        return self.product.title
    
    def get_rating(self):
        return self.rating
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True) 
    date = models.DateTimeField(auto_now_add=True)

    class meta :
        verbose_name_plural = "wishlists"

    def __str__(self) :
        return self.product.title
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) 
    address = models.CharField(max_length=100, null=False, blank=False, default="none")  
    contact = models.CharField(max_length=100, null=False, blank=True)  
    status = models.BooleanField(default=False)  
    class Meta:
        verbose_name_plural = "Addresses"  



     

     



        





        



             