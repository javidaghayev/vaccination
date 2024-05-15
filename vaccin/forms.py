from django.forms import ModelForm
from vaccin.models import Vaccine


class VaccineForm(ModelForm):
    class Meta:
        model = Vaccine
        fields = '__all__'
