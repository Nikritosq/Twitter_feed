import random
from django.db import models

class Post(models.Model):
    # id = models.AutoField(primary_key=True)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)

def serialize(self):
    return {
        "id": self.id,
        "content": self.content,
        "likes": 0,
        "reposts": 0,
    }