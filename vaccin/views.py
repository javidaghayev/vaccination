from django.shortcuts import render
from django.views import View
from vaccin.models import Vaccine
from vaccin.forms import VaccineForm
# from django.http import HttpResponseRedirect, Http404
# from django.urls import reverse


class VaccineList(View):
    def get(self, request):
        vaccine_list = Vaccine.objects.all()
        context = {
            'vaccine_list': vaccine_list
        }
        return render(request, 'vaccine/vaccine_list.html', context)
    

class VaccineDetail(View):
    def get(self, request, pk):
        vaccine_detail = Vaccine.objects.get(pk=pk)
        context = {
            'vaccine_detail': vaccine_detail
        }
        return render(request, 'vaccine/vaccine_detail.html', context)
    

class VaccineCreate(View):
    form_class = VaccineForm
    template_name = 'vaccine/create_vaccine.html'

    def get(self, request):
        context = {
            'form': self.form_class
        }
        return render(request, self.template_name, context)
