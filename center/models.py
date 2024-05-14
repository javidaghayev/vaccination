from django.db import models
from vaccin.models import Vaccine


class Center(models.Model):
    name = models.CharField(max_length=100)
    adress = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Storage(models.Model):
    center = models.ForeignKey(Center, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    total_quantity = models.IntegerField(default=0)
    booked_quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.center.name +' | ' + self.vaccine.name
    

