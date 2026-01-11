from django.http import JsonResponse
from .models import URL, CheckResult


def health(request):
    return JsonResponse({"status": "ok"})


def urls_list(request):
    data = list(URL.objects.values("id", "name", "address", "created_at"))
    return JsonResponse({"urls": data})


def results_list(request):
    data = list(CheckResult.objects.order_by("-checked_at")[:50].values())
    return JsonResponse({"results": data})
