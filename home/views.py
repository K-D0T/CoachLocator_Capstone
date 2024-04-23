from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from home.models import Coaches
from .forms import ZipSearchForm, CoachForm, ProfileForm, VideoForm
from django.contrib.auth.decorators import login_required
import pgeocode
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from PIL import Image

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
                return HttpResponseRedirect(reverse('home:login'))
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
            return HttpResponseRedirect(reverse('home:profile'))
        else:
            messages.error(request, 'Invalid login credentials.')
            return HttpResponseRedirect(reverse('home:login'))
    else:
        # Render the login form template
        return render(request, 'login.html')
    
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home:home'))

@login_required
def profile(request):
    profile, created = Coaches.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profileform = ProfileForm(request.POST, request.FILES, instance=profile)
        videoform = VideoForm(request.POST)

        if profileform.is_valid():
            profile = profileform.save(commit=False)
            image = Image.open(profileform.cleaned_data['image'])
            image = image.resize((50, 50), Image.ANTIALIAS)
            profile.image.save(profileform.cleaned_data['image'].name, image, save=False)
            profile.save()
            # Only redirect if BOTH forms are not valid, else stay on the page to process the second form
            if not videoform.is_valid():
                return redirect('/profile')  # Redirect to the profile view after saving

        # Check if videoform is valid in a separate condition to allow for video addition without profile edit
        if videoform.is_valid():
            video = videoform.save(commit=False)
            video.coach = profile  # Associate the video with the current user's profile
            video.save()
            return redirect('/profile')  # Redirect to the profile view after saving
    else:
        profileform = ProfileForm(instance=profile)
        videoform = VideoForm()  # Do not pass instance here since we're adding new videos

    return render(request, 'profile.html', {'profileform': profileform, 'videoform': videoform})
