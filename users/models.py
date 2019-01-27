from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.text import slugify
import uuid, os

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
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super(CustomUser, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.username

    def get_absolute_url(self):
        return reverse('profile', args =[str(self.slug)])


class Contact(models.Model):
	from_user = models.ForeignKey(CustomUser, on_delete = models.CASCADE, related_name="from_user")
	to_user = models.ForeignKey(CustomUser, on_delete = models.CASCADE, related_name="to_user")

CustomUser.add_to_class(
    'following',
    models.ManyToManyField(
        'self',
        through=Contact,
        related_name='followers',
        symmetrical=False))
