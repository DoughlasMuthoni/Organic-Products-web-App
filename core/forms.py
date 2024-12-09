
from django import forms
from .models import Product, ProductImages
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from taggit.forms import TagWidget



class ProductForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())
    tags = forms.CharField(widget=TagWidget(), required=False)  # For tags
    image = forms.ImageField(required=False)
    
    class Meta:
        model = Product
        fields = ['category', 'title', 'vendor', 'description', 'price', 'tags', 'image', 'stock_count', 'life', 'type', 'status', 'featured']
        
class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImages
        fields = ['product', 'image']