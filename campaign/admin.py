from django.contrib import admin
from .models import *


class SlotInline(admin.TabularInline):
    model = Slot
    readonly_fields = ['reserved']

class CustomCampaign(admin.ModelAdmin):
    inlines = [SlotInline]
    search_fields = ['center__name', 'vaccine__name']
    list_display = ['vaccine', 'center', 'start_date', 'end_date']
    ordering = ['start_date']
    fields = (
        ('vaccine'),
        ('center'),
        ('start_date', 'end_date'),
        ('agents')
    )


admin.site.register(Campaign, CustomCampaign)
