from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import Center, Storage
from center.forms import CenterForm
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic


def center_list(request):
    centers = Center.objects.all()
    context = {
        'centers': centers
        }
    return render(request, 'center/center_list.html', context)


def center_detail(request, pk):
    center = Center.objects.get(pk=pk)
    context = {
        'center': center
    }
    return render(request, 'center/center_detail.html', context)

def create_center(request):
    if request.method == 'POST':
        form = CenterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('center:list'))
        
        return render(request, 'center/create_center.html', {'form': form})
    
    context = {
        'form': CenterForm()
    }
    return render(request, 'center/create_center.html', context)


def update_center(request, pk):
    center = Center.objects.get(pk=pk)
    if request.method == 'POST':
        form = CenterForm(request.POST, instance=center)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('center:detail', kwargs= {'pk': center.pk}))
        
        return render(request, 'center/update_center.html', {'form': form})
    
    context = {
        'form': CenterForm(instance=center)
    }
    return render(request, 'center/update_center.html', context)


def delete_center(request, pk):
    center = Center.objects.get(pk=pk)

    if request.method == 'POST':
        center.delete()
        return HttpResponseRedirect(reverse('center:list'))
    
    context = {
        'center': center
    }
    return render(request, 'center/delete_center.html', context)



class StorageList(generic.ListView):
    queryset = Storage.objects.all()
    template_name = 'storage/storage_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(center_id=self.kwargs['center_id'])
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['center_id'] = self.kwargs['center_id']
    #     return context


class StorageDetail(generic.DetailView):
    model = Storage
    template_name = 'storage/storage_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['available_quantity'] = (self.object.total_quantity - self.object.booked_quantity)
        return context
    