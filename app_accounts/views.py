import random
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages ,auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.conf import settings
from django.core.mail import send_mail
from .models import Profile, UserAddress
from app_admin_panel.views import *
from django.db import IntegrityError
from app_home.views import home
from app_checkout.views import checkout


# from django.contrib.auth.hashers import check_password
import logging

logger = logging.getLogger(__name__)

# Create your views here.
    #<<<<<<<<<<<<<<<<<<<< --------------------- >>>>>>>>>>>>>>>>>>>>
    #<<<<<<<<<<<<<<<<<<<< --------------------- >>>>>>>>>>>>>>>>>>>>
    #<<<<<<<<<<<<<<<<<<<<  user authentication  >>>>>>>>>>>>>>>>>>>>
    #<<<<<<<<<<<<<<<<<<<< --------------------- >>>>>>>>>>>>>>>>>>>>
    #<<<<<<<<<<<<<<<<<<<< --------------------- >>>>>>>>>>>>>>>>>>>>

#<<<<<<<<<<<<<<<<<<<<  To create a new acount for a new user  >>>>>>>>>>>>>>>>>>>>
def signup(request):
# capturing the form input values from the HTTP POST request 
    try:
        if request.method == "POST":
            get_otp = request.POST.get('otp')
            if not get_otp:   
                username = request.POST.get("username")  
                firstname = request.POST.get("firstname")
                lastname = request.POST.get("lastname")
                email = request.POST.get("email")
                pass1 = request.POST.get('pass1')       
                pass2 = request.POST.get('pass2')
                phone_no = request.POST.get('phno')
            
        # Form validation for signup details      
                if not username.strip():
                    messages.error(request, "please enter the usernmae")
                    return redirect('signup')
        
                if not phone_no.strip():
                    messages.error(request, "please enter your phone number")
                    return redirect('signup')
                    
                if len(phone_no)>10:
                    messages.error(request, "phone number only contain 10 numbers")
                    return redirect('signup')
        
                if User.objects.filter(username = username).exists():
                    messages.error(request, "usrename is already exists!")
                    return redirect('signup')
        
                if not firstname.strip():
                    messages.error(request, "please enter the firstname")
                    return redirect('signup')
        
                if len(username)>10:
                    messages.error(request, "username must be contain lessthan 10 characters!")
                    return redirect('signup')

                if not firstname.strip():
                    messages.error(request, "please enter your name")
                    return redirect('signup')
                
                if User.objects.filter(email=email).exists():
                    messages.error(request, "Email is already taken")
                    return redirect('signup')

                if Profile.objects.filter(mobile = phone_no).exists():
                    messages.error(request, "mobile number is alrady taken")
                    return redirect('signup')
                
                if User.objects.filter(username = username).exists():
                    messages.error(request, "This username  is alrady taken")
                    return redirect('signup')
                
                if not pass1:
                    messages.error(request, "Please enter a password")
                    return redirect('signup')
                
                if not pass2:
                    messages.error(request, "Please confirm your password")
                    return redirect('signup')
                
                if pass1 != pass2:
                    messages.error(request, "Password does not match")
                    return redirect('signup')
                
                if len(pass1)<8:
                    messages.error(request, "Password must contain minimum 8 characters!")
                    return redirect('signup')
                
                
                myuser = User.objects.create_user(username = username, email = email)
                myuser.set_password(pass1)
                myuser.first_name = firstname
                myuser.last_name = lastname
                myuser.is_active = False
                myuser.save()
                otp = int(random.randint(1000,9999))
                profile = Profile(user = myuser, mobile = phone_no, otp = otp)
                profile.save()
                mess = f'hello\t{myuser.username},\nYour OTP to varify your accountfor BookStall is {otp}\nThanks!'
                send_mail(
                    "Welcome to BookStall varify your Email.",
                    mess,
                    settings.EMAIL_HOST_USER,
                    [myuser.email],
                    fail_silently = False
                    )
                return render(request, "accounts/signup.html", {'otp':True, 'usr':myuser})
            else:
                get_email = request.POST.get('email')
                user = User.objects.get(email = get_email)
                if get_otp == Profile.objects.filter(user=user).last().otp:
                    user.is_active = True
                    user.save()
                    messages.success(request, f'Account is created for {user.email}')
                    Profile.objects.filter(user=user).delete()
                    return redirect(handle_login)
                else:
                    messages.warning(request, f'You entered a wrong OTP')
                    return render(request, 'accounts/signup.html', {'otp':True, 'usr':user})

        return render(request, "accounts/signup.html", {'otp':False})
    except:
        return render(request, 'temp_home/error-404-home.html')


#<<<<<<<<<<<<<<<<<<<<  To login a user for authorisation  >>>>>>>>>>>>>>>>>>>>
def handle_login(request):
    try:
        if request.method == "POST":
            username = request.POST.get("username")
            pass1 = request.POST.get('pass1')

            if not User.objects.filter(username = username):
                messages.error(request, "Invalid User name")
                return redirect(handle_login)
            
            if username is None :
                messages.warning("please enter username")
                return redirect(handle_login)
            
            if pass1 is None:
                messages.warning(request, "Please enter password")

            user = authenticate(request, username = username, password = pass1)

            if user is not None:
                login(request, user)
                messages.success(request,'logged in')
                return redirect('/')
            else:
                messages.error(request, "invalid password")
                return redirect(handle_login)
            
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, "accounts/login.html")
    except:
        return render(request, 'temp_home/error-404-home.html')



#<<<<<<<<<<<<<<<<<<<<  To login a user using otp  >>>>>>>>>>>>>>>>>>>>
def otp_login(request):
    try:
        if request.method == "POST":
            get_otp = request.POST.get('otp')
            if not get_otp:
                email = request.POST.get('email')
                try: 
                    user = User.objects.get(email=email)
                except:
                    messages.error(request, f"This is not a valid email id ")
                    return redirect(otp_login)
                
                if user is not None:
                    otp = int(random.randint(1000,9999))
                    profile = Profile(user = user, otp = otp)
                    profile.save()
                    mess=f"Hello {user.username},\nYour OTP to login to your acount for BookStall is {otp}\nThanks"
                    send_mail(
                        "Welcome to BookStall Varify your email for login.",
                        mess,
                        settings.EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=False
                    )
                    return render(request, 'accounts/otp_login.html', {"otp":True, "usr":user})
            
            else:
                get_email = request.POST.get('email')
                user = User.objects.get(email=get_email)
                profile = Profile.objects.get(user=user)
                if get_otp == Profile.objects.filter(user=user).last().otp:
                    login(request, user)
                    messages.success(request, f"Successfully logined {user.email}")
                    Profile.objects.filter(user=user).delete()
                    return redirect('/')
                else:
                    messages.warning(request, f"You entered a wrong OTP")
                    return render(request, 'accounts/otp_login.html', {"otp": True, "usr":user})
        
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'accounts/otp_login.html' )
    except:
        return render(request, 'temp_home/error-404-home.html')
    
    



#<<<<<<<<<<<<<<<<<<<<  To log out a user from the site  >>>>>>>>>>>>>>>>>>>>
@login_required(login_url='handle_login')
def user_logout(request):
    try:
        if request.user.is_authenticated:
            logout(request)
            return HttpResponseRedirect("/")
        else:
            messages.error(request, 'You need to login first')
            return render(home)
    except:
        return render(request, 'temp_home/error-404-home.html')


    #<<<<<<<<<<<<<<<<<<<< --------------------- >>>>>>>>>>>>>>>>>>>>
    #<<<<<<<<<<<<<<<<<<<< --------------------- >>>>>>>>>>>>>>>>>>>>
    #<<<<<<<<<<<<<<<<<<<< user profile settings >>>>>>>>>>>>>>>>>>>>
    #<<<<<<<<<<<<<<<<<<<< --------------------- >>>>>>>>>>>>>>>>>>>>
    #<<<<<<<<<<<<<<<<<<<< --------------------- >>>>>>>>>>>>>>>>>>>>
     
#<<<<<<<<<<<<<<<<<<<<  To get user profile  >>>>>>>>>>>>>>>>>>>>
def user_profile(request):
    try:
        if request.user.is_authenticated:

            addresses = UserAddress.objects.filter(user=request.user)
            user = request.user
            print("************************************", addresses, "*************************")

            context = {
                'user' : user,
                'addresses': addresses,
            }

            return render(request, 'temp_home/user_profile.html', context)
        messages.error(request, 'You need to login first')
        return redirect('home')
    except:
        return render(request, 'temp_home/error-404-home.html')

#<<<<<<<<<<<<<<<<<<<<  To change user password with using old password  >>>>>>>>>>>>>>>>>>>>
def change_user_password(request):
    try:
        user = request.user
        if user.is_authenticated:
            if request.method == "POST":
                old_password = request.POST.get('old_password')
                new_password = request.POST.get('new_password')
                confirm_password = request.POST.get('confirm_password')
                

                if not user.check_password(old_password):
                    messages.error(request, 'please enter the correct password !')
                    return redirect(change_user_password)
                
                if len(new_password) < 8:
                    messages.warning(request, 'password length must be greater than 8')
                    return redirect(change_user_password)
                
                
                if old_password == new_password or old_password == confirm_password:
                    messages.warning(request, 'the new password is same as your old password please change')
                    return redirect(change_user_password)

                if new_password != confirm_password:
                    messages.error(request, "Password mismatch")
                    return redirect(request, change_user_password)

                user.set_password(new_password)
                user.save()
                auth.login(request, user)
                messages.success(request, "password changed successfully !")
                return redirect(user_profile)
            return render(request, 'temp_home/change_password.html')
        else:
            messages.error(request, 'You need to login first')
            return redirect('home')
    except:
        return render(request, 'temp_home/error-404-home.html')


#<<<<<<<<<<<<<<<<<<<<    >>>>>>>>>>>>>>>>>>>>
def forgot_password(request):
    try:
        if request.method == "POST":
            get_otp = request.POST.get("otp")
            if not get_otp:
                email = request.POST.get("email")
                try:
                    user = User.objects.get(email=email)
                except:
                    messages.error(request, f"This is not a valid email id")
                    return redirect(forgot_password)

                if user is not None:
                    otp = int(random.randint(1000, 9999))
                    profile = Profile(user=user, otp=otp)
                    profile.save()
                    mess = f"Hello\t{user.username},\nYour OTP to resetting password for BookStall account - {otp}\nThanks!"
                    send_mail(
                        "welcome to BookStall Verify your Email for password resetting",
                        mess,
                        settings.EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=False
                    )
                    return render(request, "accounts/forget_password.html", {"otp": True, "user": user})
            else:
                get_email = request.POST.get("email")
                user = User.objects.get(email=get_email)
                if get_otp == Profile.objects.filter(user=user).last().otp:
                    Profile.objects.filter(user=user).delete()
                    return render(request, "accounts/reset_password.html", {"user": user})
                else:
                    messages.warning(request, f"You Entered a wrong OTP")
                    return render(request, "accounts/forget_password.html", {"otp": True, "user": user})

        if request.user.is_authenticated:
            return redirect(home )

        return render(request, "accounts/forget_password.html")
    except:
        return render(request, 'temp_home/error-404-home.html')
    

def reset_password(request):
    try:
        if request.method == "POST":
            pass1 = request.POST.get("pass1")
            pass2 = request.POST.get("pass2")
            email = request.POST.get("email")

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "User with provided email does not exist.")
                return redirect(forgot_password)

            if pass1 != pass2:
                messages.error(request, "Passwords do not match.")
                return redirect(forgot_password)

            user.set_password(pass1)
            user.save()
            messages.success(request, "Password successfully changed.")
            return redirect(handle_login) 

        return render(request, "accounts/reset_password.html")
    except:
        return render(request, 'temp_home/error-404-home.html')




def edit_user_profile(request):
    try:
        if request.user.is_authenticated:

            if request.method == "POST":
                username = request.POST.get("username")
                fname = request.POST.get("firstname")
                lname = request.POST.get("lastname")
                email = request.POST.get("email")

                if request.user.username != username:
                    if User.objects.filter(username = username).exists():
                        messages.error(request, "user name is already taken!")
                        return redirect('edit_user_profile')

                if not username.strip():
                    messages.error(request, "please enter username!")
                    return redirect('edit_user_profile')

                if not fname.strip():
                    messages.error(request, "please enter first name!")
                    return redirect('edit_user_profile')

                if not lname.strip():
                    messages.error(request, "please enter last name!")
                    return redirect('edit_user_profile')

                if not email:
                    messages.error(request, "please enter email!")
                    return redirect('edit_user_profile')

                edited_user = request.user
                edited_user.first_name = fname
                edited_user.username = username
                edited_user.last_name = lname
                edited_user.email = email
                edited_user.save()
                
                messages.success(request, 'profile updated successfully.')
                return redirect(user_profile)
            return render(request, 'temp_home/edit_profile.html')
        else:
            messages.error(request, 'You need to login first')
            return redirect(home)
    except:
        return render(request, 'temp_home/error-404-home.html')


def add_user_address_profile(request):
    try:
        if request.user.is_authenticated:
            if request.method == "POST":
                name = request.POST.get("name")
                ph_no = request.POST.get("number")
                house = request.POST.get("house")
                landmark = request.POST.get("landmark")
                district = request.POST.get("district")
                city = request.POST.get("city")
                state = request.POST.get("state")
                country = request.POST.get("country")
                pincode = request.POST.get("pincode")
                
                if len(name) == 0:
                    messages.warning(request, 'please enter name')
                    return redirect(add_user_address_profile)
                
                if len(ph_no) == 0:
                    messages.warning(request, 'please enter phone number')
                    return redirect(add_user_address_profile)
                
                if len(ph_no) > 10:
                    messages.warning(request, 'Phone number length must be minimum 10')
                    return redirect(add_user_address_profile)
                
                if len(name) == 0:
                    messages.warning(request, 'please enter house name')
                    return redirect(add_user_address_profile)
                
                if len(landmark) == 0:
                    messages.warning(request, 'please enter your landmark')
                    return redirect(add_user_address_profile)
                
                if len(district) == 0:
                    messages.warning(request, 'please enter your district')
                    return redirect(add_user_address_profile)
                
                if len(city) == 0:
                    messages.warning(request, 'please enter your city')
                    return redirect(add_user_address_profile)
                
                if len(state) == 0:
                    messages.warning(request, 'please enter your sate')
                    return redirect(add_user_address_profile)
                
                if len(country) == 0:
                    messages.warning(request, 'please enter your country')
                    return redirect(add_user_address_profile)
                
                if len(pincode) == 0:
                    messages.warning(request, 'please enter your pincode')
                    return redirect(add_user_address_profile)


                
                UserAddress.objects.create(
                    fullname = name,
                    contact_number = ph_no,    
                    user = request.user,
                    house_name = house,
                    landmark = landmark,
                    city = city,
                    district = district,
                    state = state,
                    country = country,
                    pincode = pincode,
                ).save()
                messages.success(request, 'address added success fully')
                return redirect(user_profile)
            return render(request, 'temp_home/add_user_address.html')
        else:
            messages.error(request, 'You need to login first')
            return redirect(home)
    except:
        return render(request, 'temp_home/error-404-home.html')


def edit_user_address(request, id):
    try:
        if request.user.is_authenticated:
            address = UserAddress.objects.get(id=id)
            context = {
                "address": address,
            }

            if request.method == "POST":
                name = request.POST.get("name")
                ph_no = request.POST.get("number")
                house = request.POST.get("house")
                landmark = request.POST.get("landmark")
                district = request.POST.get("district")
                city = request.POST.get("city")
                state = request.POST.get("state")
                country = request.POST.get("country")
                pincode = request.POST.get("pincode")

                            
                if len(name) == 0:
                    messages.warning(request, 'please enter name')
                    return render(request, 'temp_home/edit_address.html', context)
                
                if len(ph_no) == 0:
                    messages.warning(request, 'please enter phone number')
                    return render(request, 'temp_home/edit_address.html', context)
                
                if len(ph_no) > 10:
                    messages.warning(request, 'Phone number length must be minimum 10')
                    return render(request, 'temp_home/edit_address.html', context)
                
                if len(name) == 0:
                    messages.warning(request, 'please enter house name')
                    return render(request, 'temp_home/edit_address.html', context)
                
                if len(landmark) == 0:
                    messages.warning(request, 'please enter your landmark')
                    return render(request, 'temp_home/edit_address.html', context)
                
                if len(district) == 0:
                    messages.warning(request, 'please enter your district')
                    return render(request, 'temp_home/edit_address.html', context)
                
                if len(city) == 0:
                    messages.warning(request, 'please enter your city')
                    return render(request, 'temp_home/edit_address.html', context)
                
                if len(state) == 0:
                    messages.warning(request, 'please enter your sate')
                    return render(request, 'temp_home/edit_address.html', context)
                
                if len(country) == 0:
                    messages.warning(request, 'please enter your country')
                    return render(request, 'temp_home/edit_address.html', context)
                
                if len(pincode) == 0:
                    messages.warning(request, 'please enter your pincode')
                    return render(request, 'temp_home/edit_address.html', context)

                
                UserAddress.objects.filter(id=id).update(
                    fullname = name,
                    contact_number = ph_no,    
                    user = request.user,
                    house_name = house,
                    landmark = landmark,
                    city = city,
                    district = district,
                    state = state,
                    country = country,
                    pincode = pincode,
                )
                messages.success(request, "address updated.")
                return redirect(user_profile)
                
            address = UserAddress.objects.get(id=id)
            context = {
                "address": address,
            }
            return render(request, 'temp_home/edit_address.html', context)
        else:
            messages.error(request, 'You need to login first')
            return redirect(home)
    except:
        return render(request, 'temp_home/error-404-home.html')
    

def delete_user_address(request, id):
    try:
        if request.user.is_authenticated:

            address = UserAddress.objects.get(id=id)
            address.delete()
            messages.success(request, "address deleted successfully.")
            return redirect(user_profile)
        else:
            messages.error(request, 'You need to login first')
            return redirect(home)
    except:
        return render(request, 'temp_home/error-404-home.html')
