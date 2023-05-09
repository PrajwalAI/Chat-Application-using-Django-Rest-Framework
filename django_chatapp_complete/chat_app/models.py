from django.db import models
#import uuid
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='name')
    message  = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    #id = models.IntegerField(primary_key=True, Read_only=True)

    class Meta:
        ordering = ('-timestamp',)



