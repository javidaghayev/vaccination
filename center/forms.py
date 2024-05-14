from django.forms import ModelForm
from center.models import Center


class CenterForm(ModelForm):
    class Meta:
        model = Center
        fields = '__all__'
