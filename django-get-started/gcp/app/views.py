from django.http import HttpResponse
from app.infra import bucket

def get_name(request):
    name = request.GET.get('name', '')
    if not name:
        return HttpResponse("Please provide a name")
    try:
        name_bytes = bucket.download_file(f"{name}.txt")
        return HttpResponse(name_bytes.decode("utf-8"))
    except:
        return HttpResponse(f"{name} was not found")

def post_name(request):
    name = request.POST.get('name', '')
    if name:
        bucket.upload_from_string(name, f"{name}.txt")
        return HttpResponse("ok")
    return HttpResponse("Please provide a name", status=400)
