from django.contrib import admin
from .models import *



class StorageInline(admin.TabularInline):
    model = Storage


class CustomCenter(admin.ModelAdmin):
    inlines = [StorageInline]
    # search_fields = []


admin.site.register(Center, CustomCenter)


