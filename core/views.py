
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from core.models import  CartOrder, CartOrderItems, Product, Category, ProductReview, Vendors,ProductImages, Address, Wishlist 
from django.db.models import Count, Avg
from taggit.models import Tag
from core.forms import CategoryForm, ProductForm, ProductImageForm, ProductReviewForm, VendorForm
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, EmptyPage
from django.core.exceptions import ObjectDoesNotExist
import calendar
from django.db.models.functions import ExtractMonth 
from django.utils.timezone import now


from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

from user_authens.models import Profile

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
    category = get_object_or_404(Category, cid=cid)  # Fetch category by cid
    products = Product.objects.filter(product_status="published", category=category)
    context = {
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



#     cart_total_amount = 0

#     # Debugging: Print the session data to the console
#     print("Cart Data in Session:", request.session.get('cart_data_obj', 'No cart data'))

#     if 'cart_data_obj' in request.session:
#         # Iterate over each item in the cart session
#         for p_id, item in request.session['cart_data_obj'].items():
#             try:
#                 # Ensure price is a float and clean it
#                 price = float(item['price'])

#                 # Ensure quantity is an integer
#                 qty = int(item['qty']) if item['qty'].isdigit() else 1

#             except ValueError:
#                 # If there's a value error (invalid price or qty), set default values
#                 price = 0.0
#                 qty = 1
#                 messages.error(request, f"Invalid data for item {item.get('title', 'Unknown')}. Defaulting to price: 0 and quantity: 1.")
            
#             # Calculate the total price for this item (price * qty)
#             total_price = round(price * qty, 2)  # Round to 2 decimal places for clarity
            
#             # Add the item total price to the session data
#             item['total_price'] = total_price

#             # Add the total item price to the overall cart total
#             cart_total_amount += total_price

#         # Render the cart view with updated data
#         return render(request, 'cart.html', {
#             'cart_data': request.session['cart_data_obj'],
#             'totalcartitems': len(request.session['cart_data_obj']),
#             'cart_total_amount': round(cart_total_amount, 2),  # Round to 2 decimal places
#         })
    
#     else:
#         # If the cart is empty, show a warning message
#         messages.warning(request, "Your cart is empty")
#         return render(request, 'cart.html')


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
# @login_required
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






def pro_details(request, pid):
    # Retrieve the product by its unique 'pid'
    product = get_object_or_404(Product, pid=pid)

    products = Product.objects.filter(category=product.category).exclude(pid=pid)
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))
    reviews = ProductReview.objects.filter(product=product).order_by("-date")
    product_images = product.product_images.all()
    review_form = ProductReviewForm()

    make_review = True

    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()

        if user_review_count > 0:
            make_review = False

    context = {
        "make_review": make_review,
        "p": product,
        "products": products,
        "average_rating": average_rating,
        "reviews": reviews,
        "review_form": review_form,
        "product_images": product_images,
       
    }

    return render(request, 'product-details.html', context)

@login_required
def add_to_cart(request):
    # Ensure qty is an integer from the GET request
    try:
        qty = int(request.GET['qty'])  # Convert qty to integer
    except ValueError:
        qty = 1  # Default to 1 if there's an issue with the input

    cart_product = {}
    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'qty': qty,  # Store qty as an integer
        'price': request.GET['price'],
        'image': request.GET['image'],
        'pid': request.GET['pid'],
    }

    # Check if 'cart_data_obj' already exists in the session
    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] += qty  # Add to the existing qty
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        # If no cart exists in session, initialize it with the new product
        request.session['cart_data_obj'] = cart_product

    # Calculate the total number of items in the cart, considering quantity
    total_items = sum(int(item['qty']) for item in request.session['cart_data_obj'].values()) 

    return JsonResponse({
        "data": request.session['cart_data_obj'],
        'totalcartitems': total_items  # Total number of items considering quantities
    })
@login_required
def wishlist_view(request):
    wishlist = Wishlist.objects.all()
    context = {
       "wishlist":wishlist, 
    }
    return render(request, 'wishlist.html', context)
@login_required
def add_to_wishlist(request):
    try:
        product_id = request.GET.get("id")
        if not product_id:
            return JsonResponse({"error": "Product ID not provided"}, status=400)
        
        # Attempt to fetch the product
        product = Product.objects.get(id=product_id)

        # Check if the product is already in the wishlist
        wishlist_count = Wishlist.objects.filter(product=product, user=request.user).count()
        print(wishlist_count)

        if wishlist_count > 0:
            context = {
                "bool": True
            }
        else:
            # Add the product to the wishlist
            Wishlist.objects.create(
                product=product,
                user=request.user,
            )
            context = {
                "bool": True
            }
    except ObjectDoesNotExist:
        context = {
            "error": "Product does not exist"
        }
        return JsonResponse(context, status=404)
    except Exception as e:
        context = {
            "error": str(e)
        }
        return JsonResponse(context, status=500)
    
    return JsonResponse(context)

def get_wishlist_count(request):
    if request.user.is_authenticated:
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    else:
        wishlist_count = 0
    return JsonResponse({'wishlist_count': wishlist_count})



from django.core import serializers

from django.views.decorators.cache import never_cache

@never_cache
def remove_wishlist(request):
    # Validate the product ID from the GET request
    pid = request.GET.get('id')  # Use .get() to handle missing 'id' gracefully
    if not pid:
        return JsonResponse({"bool": False, "message": "Product ID is required."}, status=400)

    try:
        # Ensure the item exists in the user's wishlist
        wishlist_item = Wishlist.objects.get(id=pid, user=request.user)
    except Wishlist.DoesNotExist:
        return JsonResponse({"bool": False, "message": "Wishlist item does not exist."}, status=404)

    # Delete the product from the wishlist
    wishlist_item.delete()

    # Get the updated wishlist for the user
    wishlist = Wishlist.objects.filter(user=request.user)

    # Serialize updated wishlist data
    wishlist_json = serializers.serialize("json", wishlist)

    # Render updated wishlist HTML
    context = {"wishlist": wishlist}
    data = render_to_string("core/async/wishlist-list.html", context)

    # Return updated wishlist data and HTML
    return JsonResponse({"bool": True, "data": data, "wishlist": wishlist_json})

def cart_view(request):
    cart_total_amount = 0  # Initialize total amount

    # Check if the session contains cart data
    if "cart_data_obj" in request.session:
        cart_data = request.session.get("cart_data_obj", {})

        # Validate if the cart is empty
        if not cart_data:
            messages.warning(request, 'Your cart is empty!')
            return redirect("core:home")

        # Iterate over cart items
        for p_id, item in cart_data.items():
            try:
                # Ensure `qty` is an integer
                qty = int(item.get("qty", 0))
                
                # Validate and clean the price
                raw_price = item.get("price", "0")
                price = str(raw_price).replace(",", "")  # Remove commas
                
                # Handle invalid price formats
                if price.count('.') > 1:
                    parts = price.split('.')
                    price = parts[0] + '.' + parts[1]  # Keep first decimal
                
                # Handle cases where price is empty or not properly formatted
                if price:
                    price_parts = price.split()
                    price = price_parts[0] if price_parts else "0"
                else:
                    price = "0"

                item["price"] = float(price)  # Convert to float
                
                # Update cart total amount
                cart_total_amount += qty * item["price"]
            
            except (ValueError, KeyError, TypeError) as e:
                # Log and skip problematic items
                print(f"Error processing item {p_id}: {e}")
                continue

        # Render cart view
        return render(request, "cart.html", {
            "cart_data": cart_data,
            "totalcartitems": len(cart_data),
            "cart_total_amount": cart_total_amount,
        })
    
    # Handle case where cart_data_obj is missing
    else:
        messages.warning(request, 'Your cart is empty!')
        return redirect("core:home")

@login_required
def checkout(request):
    cart_total_amount = 0

    # Check if there is cart data in session
    if "cart_data_obj" in request.session:
        # Calculate total amount and process items
        for p_id, item in request.session["cart_data_obj"].items():
            try:
                # Ensure qty is an integer
                qty = int(item["qty"])
                
                # Clean price value
                price = str(item["price"]).replace(",", "")  # Remove commas
                if price.count('.') > 1:
                    price = price.split('.')[0] + '.' + price.split('.')[1]
                price = price.split()[0] 

                item["price"] = float(price)
                cart_total_amount += qty * float(price)
            except (ValueError, KeyError, TypeError) as e:
                print(f"Error processing item {p_id}: {e}")
                continue  

        # Create a new CartOrder
        order = CartOrder.objects.create(
            user=request.user,
            price=cart_total_amount,
            order_date=now()  # Add order_date with the current timestamp
        )

        # Create CartOrderItems for each item
        for p_id, item in request.session["cart_data_obj"].items():
            try:
                CartOrderItems.objects.create(
                    order=order,
                    invoice_no="INVOICE_NO-" + str(order.id),
                    item=item['title'],
                    image=item['image'],
                    qty=int(item['qty']),
                    price=float(item['price']),
                    total=int(item['qty']) * float(item['price'])
                )
            except (ValueError, KeyError, TypeError) as e:
                print(f"Error creating order item for {p_id}: {e}")
                continue
    
    # Fetch the active address for the user
    try:
        active_address = Address.objects.get(user=request.user, status=True)
    except Address.MultipleObjectsReturned:
        messages.warning(request, 'Multiple addresses activated; only one should be active!')
        active_address = None
    except Address.DoesNotExist:
        messages.warning(request, 'No active address found for the user.')
        active_address = None

    # Render the checkout template
    return render(request, "checkoutn.html", {
        "cart_data": request.session.get('cart_data_obj', {}),
        "totalcartitems": len(request.session.get('cart_data_obj', {})),
        "cart_total_amount": cart_total_amount,
        "active_address": active_address,
    })


@login_required
def customer_dashboard(request):
    orders_list = CartOrder.objects.filter(user=request.user)
    address = Address.objects.filter(user=request.user)
    
    orders = CartOrder.objects.annotate(month=ExtractMonth("order_date")).values("month").annotate(count=Count("id")).values("month", "count")
    month =[]
    total_orders = []

    for o in orders:
        month.append(calendar.month_name[o["month"]])

    for i in orders:
        total_orders.append(i["count"])

    


    if request.method == 'POST':
        print(request.POST) 
        address = request.POST.get('address')
        contact = request.POST.get('phone')
        
        new_address = Address.objects.create(
            user= request.user,
            address= address,
            contact= contact,

        )
        
        messages.success(request, 'Address added successfully!')
        return redirect('core:customer-dashboard')
    profile = Profile.objects.get(user=request.user)
    print("Your profile is:",profile )
    context ={

        "orders_list" : orders_list,
        "profile" : profile,
        "address" : address,
        "orders" : orders,
        "month" : month,
        "total_orders" : total_orders,
    }
    return render(request, 'customer_dashboard.html', context)



def order_details(request, id):
    
    order = get_object_or_404(CartOrder, user=request.user, id=id)

    # Fetch all items related to this order
    products = CartOrderItems.objects.filter(order=order)

    context = {
        "order": order,
        "products": products,
    }
    return render(request, 'order_details.html', context)

def make_address_default(request):
    id = request.GET.get("id")
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({'boolean':True})

def delete_item_from_cart(request):
    product_id = request.GET.get('id')
    if not product_id:
        return JsonResponse({'error': 'Product ID not provided'}, status=400)

    # Check if the session contains cart data
    if "cart_data_obj" in request.session:
        cart_data = request.session["cart_data_obj"]

        # Ensure the product_id exists in the cart before trying to delete it
        if product_id in cart_data:
            del cart_data[product_id]  # Delete the product from the cart

            # Update session
            request.session["cart_data_obj"] = cart_data  # Ensure session is updated immediately

    # Recalculate the total cart amount
    cart_total_amount = 0
    total_items = 0

    if "cart_data_obj" in request.session:
        for p_id, item in request.session["cart_data_obj"].items():
            try:
                # Ensure qty is an integer
                qty = int(item.get("qty", 0))

                # Validate and clean the price
                raw_price = str(item.get("price", "0")).replace(",", "")  # Remove commas
                if raw_price.count('.') > 1:
                    parts = raw_price.split('.')
                    raw_price = parts[0] + '.' + parts[1]  # Keep only the first decimal

                # Handle cases where price is empty or improperly formatted
                if raw_price.strip():
                    price_parts = raw_price.split()  # Split into components
                    price = price_parts[0] if price_parts else "0"
                else:
                    price = "0"

                # Convert the cleaned price to a float
                item["price"] = float(price)

                # Calculate total price
                cart_total_amount += qty * item["price"]
                total_items += qty  # Keep track of total items (including quantity)

            except (ValueError, KeyError, TypeError) as e:
                print(f"Error processing item {p_id}: {e}")
                continue  # Skip any malformed item data

    # Render the updated cart HTML
    context = render_to_string("core/async/cart-list.html", {
        "cart_data": request.session.get("cart_data_obj", {}),
        "totalcartitems": total_items,
        "cart_total_amount": cart_total_amount
    })

    # Return updated cart data as JSON response
    return JsonResponse({
        "data": context,
        "totalcartitems": total_items,
        "cart_total_amount": cart_total_amount
    })
 


def update_cart(request):
    product_id = request.GET.get('id')
    product_qty = request.GET['qty']
    
    if not product_id:
        return JsonResponse({'error': 'Product ID not provided'}, status=400)
    
    if "cart_data_obj" in request.session:
        cart_data = request.session['cart_data_obj']
    
        if product_id in cart_data:
            # Correct the dictionary access with square brackets
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data  

    # Recalculate the total cart amount
    cart_total_amount = 0
    total_items = 0
    if "cart_data_obj" in request.session:
        for p_id, item in request.session["cart_data_obj"].items():
            try:
                qty = int(item["qty"])  # Ensure qty is an integer
                
                # Clean price value
                price = str(item["price"]).replace(",", "")  # Remove commas
                if price.count('.') > 1:
                    price = price.split('.')[0] + '.' + price.split('.')[1]  # Ensure only one decimal point
                price = price.split()[0]  # Remove any extra characters (e.g., spaces)

                # Store cleaned price back in the item
                item["price"] = float(price)  # Convert price to float to ensure proper formatting
                
                # Calculate total price
                cart_total_amount += qty * float(price)
                total_items += qty  # Keep track of total items (including quantity)
            except (ValueError, KeyError, TypeError) as e:
                print(f"Error processing item {p_id}: {e}")
                continue  # Skip any malformed item data

    # Render the updated cart HTML
    context = render_to_string("core/async/cart-list.html", {
        "cart_data": request.session['cart_data_obj'],
        'totalcartitems': total_items,
        "cart_total_amount": cart_total_amount
    })

    # Return updated cart data as JSON response
    return JsonResponse({
        'data': context, 
        'totalcartitems': total_items,
        'cart_total_amount': cart_total_amount
    })
def payment_completed(request):
    cart_total_amount = 0
    total_items = 0

    # Check if "cart_data_obj" exists in the session
    if "cart_data_obj" in request.session:
        for p_id, item in request.session["cart_data_obj"].items():
            try:
                qty = int(item["qty"])  # Ensure qty is an integer

                # Clean and validate the price value
                price = str(item["price"]).replace(",", "")  # Remove commas
                if price.count('.') > 1:  # Fix multiple decimal points
                    price = price.split('.')[0] + '.' + price.split('.')[1]
                price = price.split()[0]  # Remove extra characters like spaces
                item["price"] = float(price)  # Convert price to float

                # Update totals
                cart_total_amount += qty * float(price)
                total_items += qty
            except (ValueError, KeyError, TypeError) as e:
                print(f"Error processing item {p_id}: {e}")
                continue  # Skip any malformed item data
    else:
        # If "cart_data_obj" is missing, return an error response or handle appropriately
        return HttpResponse("Cart data not found. Please add items to the cart.", status=400)

    # Render the completed payment page with the calculated totals
    return render(request, "completed_payment.html", {
        "cart_data": request.session["cart_data_obj"],
        "totalcartitems": len(request.session["cart_data_obj"]),
        "cart_total_amount": cart_total_amount,
    })


class VendorListView(ListView):
    model = Vendors
    template_name = 'vendor_list.html'
    context_object_name = 'vendors'

class AddVendorView(View):
    def get(self, request):
        form = VendorForm()
        return render(request, 'vendor_add.html', {'form': form})

    def post(self, request):
        form = VendorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('core:vendor-list')  # Redirect to the vendor list view
        return render(request, 'vendor_add.html', {'form': form})

# View to edit an existing vendor
class EditVendorView(View):
    def get(self, request, pk):
        vendor = get_object_or_404(Vendors, pk=pk)
        form = VendorForm(instance=vendor)
        return render(request, 'vendor_edit.html', {'form': form, 'vendor': vendor})

    def post(self, request, pk):
        vendor = get_object_or_404(Vendors, pk=pk)
        form = VendorForm(request.POST, request.FILES, instance=vendor)
        if form.is_valid():
            form.save()
            return redirect('core:vendor-list')  # Redirect to the vendor list view
        return render(request, 'vendor_edit.html', {'form': form, 'vendor': vendor})

# View to delete a vendor
class DeleteVendorView(View):
    def get(self, request, pk):
        vendor = get_object_or_404(Vendors, pk=pk)
        vendor.delete()
        return redirect('core:vendor-list')  # Redirect to the vendor list view
    

# categories formatting


@staff_member_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_admin.html', {'categories': categories})

@staff_member_required
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('core:category-list')
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})

@staff_member_required
def edit_category(request, cid):
    category = get_object_or_404(Category, cid=cid)
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('core:category-list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'edit_category.html', {'form': form, 'category': category})

@staff_member_required
def delete_category(request, cid):
    category = get_object_or_404(Category, cid=cid)
    if request.method == "POST":
        category.delete()
        return redirect('core:category-list')
    return render(request, 'delete_category.html', {'category': category})


def ajax_add_review(request, pid):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'bool': False, 'error': 'User not authenticated'}, status=401)

    try:
        # Try to retrieve the product by its pid
        product = Product.objects.get(pid=pid)
    except Product.DoesNotExist:
        # If the product doesn't exist, return a 404 error
        return JsonResponse({'bool': False, 'error': 'Product not found'}, status=404)

    # Get review and rating from the request
    review = request.POST.get('review', '').strip()
    rating = request.POST.get('rating')

    # Ensure review and rating are provided
    if not review or not rating:
        return JsonResponse({'bool': False, 'error': 'Review or rating missing'}, status=400)

    try:
        # Try to convert rating to an integer, if it fails, return a 400 error
        rating = int(rating)
        if rating < 1 or rating > 5:
            # Ensure the rating is within a valid range (e.g., 1 to 5)
            return JsonResponse({'bool': False, 'error': 'Rating must be between 1 and 5'}, status=400)
    except ValueError:
        return JsonResponse({'bool': False, 'error': 'Invalid rating value'}, status=400)

    # Create the product review
    review_instance = ProductReview.objects.create(
        user=request.user,  # Use the authenticated user
        product=product,
        review=review,
        rating=rating,
    )

    # Prepare the context for the response
    context = {
        'user': request.user.username,  # Display the username
        'review': review_instance.review,
        'rating': review_instance.rating,
    }

    # Calculate the average rating for the product
    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))

    # Return the response with the created review and average rating
    return JsonResponse(
        {
            'bool': True,
            'context': context,
            'average_reviews': average_reviews['rating'],  # Extract the average rating value
        }
    )