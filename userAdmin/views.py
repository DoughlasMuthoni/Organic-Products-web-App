import datetime
from django.shortcuts import render
from django.db.models import Sum
from core.models import CartOrder, Category, Product
from user_authens.models import User

# Create your views here.
def dashboard(request):
    revenue = CartOrder.objects.aggregate(price=Sum("price"))
    total_orders_count = CartOrder.objects.all()
    all_products = Product.objects.all()
    all_categories = Category.objects.all()
    all_customers = User.objects.all()
    new_customers = User.objects.all().order_by("-id")
    latest_orders = CartOrder.objects.all()
    this_month = datetime.datetime.now().month

    monthly_revenue = CartOrder.objects.filter(order_date__month=this_month).aggregate(price=Sum("price"))

    context ={
      "revenue": revenue,  
      "total_orders_count": total_orders_count,  
      "all_products": all_products,  
      "all_categories": all_categories,  
      "all_customers": all_customers,  
      "new_customers": new_customers,  
      "latest_orders": latest_orders,  
      "monthly_revenue": monthly_revenue,  
    }

    return render(request, 'userAdmin/dashboard.html', context)