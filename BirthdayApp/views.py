import hmac
import json
from pathlib import Path

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .models import Photo

MAX_TRIES, WINDOW = 8, 600  # 8 wrong tries per IP per 10 minutes
INDEX_FILE = Path(__file__).resolve().parent / "templates" / "index.html"


@require_GET
def home(request):
    """Serve the birthday page as-is (no Django template processing)."""
    html = INDEX_FILE.read_text(encoding="utf-8")
    if not settings.DEBUG:
        html = html.replace("allowTest: true", "allowTest: false")
    response = HttpResponse(html)
    response["Cache-Control"] = "no-store"
    return response


def favicon(request):
    return HttpResponse(status=204)


def _client_ip(request):
    fwd = request.META.get("HTTP_X_FORWARDED_FOR")
    return fwd.split(",")[0].strip() if fwd else request.META.get("REMOTE_ADDR", "")


@csrf_exempt
@require_POST
def unlock(request):
    key = f"unlock:{_client_ip(request)}"
    tries = cache.get(key, 0)
    if tries >= MAX_TRIES:
        return JsonResponse({"detail": "too many attempts"}, status=429)

    try:
        supplied = str(json.loads(request.body or b"{}").get("password", ""))
    except (ValueError, AttributeError):
        return JsonResponse({"detail": "bad request"}, status=400)

    expected = settings.BIRTHDAY_PASSWORD
    ok = hmac.compare_digest(
        supplied.strip().lower().encode(), expected.strip().lower().encode()
    )
    if not ok:
        cache.set(key, tries + 1, WINDOW)
        return JsonResponse({"detail": "wrong password"}, status=403)

    cache.delete(key)
    photos = [
        {
            "url": request.build_absolute_uri(p.image.url),
            "caption": p.caption,
            "date": p.date_text,
        }
        for p in Photo.objects.all()
    ]
    return JsonResponse({"photos": photos})