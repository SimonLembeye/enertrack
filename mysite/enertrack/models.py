from django.db import models


PRODUCTION_TYPE_CHOICES = (
    ("FOSSIL_GAS", "gas"),
    ("FOSSIL_HARD_COAL", "coal"),
    ("HYDRO_PUMPED_STORAGE", "hydro_pumped_storage"),
    ("NUCLEAR", "nuclear"),
    ("SOLAR", "solar"),
    ("WIND_OFFSHORE", "wind_offshore"),
    ("WIND_ONSHORE", "wind_onshore"),
)


class Country(models.Model):
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name_plural = "Countries"


class InstalledCapacity(models.Model):
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE
    )
    value = models.IntegerField(help_text="expressed in kW")
    date = models.DateField(auto_now=False)
    production_type = models.CharField(
        max_length=50, choices=PRODUCTION_TYPE_CHOICES, default="SOLAR"
    )

    def __str__(self):
        return f"{self.country.code} - {self.date} - {self.production_type}"

    class Meta:
        verbose_name_plural = "InstalledCapacities"
