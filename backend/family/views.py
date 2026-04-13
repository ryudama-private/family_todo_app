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
    
    if not isinstance(body, dict):
        return JsonResponse({"error": "JSONオブジェクトを指定してください。"}, status=400)
    
    fields = {
        "name": body.get("name"),
        "password": body.get("password"),
        "secret_question": body.get("secret_question"),
        "secret_answer": body.get("secret_answer"),
    }

    errors = {}
    for field, value in fields.items():
        if not isinstance(value, str):
            errors[field] = "文字列で指定してください。"
        elif not value.strip():
            errors[field] = "必須項目です。"

    if errors:
        return JsonResponse({"errors": errors}, status=400)

    name = fields["name"].strip()
    password = fields["password"].strip()
    secret_question = fields["secret_question"].strip()
    secret_answer = fields["secret_answer"].strip()

    family = Family.objects.create(
        name=name,
        password=make_password(password),
        secret_question=secret_question,
        secret_answer=make_password(secret_answer),
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
