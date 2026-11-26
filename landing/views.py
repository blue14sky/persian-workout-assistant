import json
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .models import EarlyAccessSignup


def home(request):
    return render(request, "landing/index.html")


@require_POST
def signup(request):
    # Honeypot: silent response for obvious automated submissions.
    if request.POST.get("website"):
        return redirect("/#early-access")

    email = request.POST.get("email", "").strip().lower()
    consent = request.POST.get("consent") == "yes"
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError

    try:
        validate_email(email)
    except ValidationError:
        messages.error(request, "لطفاً یک ایمیل معتبر وارد کنید.")
        return redirect("/#early-access")

    if not consent:
        messages.error(request, "برای ثبت ایمیل، لطفاً با دریافت خبرهای نسخه آزمایشی موافقت کنید.")
        return redirect("/#early-access")

    try:
        EarlyAccessSignup.objects.get_or_create(email=email)
    except IntegrityError:
        pass

    messages.success(request, "ثبت شد! اگر نسخه آزمایشی آماده شود، به شما خبر می‌دهیم.")
    return redirect("/#early-access")


def manifest(request):
    return JsonResponse(
        {
            "id": "/",
            "name": "فیتو | دستیار برنامه تمرینی",
            "short_name": "فیتو",
            "lang": "fa",
            "dir": "rtl",
            "start_url": "/",
            "scope": "/",
            "display": "standalone",
            "background_color": "#0b1015",
            "theme_color": "#0b1015",
            "description": "برنامه مربی‌ات را به تجربه‌ای ساده‌تر در باشگاه تبدیل کن.",
            "icons": [
                {"src": "/static/landing/icon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any"},
                {"src": "/static/landing/icon-maskable.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "maskable"},
            ],
        },
        json_dumps_params={"ensure_ascii": False},
        content_type="application/manifest+json",
    )


def service_worker(request):
    source = Path(settings.BASE_DIR) / "landing" / "sw.js"
    response = HttpResponse(source.read_text(encoding="utf-8"), content_type="text/javascript; charset=utf-8")
    response["Cache-Control"] = "no-cache"
    response["Service-Worker-Allowed"] = "/"
    return response
