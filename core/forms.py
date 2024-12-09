
from django import forms
from .models import Category, Product, ProductImages, Vendors
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from taggit.forms import TagWidget



class ProductForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())
    tags = forms.CharField(widget=TagWidget(), required=False)  # For tags
    image = forms.ImageField(required=False)

    # Define the choices for product status
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("disabled", "Disabled"),
        ("rejected", "Rejected"),
        ("in_review", "In Review"),
        ("published", "Published"),
    ]

    # Ensure the product status is displayed as a dropdown
    product_status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(),  # Render as a dropdown (select)
        required=True
    )

    class Meta:
        model = Product
        fields = ['category', 'title', 'vendor', 'description', 'price', 'tags', 'image', 'stock_count', 'life', 'type', 'product_status', 'status', 'featured']
        
class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImages
        fields = ['product', 'image']


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendors
        fields = [
            'title', 'image', 'cover_image', 'description', 'address', 
            'contact', 'chat_resp_time', 'shipping_on_time', 'authentic_rating', 
            'days_return', 'warranty_period', 'user'
        ]

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'image']