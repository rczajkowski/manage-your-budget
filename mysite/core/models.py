from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.name

class Finance(models.Model):
    pub_date = models.DateTimeField()
    title = models.CharField(max_length=20)
    value = models.FloatField(null=False, default=0)
    category = models.ForeignKey(Category)
    user = models.ForeignKey(User, default=1)