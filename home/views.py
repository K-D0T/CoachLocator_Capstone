from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from home.models import Coaches
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .forms import ZipSearchForm, CoachForm
import pgeocode

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
