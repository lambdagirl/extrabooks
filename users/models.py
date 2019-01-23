from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.text import slugify
import uuid, os

# Create your models here.


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    # return the whole path to the file
    return os.path.join(str(instance.id), "avatar", filename)

class CustomUser(AbstractUser):
    zip_code = models.CharField( max_length=5, blank = False)
    avatar = models.ImageField(upload_to = user_directory_path,
                                verbose_name= 'profile_pic',
                                default = 'None/no-img.jpg')

    def __str__(self) -> str:
        return self.username

    def get_absolute_url(self):
        return reverse('profile', args =[str(self.id)])


'''    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super(CustomUser, self).save(*args, **kwargs)
'''
