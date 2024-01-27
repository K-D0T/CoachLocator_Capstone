from django.shortcuts import render
import requests
from django.http import HttpResponseRedirect
from django.urls import reverse
from home.models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from .forms import ZipSearchForm
import pgeocode
import os
from django.shortcuts import render, get_object_or_404, redirect

def home(request):


    context = {

    }
    return render(request, 'index.html', context)


def nearme(request):
    if request.method == "POST":
        form = ZipSearchForm(request.POST)
        if form.is_valid():
            zip_code = form.cleaned_data['zip_code']
            # get all coaches objects
            coaches = Coaches.objects.all()
            dist = pgeocode.GeoDistance('us')
            coaches_with_distance = []
            for coach in coaches:
                distance = dist.query_postal_code(zip_code, coach.zip_code) * 0.621371
                coaches_with_distance.append((coach, distance))

            # Sort the list of tuples based on distance
            coaches_with_distance.sort(key=lambda x: x[1])
            

            
            
            return render(request, 'nearme.html', {'coaches_with_distance': coaches_with_distance})
    else:
        form = ZipSearchForm()
    return render(request, 'nearme.html', {'form': form})
