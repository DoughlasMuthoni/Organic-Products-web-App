
from django.urls import path
from .import views
from .views import AddVendorView, EditVendorView, DeleteVendorView, VendorListView

app_name = 'core'

urlpatterns =[
    path('', views.indexPage, name="home"),
    #products
    path('product/', views.product_list_views, name="product-list"),
    path('product-cart/', views.product_cart_views, name="product-cart"),
    path('checkout/', views.checkout_view, name='checkout'),
    path('pro-details/<str:pid>/', views.pro_details, name='pro-details'),

    #categories
    path('category/', views.category_list_views, name="category_list"),
    path('category/add/', views.add_category, name='add-category'),
    path('categories/', views.category_list, name='category-list'),
    path('category/edit/<str:cid>/', views.edit_category, name='edit-category'),
    path('category/delete/<str:cid>/', views.delete_category, name='delete-category'),
    path('category/<cid>/', views.category_products_list_view, name="category-product-list"),

    
    #vendors
    path('vendor/', views.vendors_list_view, name="vendor-list"),
    path('vendorDetails/<vid>/', views.vendors_details_view, name="vendor-details"),
    path('vendors/', VendorListView.as_view(), name='vendor-list'),  # Display a list of vendors
    path('vendor/add/', AddVendorView.as_view(), name='add-vendor'),  # Add a new vendor
    path('vendor/edit/<int:pk>/', EditVendorView.as_view(), name='edit-vendor'),  # Edit vendor
    path('vendor/delete/<int:pk>/', DeleteVendorView.as_view(), name='delete-vendor'),  # Delete vendor
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
    path('ajax-add-review/<str:pid>/', views.ajax_add_review, name="ajax-add-review"),
    path('add-to-cart/', views.add_to_cart, name="add-to-cart"),
    path('cart/', views.cart_view, name="cart"),
    path('delete-from-cart/', views.delete_item_from_cart, name="delete-from-cart"),
    path('update-cart/', views.update_cart, name="update-cart"),
    path('checkoutn/', views.checkout, name='checkoutn'),
    path('completed-payment/', views.payment_completed, name='completed-payment'),
    path('customer-dashboard/', views.customer_dashboard, name='customer-dashboard'),

]