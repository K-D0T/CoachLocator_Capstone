from django.db import models

class Coaches(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    bio = models.TextField()
    zip_code = models.CharField(max_length=10)
    profile_pic = models.ImageField(upload_to='media/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Athlete(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    zip_code = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
	
 