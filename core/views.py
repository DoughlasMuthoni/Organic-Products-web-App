
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from core.models import Product, Category, Vendors, ProductReview, ProductImages, Address 
from django.db.models import Count, Avg
from taggit.models import Tag
from core.forms import ProductReviewForm, ProductForm, ProductImageForm
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.contrib import messages

def indexPage(request):
    # Retrieve all products
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

# shop page

def shopPage(request):
    context = {}
    return render(request, 'shop.html', context)

def category_list_views(request):
    # categories = Category.objects.all()
    categories = Category.objects.all().annotate(product_count=Count("category"))

    context = {
        "categories": categories
    }
    return render(request, 'category-list.html', context)

def category_products_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status ="published", category =category)
    context ={
        "category": category,
        "products": products
    }
    return render(request, "category-product-list.html", context)


def vendors_list_view(request):
    vendor = Vendors.objects.all()
    context = {
        "vendors" :vendor
    }
    return render(request, 'vendors-list.html', context)


def vendors_details_view(request, vid):

    vendor = Vendors.objects.get(vid=vid)

    products = Product.objects.filter(vendor=vendor, product_status ="published")

    context = {
        "vendors" :vendor,
        "products":products
    }
    return render(request, 'vendors-details.html', context)

 #product view details

def product_list_views(request):
    product = Product.objects.all()
    context = {
        "product": product
    }
    return render(request, 'product-list.html', context)

def tag_list(request, tag_slug=None):
    # Get the products that are published
    products = Product.objects.filter(product_status="published").order_by("-id")
    tag = None

    # If tag_slug is provided, filter products by the tag
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])

    # Paginate the filtered products list
    paginator = Paginator(products, 12)  # 12 products per page
    page = request.GET.get('page')  # Get the page number from the GET parameter
    try:
        page_obj = paginator.get_page(page)  # Get the products for the current page
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)  # Default to page 1 if the page is not an integer
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)  # Return the last page if the page is out of range

    # Create the context to pass to the template
    context = {
        "products": page_obj,
        "tag": tag
    }

    # Render the page with the filtered products and tag context
    return render(request, "tag.html", context)



def ajax_add_review(request, pid):
    try:
        product = Product.objects.get(pid=pid)
    except Product.DoesNotExist:
        return JsonResponse({'bool': False, 'message': 'Product not found'})

    if not request.user.is_authenticated:
        return JsonResponse({'bool': False, 'message': 'User must be logged in'})

    review_text = request.POST.get('review')
    rating = request.POST.get('rating')

    if not review_text or not rating:
        return JsonResponse({'bool': False, 'message': 'Review text and rating are required'})

    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
    except (ValueError, TypeError):
        return JsonResponse({'bool': False, 'message': 'Invalid rating value'})

    # Check if the user has already reviewed this product
    if ProductReview.objects.filter(user=request.user, product=product).exists():
        return JsonResponse({'bool': False, 'message': 'You have already reviewed this product'})

    review = ProductReview.objects.create(
        user=request.user,
        product=product,
        review=review_text,
        rating=rating,
    )

    context = {
        'user': request.user.username,
        'review': review_text,
        'rating': rating,
    }

    average_reviews = ProductReview.objects.filter(product=product).aggregate(Avg("rating"))
    average_rating = average_reviews.get('rating__avg', 0)

    return JsonResponse({
        'bool': True,
        'context': context,
        'average_reviews': average_rating
    })

#searching products

def search_view(request):
    query = request.GET.get("q")

    products = Product.objects.filter(title__icontains=query).order_by("-date")
    context ={
        "products" :products,  
        "query" :query,
        
    }
    return render(request, "search.html", context)

 
def filter_product(request):
   
    categories = request.GET.getlist('category[]')
    vendors = request.GET.getlist("vendor[]")

    # Filter products that are 'published', ordered by the latest ID, and distinct
    products = Product.objects.filter(product_status="published").order_by("-id").distinct()

    # If there are selected categories, filter products by category IDs
    if categories:
        products = products.filter(category__id__in=categories).distinct()

    # If there are selected vendors, filter products by vendor IDs
    if vendors:
        products = products.filter(vendor__id__in=vendors).distinct()

    # Render the filtered products list to a string
    data = render_to_string("core/async/product-list.html", {"products": products})

    # Return the rendered HTML in a JSON response
    return JsonResponse({"data": data})



# def add_to_cart(request):
#     cart_product = {}

#     # Add product to cart using the GET parameters
#     cart_product[str(request.GET['id'])] = {
#         'title': request.GET.get('title', ''),
#         'qty': request.GET.get('qty', 1),  # Default quantity to 1 if not provided
#         'price': request.GET.get('price', 0),  # Default to 0 if no price
#         'image': request.GET.get('image', ''),
#         'pid': request.GET.get('pid', ''),
#     }

#     # If cart data exists in the session, update the cart
#     if 'cart_data_obj' in request.session:
#         cart_data = request.session['cart_data_obj']

#         # Check if product already exists in the cart
#         if str(request.GET['id']) in cart_data:
#             # Update the quantity of the existing product
#             cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
#         else:
#             cart_data.update(cart_product)
        
#         # Save the updated cart data back to the session
#         request.session['cart_data_obj'] = cart_data

#     else:
#         # If cart doesn't exist in the session, create a new one
#         request.session['cart_data_obj'] = cart_product

#     return JsonResponse({
#         'data': request.session['cart_data_obj'],
#         'totalcartitems': len(request.session['cart_data_obj']),
#     })

       

# def update_cart(request):
    
#     product_id = request.GET.get('id')
#     quantity = request.GET.get('qty')

#     if not product_id or not quantity:
#         return JsonResponse({'error': 'Product ID and quantity are required'}, status=400)

#     try:
        
#         quantity = int(quantity)
#         if quantity <= 0:
#             return JsonResponse({'error': 'Quantity must be greater than 0'}, status=400)

        
#         cart = request.session.get('cart', {})

        
#         if product_id in cart:
#             cart[product_id]['qty'] = quantity
#         else:
#             return JsonResponse({'error': 'Product not found in cart'}, status=404)

        
#         request.session['cart'] = cart
    
        
#         return JsonResponse({'message': 'Cart updated successfully', 'cart': cart})

#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)


# def cart_view(request):
    cart_total_amount = 0

    # Debugging: Print the session data to the console
    print("Cart Data in Session:", request.session.get('cart_data_obj', 'No cart data'))

    if 'cart_data_obj' in request.session:
        # Iterate over each item in the cart session
        for p_id, item in request.session['cart_data_obj'].items():
            try:
                # Ensure price is a float and clean it
                price = float(item['price'])

                # Ensure quantity is an integer
                qty = int(item['qty']) if item['qty'].isdigit() else 1

            except ValueError:
                # If there's a value error (invalid price or qty), set default values
                price = 0.0
                qty = 1
                messages.error(request, f"Invalid data for item {item.get('title', 'Unknown')}. Defaulting to price: 0 and quantity: 1.")
            
            # Calculate the total price for this item (price * qty)
            total_price = round(price * qty, 2)  # Round to 2 decimal places for clarity
            
            # Add the item total price to the session data
            item['total_price'] = total_price

            # Add the total item price to the overall cart total
            cart_total_amount += total_price

        # Render the cart view with updated data
        return render(request, 'cart.html', {
            'cart_data': request.session['cart_data_obj'],
            'totalcartitems': len(request.session['cart_data_obj']),
            'cart_total_amount': round(cart_total_amount, 2),  # Round to 2 decimal places
        })
    
    else:
        # If the cart is empty, show a warning message
        messages.warning(request, "Your cart is empty")
        return render(request, 'cart.html')


def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.user = request.user  # Set the logged-in user as the creator
            product.save()
            
            # Handle product images if uploaded
            image_form = ProductImageForm(request.POST, request.FILES)
            if image_form.is_valid():
                for img in request.FILES.getlist('image'):  # Handle multiple images
                    ProductImages.objects.create(product=product, image=img)
            
            return redirect('core:product-list')  # Redirect to the product list page
    else:
        product_form = ProductForm()
    
    return render(request, 'add_product.html', {'product_form': product_form})

def product_list_ui(request):
    # Check if the user is an admin
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to view this page.")

    # Retrieve all products
    products = Product.objects.all()
    return render(request, 'product_list_ui.html', {'products': products})

def edit_product(request, product_id):
    # Get the product to edit
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('core:product_list_ui')  # Redirect back to the product list page
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form, 'product': product})

def delete_product(request, product_id):
    # Get the product to delete
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product.delete()
        return redirect('core:product_list_ui')  # Redirect back to the product list page
    
    return render(request, 'delete_product.html', {'product': product})

def product_purchase(request):
    # Retrieve all products
    products = Product.objects.all()
    return render(request, 'product_purchase.html', {'products': products})
def product_cart_views(request):
    # Get all products or filter by query if provided
    query = request.GET.get("q", "")
    if query:
        products = Product.objects.filter(title__icontains=query)
    else:
        products = Product.objects.all()

    # Initialize variables for the checkout process
    total_amount = 0
    selected_products = []

    if request.method == 'POST':
        # Process the quantities selected by the user
        for product in products:
            # Get the quantity for each product in the cart
            quantity_key = f"quantity_{product.id}"
            quantity = int(request.POST.get(quantity_key, 0))

            # Only include products that have a quantity greater than 0
            if quantity > 0:
                total_amount += product.price * quantity
                selected_products.append({
                    'product': product,
                    'quantity': quantity,
                    'total': product.price * quantity
                })

        # After calculating the total amount, redirect to checkout or handle payment logic
        return render(request, 'checkout.html', {
            'selected_products': selected_products,
            'total_amount': total_amount
        })

    # Render the page with products and a query (if any)
    return render(request, 'trial.html', {
        'products': products,
        'query': query
    })


def checkout_view(request):
    if request.method == 'POST':
        # Initialize variables to store the total amount and the selected products
        total_amount = 0
        selected_products = []

        # Process each product to get the quantity selected by the user
        for product in Product.objects.all():
            # Get the quantity for each product using its unique ID
            quantity_key = f"quantity_{product.id}"
            quantity = int(request.POST.get(quantity_key, 0))

            # If the user selected a quantity greater than 0, calculate the total price for that product
            if quantity > 0:
                total_amount += product.price * quantity
                selected_products.append({
                    'product': product,
                    'quantity': quantity,
                    'total': product.price * quantity
                })

        # If there are selected products, render the checkout page with the order summary
        if selected_products:
            return render(request, 'checkout.html', {
                'selected_products': selected_products,
                'total_amount': total_amount
            })
        else:
            # If no products are selected, redirect back to the product list with a message
            return redirect('core:product-cart')  # Or show an error message like 'Please select products'
    
    # If the request method is not POST (i.e., the user directly navigates to the checkout URL), redirect to product list
    return redirect('core:product-cart')





def pro_details(request, pid):
    # Retrieve the product by its unique 'pid'
    product = get_object_or_404(Product, pid=pid)
    products = Product.objects.filter(category=product.category).exclude(pid=pid)
    product_images = product.product_images.all()

    context = {
        'product': product,
        "products": products,
        "product_images": product_images,
       
    }

    return render(request, 'product-details.html', context)
