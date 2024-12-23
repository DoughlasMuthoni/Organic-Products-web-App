from django.urls import path
from . import views

app_name = 'user_authens'

urlpatterns = [
    path('sign-up/', views.register_view, name="sign-up"),
    path('sign-in/', views.login_view, name="sign-in"),
    path('sign-out/', views.logout_view, name="sign-out"),

     path('pay/', views.pay, name='pay'), # view the payment form
    path('stk/', views.stk, name='stk'), # send the stk push prompt
    path('token/', views.token, name='token'), # generate the token for that particular transaction
    path('profile/update/', views.profile_edit, name="profile-update"),
    path('settings/', views.settings, name="settings"),
]