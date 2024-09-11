from django.http import HttpResponse
import launchflow as lf

def index(request):
    return HttpResponse(f"Hello from {lf.project}/{lf.environment}")
