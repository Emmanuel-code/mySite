from django.db import models

# Create your models here.


class About(models.Model):
    content=models.TextField()

    def __str__(self):
        return self.content


class Profile1(models.Model):
    first_name=models.CharField(max_length=160)
    last_name=models.CharField(max_length=160)
    date_of_birth = models.DateField(blank=True, null=True)
    email=models.EmailField(max_length=160)
    phone=models.IntegerField(blank=True)
    about_me=models.TextField()
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.first_name
