from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from home.models import Coaches
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .forms import ZipSearchForm, CoachForm
import pgeocode
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout

def calculate_distance(zip_code, coach):
    dist = pgeocode.GeoDistance('us')
    distance = dist.query_postal_code(zip_code, coach.zip_code) * 0.621371
    return distance

def get_coaches_with_distance(zip_code):
    coaches = Coaches.objects.all()
    coaches_with_distance = [(coach, calculate_distance(zip_code, coach)) for coach in coaches]
    coaches_with_distance.sort(key=lambda x: x[1])
    return coaches_with_distance

def home(request):
    if request.method == "POST":
        form = ZipSearchForm(request.POST)
        if form.is_valid():
            zip_code = form.cleaned_data['zip_code']
            coaches_with_distance = get_coaches_with_distance(zip_code)
            form = ZipSearchForm()
            return render(request, 'nearme.html', {'coaches_with_distance': coaches_with_distance, 'form': form})
    else:
        form = ZipSearchForm()
    context = {'form': form}
    return render(request, 'index.html', context)

def becomecoach(request):
    if request.method == "POST":
        form = CoachForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('home:home'))
        else:
            print("Form is not valid")
            print(form.errors)
    form = CoachForm()
    return render(request, 'becomecoach.html', {'form': form})

def nearme(request):
    if request.method == "POST":
        form = ZipSearchForm(request.POST)
        if form.is_valid():
            zip_code = form.cleaned_data['zip_code']
            coaches_with_distance = get_coaches_with_distance(zip_code)
            form = ZipSearchForm()
            return render(request, 'nearme.html', {'coaches_with_distance': coaches_with_distance, 'form': form})
    else:
        form = ZipSearchForm()
    context = {'form': form}
    return render(request, 'nearme.html', context)



def coach_detail(request, coach_id):
    coach = get_object_or_404(Coaches, pk=coach_id)


    context = {
        'coach': coach,

            }


    return render(request, 'coachdetail.html', context)


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
        if password == confirm_password:
            # Check if the user already exists
            if not User.objects.filter(username=username).exists():
                # Hash the password
                hashed_password = make_password(password)
                
                # Create and save the user
                user = User(username=username, email=email, password=hashed_password)
                user.save()
                
                # Redirect to a success page or login page
                return HttpResponseRedirect(reverse('home:becomecoach'))
            else:
                return HttpResponse('User already exists.')
        else:
            return HttpResponse('Passwords do not match.')
    else:
        # Render the signup form template
        return render(request, 'register.html')
    
def user_login(request):
    if request.method == 'POST':
        # Retrieve username and password from request
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        # Use Django's built-in authenticate method
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            # If user is valid and active, log the user in and redirect to a success page
            login(request, user)
            return HttpResponseRedirect(reverse('home:home'))
        else:
            # Return an 'invalid login' error message or redirect to the login page again
            
            return HttpResponse('Invalid login credentials.')
    else:
        # Render the login form template
        return render(request, 'login.html')
    
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home:home'))