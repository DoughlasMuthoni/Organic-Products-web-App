import json
from urllib.request import HTTPBasicAuthHandler
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
from user_authens.credentials import LipanaMpesaPpassword, MpesaAccessToken
from user_authens.forms import ProfileForm, UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from user_authens.models import Profile, User
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver


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
        # Check if the user has a profile, and create one if it doesn't exist
        if not hasattr(request.user, 'profile'):
            Profile.objects.create(user=request.user)
        
        return redirect("core:home") 

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Hey, you are logged in!")
            return redirect("core:home")  
        else:
            messages.warning(request, "Invalid email or password. Please try again or create an account.")
    
    context = {}

    return render(request, "user_authens/sign-in.html", context)
 
#logging out
def logout_view(request):
    logout(request)
    messages.success(request, "You logged out!!!")
    next_page = request.GET.get('next', 'user_authens:sign-in')
    return redirect(next_page)
             
#  Adding the mpesa functions
#Display the payment form
# @login_required
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

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)




def profile_edit(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form .save()
            messages.success(request, 'Profile saved successfully')
            return redirect('core:customer-dashboard')  # Replace with the correct URL name
    else:
        form = ProfileForm(instance=profile)

    context = {
        "form": form,
        "profile": profile,
    }   
    return render(request, 'profile_edit.html', context)

def settings(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        image = request.FILES.get('image')  
        full_name = request.POST.get('full_name')  
        phone = request.POST.get('phone')  
        bio= request.POST.get('bio')  
        address = request.POST.get('address')  
        county = request.POST.get('county')  

        if image != None:
            profile.image = image

        profile.full_name = full_name
        profile.phone = phone
        profile.bio = bio
        profile.address = address
        profile.county = county


        profile.save()

        messages.success(request, 'profile updated successfully!!!')
        return redirect("user_authens:settings")
    context ={
        "profile": Profile
    }    

    return render(requests, 'core:settings.html')