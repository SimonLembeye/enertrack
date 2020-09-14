import datetime
from django.shortcuts import render
from pytz import timezone


def index(request):
    paris = timezone("Europe/Amsterdam")
    today = datetime.datetime.now(paris)

    print(today.year, today.month, today.hour)

    context = {}
    return render(request, "enertrack/home.html", context)
