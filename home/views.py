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
            coaches = Coaches.objects.filter(zip_code=zip_code)
            
            return render(request, 'nearme.html', {'coaches': coaches})
    else:
        form = ZipSearchForm()
    return render(request, 'nearme.html', {'form': form})


'''
def nearme(request):
    # Get all Coach objects from the database
    coaches = list(Coaches.objects.values())
    context = {
        'coaches': coaches,
    }

    return render(request, 'nearme.html', context)
'''