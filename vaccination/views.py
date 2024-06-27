from django.shortcuts import render
from django.views import generic
from vaccin.models import Vaccine
from campaign.models import Campaign, Slot
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from vaccination.forms import VaccinationForm
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from vaccination.models import Vaccination
from vaccination.utils import generate_pdf
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.urls import reverse




class ChooseVaccine(LoginRequiredMixin, generic.ListView):
    model = Vaccine
    template_name = 'vaccination/choose-vaccine.html'
    paginate_by = 3
    ordering = ['name']


class ChooseCampaign(LoginRequiredMixin, generic.ListView):
    model = Campaign
    template_name = 'vaccination/choose-campaign.html'
    paginate_by = 3
    ordering = ['start_date']

    def get_queryset(self):
        return super().get_queryset().filter(vaccine=self.kwargs['vaccine_id'])
    


class ChooseSlot(LoginRequiredMixin, generic.ListView):
    model = Slot
    template_name = 'vaccination/choose-slot.html'
    paginate_by = 3
    ordering = ['date']

    def get_queryset(self):
        return super().get_queryset().filter(campaign=self.kwargs['campaign_id'], date__gte=timezone.now())
    

class ConfirmVaccination(View):
    form_class = VaccinationForm

    def get(self, request, *args, **kwargs):
        campaign = Campaign.objects.get(pk=self.kwargs['campaign_id'])
        slot = Slot.objects.get(pk=self.kwargs['slot_id'])
        form = self.form_class(initial={
            'patient': request.user,
            'campaign': campaign,
            'slot': slot
        })

        context = {
            'patient': request.user,
            'campaign': campaign,
            'slot': slot,
            'form': form
        }
        return render(request, 'vaccination/confirm-vaccination.html', context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            is_reserved = Slot.reserve_vaccine(self.kwargs['campaign_id'], self.kwargs['slot_id'])
            if is_reserved:
                form.save()
                return HttpResponse('Your vaccination has been reserved')
            return HttpResponseBadRequest('Unable to reserve at this moment')
        return HttpResponseBadRequest('Invalid form data!')
    


class VaccinationList(LoginRequiredMixin, generic.ListView):
    model = Vaccination
    template_name = 'vaccination/vaccination-list.html'
    paginate_by = 2
    ordering = ['-id']



class VaccinationDetail(LoginRequiredMixin, generic.DetailView):
    model = Vaccination
    template_name = 'vaccination/vaccination-detail.html'



@login_required
def appointment_letter(request, vaccination_id):
    vaccination = Vaccination.objects.get(pk=vaccination_id)
    context = {
        'pdf_title': f"{vaccination.patient.get_full_name()} | Appointment Letter",
        'date': str(timezone.now()),
        'title': 'Appointment Letter',
        'subtitle': 'TO whom may concern',
        'content': f'This is to inform that the {vaccination.campaign.vaccine.name} vaccination of {vaccination.patient.get_full_name()} is scheduled {vaccination.slot.date}'
    }
    return generate_pdf(context)



@login_required
def vaccination_certificate(request, vaccination_id):
    vaccination = Vaccination.objects.get(pk=vaccination_id)
    if vaccination.is_vaccinated:
        context = {
            'pdf_title': f"{vaccination.patient.get_full_name()} | Vaccination Certificate",
            'date': str(timezone.now()),
            'title': 'Vaccination Certificate',
            'subtitle': 'TO whom may concern',
            'content': f'This is to certify that the {vaccination.patient.get_full_name()} has successfully {vaccination.campaign.vaccine.name} on {vaccination.date}. The vaccination was scheduled on {vaccination.campaign.center.name}'
        }
        return generate_pdf(context)
    return HttpResponseBadRequest('User is not vaccinated')



def approve_vaccination(request, vaccination_id):
    if request.user.has_perm('vaccination.change_vaccination'):
        try:
            vaccination = Vaccination.objects.get(pk=vaccination_id)
        except Vaccination.DoesNotExist:
            return HttpResponseBadRequest('Vaccination does not exist')
        if request.user in vaccination.campaign.agents.all():
            if vaccination.is_vaccinated:
                return HttpResponse('User already vaccinated')
            else:
                vaccination.is_vaccinated = True
                vaccination.date= timezone.now()
                vaccination.updated_by = request.user
                vaccination.save()
                return HttpResponseRedirect('vaccination:vaccination-detail', kwargs={'pk': vaccination_id})
        raise PermissionDenied()
    raise PermissionDenied()
