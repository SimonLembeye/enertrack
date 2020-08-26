from django.contrib import admin

# Register your models here.
from enertrack.models import Country, InstalledCapacity

admin.site.register(Country)
admin.site.register(InstalledCapacity)
