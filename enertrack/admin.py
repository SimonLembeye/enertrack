from django.contrib import admin

# Register your models here.
from enertrack.models import Country, InstalledCapacity, Forecast, Measure


class ForecastAdmin(admin.ModelAdmin):
    list_display = (
        "forecast_production_type",
        "type",
        "value",
        "start_date",
        "updated_date",
    )


class MeasureAdmin(admin.ModelAdmin):
    list_display = ("production_type", "value", "start_date", "updated_date")


admin.site.register(Country)
admin.site.register(InstalledCapacity)
admin.site.register(Forecast, ForecastAdmin)
admin.site.register(Measure, MeasureAdmin)
