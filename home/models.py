from django.db import models
from django.contrib.auth.models import User

class Coaches(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=False)
    price_thirty = models.IntegerField(null=True, blank=True)
    price_hour = models.IntegerField(null=True, blank=True)
    # chose between coed or allgirl 
    coed = 'Coed'
    allgirl = 'All-Girl'
    COED_ALLGIRL_CHOICES = [
        (coed, 'Coed'),
        (allgirl, 'All-Girl'),
    ]
    coed_allgirl = models.CharField(
        max_length=10,
        choices=COED_ALLGIRL_CHOICES,
        default=coed,
    )
    yes = 'Yes'
    no = 'No'
    TUMBLING_CHOICES = [
        (yes, 'yes'),
        (no, 'no'),
    ]
    coach_tumbling = models.CharField(
        max_length=10,
        choices=TUMBLING_CHOICES,
        default=no,
    )
    
    zip_code = models.CharField(max_length=10)
    profile_pic = models.ImageField(upload_to='media/', blank=True, null=True)
    bio = models.TextField()

    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Video(models.Model):
    coach = models.ForeignKey(Coaches, related_name='videos', on_delete=models.CASCADE)
    video = models.CharField(max_length=10000, null=True, blank=True, verbose_name="Link to Instagram Reel")


class Athlete(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    zip_code = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
	
 