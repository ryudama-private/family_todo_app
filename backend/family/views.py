import json

from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Family


@csrf_exempt
@require_POST
def register(request):
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "リクエストボディが不正です。"}, status=400)

    name = body.get("name", "").strip()
    password = body.get("password", "").strip()
    secret_question = body.get("secret_question", "").strip()
    secret_answer = body.get("secret_answer", "").strip()

    errors = {}
    if not name:
        errors["name"] = "必須項目です。"
    if not password:
        errors["password"] = "必須項目です。"
    if not secret_question:
        errors["secret_question"] = "必須項目です。"
    if not secret_answer:
        errors["secret_answer"] = "必須項目です。"

    if errors:
        return JsonResponse({"errors": errors}, status=400)

    family = Family.objects.create(
        name=name,
        password=make_password(password),
        secret_question=secret_question,
        secret_answer=secret_answer,
    )

    return JsonResponse(
        {
            "id": family.id,
            "name": family.name,
            "created_at": family.created_at.isoformat(),
            "updated_at": family.updated_at.isoformat(),
        },
        status=201,
    )
