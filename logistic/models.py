from django.db import models

# Create your models here.
class Scrips(models.Model):
    scipt_types = (('N', 'NSE'),('B', 'BSE'))
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    script_type = models.CharField(max_length=1, choices=scipt_types)