


from core.models import Product, Category, Vendors, ProductReview, ProductImages, Address

def default(request):
    categories = Category.objects.all()
    vendors = Vendors.objects.all()

    # Check if the user is authenticated
    if request.user.is_authenticated:
        try:
            # If the user is authenticated, get their address
            address = Address.objects.filter(user=request.user).first()
        except Address.DoesNotExist:
            # Handle the case where the user has no address
            address = None  # or you could set a default address here
    else:
        # If the user is not authenticated, set address to None
        address = None

    return {
        'categories': categories,
        'address': address,
        'vendors': vendors,
    }



    
     