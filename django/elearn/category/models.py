from django.db import models

class Cateogries(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500)

# Create your models here.
