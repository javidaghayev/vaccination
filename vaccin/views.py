from django.shortcuts import render, get_object_or_404
from django.views import View
from vaccin.models import Vaccine
from vaccin.forms import VaccineForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator 


@method_decorator(login_required, name='dispatch')
class VaccineList(View):
    def get(self, request):
        vaccine_list = Vaccine.objects.all().order_by('-id')
        paginator = Paginator(vaccine_list, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'page_obj': page_obj
            }
        return render(request, 'vaccine/vaccine_list.html', context)
    
@method_decorator(login_required, name='dispatch')
class VaccineDetail(View):
    def get(self, request, pk):
        vaccine_detail = Vaccine.objects.get(pk=pk)
        context = {
            'vaccine_detail': vaccine_detail
        }
        return render(request, 'vaccine/vaccine_detail.html', context)
    
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('vaccin.add_vaccine', raise_exception=True), name='dispatch')
class VaccineCreate(View):
    form_class = VaccineForm
    template_name = 'vaccine/create_vaccine.html'

    def get(self, request):
        context = {
            'form': self.form_class
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('vaccin:list'))
        return render(request, self.template_name, {'form': form})
    
        
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('vaccin.change_vaccine', raise_exception=True), name='dispatch')
class UpdateVaccine(View):
    form_class = VaccineForm
    template_name = 'vaccine/update_vaccine.html'

    def get(self, request, pk):
        vaccine = get_object_or_404(Vaccine, pk=pk)
        context = {
            'form': self.form_class(instance=vaccine)
        }
        return render(request, self.template_name, context)
    
    def post(self, request, pk):
        vaccine = get_object_or_404(Vaccine, pk=pk)
        form = self.form_class(request.POST, instance=vaccine)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('vaccin:detail', kwargs={'pk': vaccine.pk}))
        return render(request, self.template_name, {'form': form})
        
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('vaccin.delete_vaccine', raise_exception=True), name='dispatch')
class VaccineDelete(View):
    template_name = 'vaccine/delete_vaccine.html'

    def get(self, request, pk):
        vaccine = get_object_or_404(Vaccine, pk=pk)
        context = {
            'vaccine': vaccine
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        get_object_or_404(Vaccine, pk=pk).delete()
        return HttpResponseRedirect(reverse('vaccin:list'))
    