from django.db import models

# Create your models here.
class Documents(models.Model):
    doc = models.IntegerField()
    keyword = models.CharField(max_length=20)
    #weight = models.DecimalField(decimal_places=8, max_digits=10)
    weight = models.FloatField()
