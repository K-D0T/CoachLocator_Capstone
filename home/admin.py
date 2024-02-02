from django.contrib import admin
from .models import Athlete, Coaches, Video

admin.site.register(Athlete)
admin.site.register(Video)
admin.site.register(Coaches)

