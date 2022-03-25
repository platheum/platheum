from re import M
from statistics import mode
from django.db import models

# Create your models here.
class Node(models.Model):
    ip = models.GenericIPAddressField()