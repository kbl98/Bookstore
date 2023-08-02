from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    pass

    author_pseudonym=models.CharField(max_length=30,default="")

    def __str__(self):
        return self.username
    

class Book(models.Model):
    title=models.CharField(max_length=150)
    description=models.CharField(max_length=350)
    author=models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=False)
    cover=models.ImageField(upload_to = 'media', max_length=100,blank=True,null=True)
    price=models.DecimalField(max_digits=15, decimal_places=2,)
    

