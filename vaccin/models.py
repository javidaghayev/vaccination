from django.db import models

# Create your models here.

class Vaccine(models.Model):
    name = models.CharField('Vaccine name ', max_length=100)
    description = models.TextField()
    number_of_dose = models.IntegerField(default=1)
    interval = models.IntegerField(default=0, help_text='Please provide the interval')
    storage_temprature = models.IntegerField(null=True, blank=True, help_text='Please provide temprature ')
    minimum_age = models.IntegerField(default=0)

    def __str__(self):
        return self.name