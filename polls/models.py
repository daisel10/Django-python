from django.db import models

class Post(models.Model):
    # id 
    name = models.CharField(max_length=10, unique=True)
    gmail = models.EmailField()
    description = models.CharField(max_length=200)
