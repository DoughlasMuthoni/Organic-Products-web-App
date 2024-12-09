
from django.urls import path
from .import views

app_name = 'core'

urlpatterns =[
    path('', views.indexPage, name="home"),
    #products
    path('product/', views.product_list_views, name="product-list"),
    path('product-cart/', views.product_cart_views, name="product-cart"),
    path('checkout/', views.checkout_view, name='checkout'),
    path('pro-details/<str:pid>/', views.pro_details, name='pro-details'),

    #categories
    path('category/', views.category_list_views, name="category-list"),
    path('category/<cid>/', views.category_products_list_view, name="category-product-list"),
    #vendors
    path('vendor/', views.vendors_list_view, name="vendor-list"),
    path('vendorDetails/<vid>/', views.vendors_details_view, name="vendor-details"),
    #tags
    path('products/tag/<slug:tag_slug>/', views.tag_list, name="tags"),
    
    #search for a product
    path('search/', views.search_view, name="search"),
    #filter products
    path('filter-products/', views.filter_product, name="filter-product"),
    path('add-product/', views.add_product, name='add-product'),
    path('product_list_ui/', views.product_list_ui, name='product_list_ui'),
    path('product_purchase/', views.product_purchase, name='product_purchase'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit-product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete-product'),
    
    
    
]