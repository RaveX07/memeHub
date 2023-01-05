from django.db import models

# Create your models here.
class Post(models.Model):
    content = models.TextField(max_length=240, blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    likes = models.IntegerField(default=0, editable=False)