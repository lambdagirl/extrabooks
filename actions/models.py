from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.
class Action(models.Model):
    user = models.ForeignKey(get_user_model(),
                            related_name='action',
                            db_index=True,
                            on_delete=models.CASCADE)
    #the verb describing the action that user has performed.
    verb = models.CharField(max_length=255)
    #target_ct, is a ForeignKey points to the ContentType.
    target_ct = models.ForeignKey(ContentType,
                                blank = True,
                                null = True,
                                related_name='target_object',
                                on_delete=models.CASCADE)
    #target_id A PositiveIntegerField for storing the primary key of the related object
    target_id = models.PositiveIntegerField(null = True,
                                            blank = True,
                                            db_index = True)
    #target, a GenericForeignKey field to the related object based on the combination of the two previous fields.
    target = GenericForeignKey('target_ct','target_id')
    created = models.DateTimeField(auto_now_add = True, db_index = True)
    class Meta:
        ordering = ('-created',)
