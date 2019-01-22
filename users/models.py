from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

# Create your models here.
class CustomUser(AbstractUser):
    zip_code = models.CharField( max_length=5, blank = False)
    avatar = models.ImageField(upload_to = 'avatar/',  default = 'pic_folder/None/no-img.jpg')

    def __str__(self) -> str:
        return self.username

    def get_absolute_url(self):
        return reverse('profile', args =[str(self.id)])
