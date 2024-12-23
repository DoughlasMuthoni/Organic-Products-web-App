


from django.contrib import messages
from django.shortcuts import get_object_or_404
from core.models import Product, Category, Vendors, ProductImages, Address, Wishlist

def default(request):
    categories = Category.objects.all()
    vendors = Vendors.objects.all()

    # Initialize wishlist count
    wishlist_count = 0

    if request.user.is_authenticated:
        try:
            # Get the wishlist for the logged-in user
            wishlist_count = Wishlist.objects.filter(user=request.user).count()
        except Exception as e:
            # Handle any unexpected errors
            print(f"Error fetching wishlist: {e}")
            messages.warning(request, "There was an issue retrieving your wishlist.")

    # Check if the user is authenticated before querying for the address
    if request.user.is_authenticated:
        address = Address.objects.filter(user=request.user).first()  # Returns None if not found
    else:
        address = None  # No address for unauthenticated users

    return {
        'categories': categories,
        'wishlist_count': wishlist_count,  # Use a proper count
        'address': address,
        'vendors': vendors,
    }


    
        
  




    
     