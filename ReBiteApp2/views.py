from django.shortcuts import render
from django.db import IntegrityError
import datetime as dt

def main(request):
    return render(request, "main.html")

def login(request):
    return render(request, "login.html")

def home(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def menu(request):
    return render(request, "menu.html")
def book(request):    
    # Render book page if OTP verified
    return render(request, "book.html")


from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
import random
from ReBiteApp2.models import User,FoodItem
from ReBiteApp2.forms import FoodItemForm

from django.shortcuts import get_object_or_404


def add_food(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = FoodItemForm()
    
    return render(request, 'add_food.html', {'form': form})

def menu(request):
    food_items = FoodItem.objects.all()
    return render(request, 'menu.html', {'food_items': food_items})


def send_otp(request):
    if request.method == 'POST':
        name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        dob = request.POST.get("dob")
        email = request.POST.get("email")
        username = request.POST.get("username")
        district = request.POST.get("district")

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists. Please choose a different username.")
        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already exists. Please use a different email.")
        

        request.session.set_expiry(1256709600)  # Set session expiry to 2 weeks (optional)
        # Store user details in session
        request.session["name"] = name
        request.session["phone"] = phone
        request.session["password"] = password
        request.session["dob"] = dob
        request.session["email"] = email
        request.session["username"] = username
        request.session["district"] = district

        # Generate a random 4-digit OTP
        otp = str(random.randint(1000, 9999))
        request.session["otp"] = otp
        # Construct the email subject and message
        subject = 'Your OTP Code'
        message_body = f"Your OTP code is: {otp}"

        # Send the email with OTP
        send_mail(
            subject,
            message_body,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )

        return render(request, 'otp_confirmation.html')

    return render(request, 'send_otp.html')


def verify_otp(request):
    if request.method == "POST":
        otp_input = ''.join([request.POST.get(f'otp{i}') for i in range(1, 5)])
        correct_otp = request.session.get("otp")
        if otp_input == correct_otp:
            return redirect('save_user')
        else:
            return HttpResponse("Incorrect OTP, please try again.")
    return render(request, 'login_success.html')

def save_user(request):
    try:
        # Retrieve user details from session
        email = request.session.get("email")
        name = request.session.get("name")
        phone = request.session.get("phone")
        password = request.session.get("password")
        dob = request.session.get("dob")
        username = request.session.get("username")
        district = request.session.get("district")

        # Save user details into the database
        user = User(
            email=email,
            username=username,
            district=district,
            name=name,
            phone=phone,
            password=password,
            dob=dob,
            created_at=dt.date.today()
        )
        user.save()

        # Set the username in the session
        request.session["username"] = username

        return redirect('login_success')
    except IntegrityError:
        return HttpResponse("An error occurred while saving user details. Please try again.")

def otp_confirmation(request):
    # This is the page where the user will enter the OTP they received.
    return render(request, 'otp_confirmation.html')


def login_success(request):
    # Render the success page template
     return render(request, 'login_success.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username, password=password)
            request.session["username"] = username
            return redirect('login_success')
        except User.DoesNotExist:
            return HttpResponse("Invalid username or password. Please try again.")

    return render(request, 'login.html')

