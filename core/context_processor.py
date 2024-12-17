


from django.shortcuts import get_object_or_404
from core.models import Product, Category, Vendors, ProductImages, Address

def default(request):
    categories = Category.objects.all()

    # Check if the user is authenticated before querying for the address
    if request.user.is_authenticated:
        address = Address.objects.filter(user=request.user).first()  # Returns None if not found
    else:
        address = None  # No address for unauthenticated users

    return {
        'categories': categories,
        'address': address,
        
    }




    
     