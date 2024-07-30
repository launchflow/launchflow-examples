import launchflow as lf
from django.http import HttpResponse


def index(request):
    return HttpResponse(f"Hello from {lf.environment}!")
