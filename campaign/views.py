from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from campaign.models import Campaign, Slot
from campaign.forms import CampaignForm, SlotForm
from vaccination.models import Vaccination
from django.urls import reverse, reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin


class CampaignViewList(LoginRequiredMixin, generic.ListView):
    model = Campaign
    template_name = 'campaign/campaign_list.html'
    paginate_by = 2
    ordering = ['-id']



class CampaignDetailView(LoginRequiredMixin, generic.DetailView):
    model = Campaign
    template_name = 'campaign/campaign_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registrations'] = Vaccination.objects.filter(campaign = self.kwargs['pk']).count()
        return context



class CampaignCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Campaign
    form_class = CampaignForm
    template_name = 'campaign/campaign_create.html'
    permission_required = ('campaign.add_campaign')
    success_url = reverse_lazy('campaign:campaign-list')
    
    # def get_success_url(self):
    #     return reverse('campaign:campaign-list')
    


class CampaignUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Campaign
    form_class = CampaignForm
    template_name = 'campaign/campaign_update.html'
    permission_required = ('campaign.change_campaign')
    success_url = reverse_lazy('campaign:campaign-list')

    # def get_success_url(self):
    #     return reverse('campaign:campaign-list')
    


class CampaignDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Campaign
    template_name = 'campaign/campaign_delete.html'
    permission_required = ('campaign.delete_campaign')
    success_url = reverse_lazy('campaign:campaign-list')

    # def get_success_url(self):
    #     return reverse('campaign:campaign-list')
    


#Slot
class SlotListView(LoginRequiredMixin, generic.ListView):
    # queryset = Slot.objects.all()
    model = Slot
    template_name = 'slot/slot-list.html'
    ordering = ['-id']
    paginate_by = 2

    def get_queryset(self):
        # return super().get_queryset().filter(campaign_id=self.kwargs['campaign_id'])
        queryset = Slot.objects.filter(campaign = self.kwargs['campaign_id']).order_by('-id')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campaign_id'] = self.kwargs['campaign_id']
        return context
    


class SlotDetailView(LoginRequiredMixin, generic.DetailView):
    model = Slot
    template_name = 'slot/slot-detail.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context
    


class SlotCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Slot
    form_class = SlotForm
    template_name = 'slot/slot-create.html'
    success_message = "Slot created successfully"
    permission_required = ('campaign.add_slot',)

    def get_form_kwargs(self): #diger secimleri yigisdirdi
        kwargs = super().get_form_kwargs()
        kwargs['campaign_id'] = self.kwargs['campaign_id']
        return kwargs
    
    def get_initial(self): # secilmis campaign secilmis gelir
        initial = super().get_initial()
        initial['campaign'] = Campaign.objects.get(id=self.kwargs['campaign_id'])
        return initial
    
    def get_success_url(self):
        return reverse_lazy('campaign:slot-list', kwargs= {'campaign_id': self.kwargs['campaign_id']})
    


class SlotUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Slot
    form_class = SlotForm
    template_name = 'slot/slot-update.html'
    success_message = "Slot updated successfully"
    permission_required = ('campaign.change_slot',)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['campaign_id'] = self.get_object().campaign.id
        return kwargs
    
    def get_success_url(self):
        return reverse_lazy('campaign:slot-list', kwargs={'campaign_id': self.get_object().campaign.id})
    


class SlotDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = Slot
    template_name = 'slot/slot-delete.html'
    success_message = "Slot deleted successfully"
    permission_required = ('campaign.delete_slot',)

    def get_success_url(self):
        return reverse_lazy('campaign:slot-list', kwargs={'campaign_id': self.get_object().campaign.id})