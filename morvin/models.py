from django.db import models
from django.utils.text import slugify
from datetime import datetime
from django.http import HttpResponseNotAllowed




# Create your models here.

CUSTODY = (
        ('Jinja Rd Police', 'Jinja Rd Police'), 
        ('Rubaga Div Police', 'Rubaga Div Police'),
        ('Kiira Rd Police', 'Kiira Rd Police'),
        ('Wandegeya div Police', 'Wandegeya div Police'),
        )
class CrimeModel(models.Model):
    # fields of the model
    
    name = models.CharField(max_length=50)
    crime_type = models.TextField()
    license = models.TextField(max_length=8, blank= True)
    occupation = models.TextField(blank= True)
    stage = models.TextField(null=True, blank=True)
    telephone = models.TextField(max_length=10)
    datetime = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    custody = models.CharField(max_length=200, null=True, choices=CUSTODY, default='Kiira Rd Police')
    # renames the instances of the model
    # with their title name

    class Meta:
        db_table = "morvin_crimemodel"
        ordering = ['id'] 

    def __str__(self):
        return self.name 