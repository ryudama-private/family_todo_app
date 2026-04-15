import json

from django.conf import settings
from django.utils.crypto import constant_time_compare
from django.contrib.auth.hashers import check_password, make_password
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods

from .models import Family


def _parse_json_body(request):
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return None, JsonResponse({"error": "リクエストボディが不正です。"}, status=400)

    if not isinstance(body, dict):
        return None, JsonResponse({"error": "JSONオブジェクトを指定してください。"}, status=400)

    return body, None


def _validate_and_strip_fields(body, field_names):
    fields = {field_name: body.get(field_name) for field_name in field_names}

    errors = {}
    for field, value in fields.items():
        if not isinstance(value, str):
            errors[field] = "文字列で指定してください。"
        elif not value.strip():
            errors[field] = "必須項目です。"

    if errors:
        return None, JsonResponse({"errors": errors}, status=400)

    normalized_fields = {field: value.strip() for field, value in fields.items()}
    return normalized_fields, None


@csrf_exempt
@require_POST
def register(request):
    body, error_response = _parse_json_body(request)
    if error_response:
        return error_response

    fields, error_response = _validate_and_strip_fields(
        body,
        ["name", "password", "secret_question", "secret_answer"],
    )
    if error_response:
        return error_response

    name = fields["name"]
    password = fields["password"]
    secret_question = fields["secret_question"]
    secret_answer = fields["secret_answer"]

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


@csrf_exempt
@require_POST
def login(request):
    body, error_response = _parse_json_body(request)
    if error_response:
        return error_response

    fields, error_response = _validate_and_strip_fields(body, ["name", "password"])
    if error_response:
        return error_response

    name = fields["name"]
    password = fields["password"]

    try:
        family = Family.objects.get(name=name)
    except Family.DoesNotExist:
        return JsonResponse({"error": "名前またはパスワードが違います。"}, status=401)

    if not check_password(password, family.password):
        return JsonResponse({"error": "名前またはパスワードが違います。"}, status=401)

    return JsonResponse(
        {
            "id": family.id,
            "name": family.name,
        },
        status=200,
    )


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_family_for_e2e(request, family_id):
    if not settings.DEBUG:
        return JsonResponse({"error": "この機能は開発環境でのみ利用できます。"}, status=403)

    if not getattr(settings, "E2E_CLEANUP_ENABLED", False):
        return JsonResponse({"error": "cleanup機能が無効です。"}, status=403)

    expected_token = getattr(settings, "E2E_CLEANUP_TOKEN", "")
    if not expected_token:
        return JsonResponse({"error": "cleanupトークンが未設定です。"}, status=503)

    provided_token = request.headers.get("X-E2E-Cleanup-Token", "")
    if not constant_time_compare(provided_token, expected_token):
        return JsonResponse({"error": "cleanupトークンが不正です。"}, status=403)

    family = get_object_or_404(Family, id=family_id)
    family.delete()
    return JsonResponse({"deleted_id": family_id}, status=200)
