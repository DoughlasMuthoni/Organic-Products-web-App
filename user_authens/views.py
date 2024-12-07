import json
from urllib.request import HTTPBasicAuthHandler
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
from user_authens.credentials import LipanaMpesaPpassword, MpesaAccessToken
from user_authens.forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from user_authens.models import User

# User = settings.AUTH_USER_MODEL 
# Create your views here.
def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hey {username}, Your account was created successfully")
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1']
            )
            login(request, new_user)
            return redirect ("core:home")
    else:
            form = UserRegisterForm()
    context = {
        'form' : form
    }
    return render(request, 'user_authens/sign-up.html', context)



          


def login_view(request):
    if request.user.is_authenticated:
        
        return redirect("core:home") 
    
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

       
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"hey You are logged in!")
            return redirect("core:home")  
        else:
            messages.warning(request, "Invalid email or password. Please try again or create an account.")
    
    context = {
       
    }

    return render(request, "user_authens/sign-in.html", context)

#logging out
def logout_view(request):
    logout(request) 
    messages.success(request, "You logged out!!!")
    return redirect("user_authens:sign-in")         
      
         
#  Adding the mpesa functions
#Display the payment form
def pay(request):
   """ Renders the form to pay """
   return render(request, 'user_authens/pay.html')


# Generate the ID of the transaction
def token(request):
    """ Generates the ID of the transaction """
    consumer_key = 'kYMG2xBGvUlBGW31KWyN6G039N2JWBXM9n1LiyUeT7h0lTGk'
    consumer_secret = 'jJ2VRhe3t2j28HDHGVtunmN8MyGI0BA7hIIfJRgnkdcK0Pj1lPXmtav1Gl4bJUXM'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuthHandler(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})


# Send the stk push
def stk(request):
    """ Sends the stk push prompt """
    if request.method =="POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "Doughlas",
            "TransactionDesc": "Web Development Charges"
        }
        response = requests.post(api_url, json=request, headers=headers)
        return HttpResponse("Successfully done!!")
      