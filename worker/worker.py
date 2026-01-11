import os
import sys
import time
import django
import requests
from django.utils import timezone

# --- Force Python to see the project root ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kubewatch.settings")

django.setup()

from monitor.models import URL, CheckResult  # noqa


def check_url(url_obj: URL):
    try:
        start = time.time()
        response = requests.get(url_obj.address, timeout=5)
        elapsed = (time.time() - start) * 1000  # ms

        CheckResult.objects.create(
            url=url_obj,
            status_code=response.status_code,
            response_time_ms=elapsed,
            is_up=response.ok,
            checked_at=timezone.now()
        )

        print(f"OK {url_obj.address} {response.status_code} {elapsed:.1f}ms")

    except Exception as e:
        CheckResult.objects.create(
            url=url_obj,
            status_code=0,
            response_time_ms=0,
            is_up=False,
            checked_at=timezone.now()
        )
        print(f"FAIL {url_obj.address} {e}")


def run_worker(interval_seconds=30):
    while True:
        urls = URL.objects.all()
        if not urls:
            print("No URLs to check yet… add some in /admin")
        for u in urls:
            check_url(u)

        print(f"Sleeping {interval_seconds}s…")
        time.sleep(interval_seconds)


if __name__ == "__main__":
    run_worker()
