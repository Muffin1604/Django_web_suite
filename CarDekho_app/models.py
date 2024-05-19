from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User
# Create your models here.
class Showroomlist(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    website = models.URLField(max_length=100)

    def __str__(self):
        return self.name
    
class Carlist(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    chassisnumber = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    showroom = models.ForeignKey(Showroomlist, on_delete=models.CASCADE, related_name="Showrooms",null=True)
    def __str__(self):
        return self.name
    
class Review(models.Model):
    apiuser = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator,MaxValueValidator])
    comments = models.CharField(max_length=200, null=True)
    car = models.ForeignKey(Carlist, on_delete=models.CASCADE, related_name="Reviews", null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)
    def __str__(self):
        return "The rating of " + self.car.name +" is :--" + str(self.rating)

