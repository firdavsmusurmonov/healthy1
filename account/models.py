from email.mime import image
from pyexpat import model
from typing_extensions import Self
from unicodedata import category
from django.db import models


from django.contrib.auth.models import AbstractUser
from doctor.utils import generate_unique_slug

def get_avatar(instance, filename):
    return "users/%s" % (filename)

def get_image(instance, filename):
    return "users/%s" % (filename)

def get_profession(instance, filename):
    return "profession/%s" % (filename)


class Profession(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=get_profession, default='users/default.png')
    def __str__(self):
        return self.name
        
class Region(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', related_name="childs", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Customuser(AbstractUser):
    GENDER_CHOICES = (
        ('man', 'Man'),
        ('woman', 'Woman')
    )
    fullname = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    smscode = models.IntegerField(default=0)
    complete = models.IntegerField(default=0)
    phone = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to=get_avatar, default='users/default.png')
    gender = models.CharField(choices=GENDER_CHOICES, max_length=50, null=True, blank=True)
    birth_date = models.DateField(default=None, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    langtude = models.FloatField(default=0)
    latitude = models.FloatField(default=0)
    profession = models.ForeignKey(Profession, null=True, blank=True, on_delete=models.SET_NULL)
    region = models.ForeignKey(Region, related_name="user_region", null=True,blank=True,on_delete=models.CASCADE)
    city = models.ForeignKey(Region,related_name="user_city",null=True,blank=True,on_delete=models.CASCADE)


class Review(models.Model):
    start = models.IntegerField(default=0)
    user = models.ForeignKey(Customuser, related_name="review_user", null=True, blank=True, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Customuser, related_name="review_doctor", null=True, blank=True, on_delete=models.CASCADE)
    profession = models.ForeignKey(Profession, related_name="review_profession", null=True, blank=True, on_delete=models.CASCADE)
    text = models.CharField(max_length=512)

    
    def __str__(self):
        return str(self.doctor)

class Drug(models.Model):
    name = models.CharField(default="",max_length=255,null=True,blank=True)
    image = models.ImageField(upload_to=get_image, default='users/default.png')
    def __str__(self):
        return str(self.name)

class Disease(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    drugs = models.ManyToManyField(Drug, related_name='drugs')
    def __str__(self):
        return str(self.name)
        
class Diagnos(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField(default="",null=True,blank=True)
    disease = models.ManyToManyField(Disease, related_name='disease')
    def __str__(self):
        return str(self.name)

class Category(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    slug = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to=get_profession, default='users/default.png')
    profession = models.ForeignKey(Profession, null=True, blank=True, on_delete=models.SET_NULL)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            if len(self.name) > 0:
                self.slug = generate_unique_slug(self, 'name')
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    # drugs = models.ManyToManyField(Drug, related_name='drugs')
    # diagnos = models.ForeignKey(Diagnos, related_name='diagnos',null=True, blank=True, on_delete=models.SET_NULL)