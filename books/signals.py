from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.auth.signals import user_logged_in
from .models import BookImage
THUMNBAIL_SIZE = (300,300)

@receiver(pre_save, sender=BookImage)
def generate_thumbnail(sender, instance, **kwargs):
    im = Image.open(instance.image)
    im = im.convert("RGB")
    im.thumbnail(THUMNBAIL_SIZE, Image.ANTIALIAS)
    temp_thumb = BytesIO()
    im.save(temp_thumb,"JPEG")
    temp_thumb.seek(0)

    # set save=False, otherwise it will run in an infinite loop
    instance.thumbnail.save(
        instance.image.name,
        ContentFile(temp_thumb.read()),
        save=False,
    )
    temp_thumb.close()
