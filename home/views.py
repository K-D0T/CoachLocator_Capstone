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
from PIL import Image, ImageOps
from io import BytesIO
from django.core.files.base import ContentFile
import requests
from django.core.mail import send_mail

def calculate_distance(zip_code, coach):
    dist = pgeocode.GeoDistance('us')
    distance = dist.query_postal_code(zip_code, coach.zip_code) * 0.621371
    return distance

def get_coaches_with_distance(zip_code):
    coaches = Coaches.objects.all()

    # find coaches with profile filled out 
    coaches = [coach for coach in coaches if coach.profile_pic]

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
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
                return render(request, 'register.html')
            # Check if the email is already in use
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already in use.')
                return render(request, 'register.html')
            else:
                # Hash the password
                hashed_password = make_password(password)
                
                # Create and save the user
                user = User(username=username, email=email, password=hashed_password)
                user.save()

                # Send an email notification
                send_mail(
                    'New user registration',
                    f'A new user has registered with the username: {username}',
                    'kaiden.thrailkill@gmail.com',  # Replace with your email
                    ['kaiden.thrailkill@gmail.com'],  # Replace with your email
                    fail_silently=False,
                )
                
                # Log the user in
                login(request, user)

                # Redirect to a success page or login page
                return HttpResponseRedirect(reverse('home:profile'))
        else:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html')
    else:
        # Render the signup form template
        return render(request, 'register.html')
    

    
def user_login(request):
    if request.method == 'POST':
        # Retrieve username/email and password from request
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        # Try to find a user that matches either the username or email
        user = authenticate(username=username_or_email, password=password)
        if user is None:
            try:
                user_obj = User.objects.filter(email=username_or_email).first()
                if user_obj:
                    user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass

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
            image = Image.open(profileform.cleaned_data['profile_pic'])

            image = ImageOps.exif_transpose(image)  # Rotate the image correctly

            image = image.resize((150, 150), Image.LANCZOS)

            # Convert the Image object to a file-like object
            image_io = BytesIO()
            image.save(image_io, format='JPEG')
            image_file = ContentFile(image_io.getvalue(), name=profileform.cleaned_data['profile_pic'].name)

            profile.profile_pic.save(image_file.name, image_file, save=False)
            profile.save()
            messages.success(request, "Successfully Updated Profile")
            # Only redirect if BOTH forms are not valid, else stay on the page to process the second form
            if not videoform.is_valid():
                return redirect('/profile')  # Redirect to the profile view after saving

        # Check if videoform is valid in a separate condition to allow for video addition without profile edit
        if videoform.is_valid():
            try:
                instaurl = videoform.cleaned_data['video']
                response = requests.get(f"https://iframe.ly/api/oembed?url={instaurl}&api_key=f68b29ec833a23d0d81c6c")
                data = response.json()
                html = data['html']
                video = videoform.save(commit=False)
                video.video = html  # Assign the html to the video field of the video instance
                video.coach = profile  # Associate the video with the current user's profile
                video.save()
                messages.success(request, "Successfully Updated Profile")
            except Exception as e:
                print(f"Failed to add video: {e}")
            return redirect('/profile')  # Redirect to the profile view after saving  # Redirect to the profile view after saving  # Redirect to the profile view after saving
    else:
        profileform = ProfileForm(instance=profile)
        videoform = VideoForm()  # Do not pass instance here since we're adding new videos

    return render(request, 'profile.html', {'profileform': profileform, 'videoform': videoform})
