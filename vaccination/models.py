from django.db import models
from campaign.models import Campaign, Slot
from django.contrib.auth.models import User


class Vaccination(models.Model):
    patient = models.ForeignKey(User, related_name='patient', on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    is_vaccinated = models.BooleanField(default=False)
    updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.patient.get_full_name() + ' | ' + str(self.campaign.vaccine.name)