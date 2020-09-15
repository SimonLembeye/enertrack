import datetime
from django.shortcuts import render
from pytz import timezone

from mysite import settings


def index(request):
    paris = timezone("Europe/Amsterdam")
    today = datetime.datetime.now(paris)

    print(today.year, today.month, today.hour)

    context = {'var': settings.STATIC_ROOT}
    return render(request, "enertrack/home.html", context)
