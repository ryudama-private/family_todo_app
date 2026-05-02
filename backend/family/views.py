import json
from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.crypto import constant_time_compare
from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from .models import Task, Family

@csrf_exempt
@require_http_methods(['PATCH'])
def update_task_title(request, task_id):
    try:
        data = json.loads(request.body)
    except Exception:
        return JsonResponse({'error': 'JSONが不正です'}, status=400)
    title = data.get('title')
    if not isinstance(title, str) or not title.strip():
        return JsonResponse({'error': 'titleは必須です'}, status=400)
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({'error': '指定されたタスクが存在しません'}, status=404)
    task.title = title.strip()
    task.save()
    return JsonResponse({'title': task.title}, status=200)

@csrf_exempt
@require_http_methods(['POST'])
def create_task(request):
    try:
        data = json.loads(request.body)
    except Exception:
        return JsonResponse({'error': 'JSONが不正です'}, status=400)
    required_fields = ['title', 'creator_id', 'assignee_id', 'status']
    for field in required_fields:
        if not data.get(field):
            return JsonResponse({'error': f'{field}は必須です'}, status=400)
    try:
        creator = Family.objects.get(id=data['creator_id'])
        assignee = Family.objects.get(id=data['assignee_id'])
    except Family.DoesNotExist:
        return JsonResponse({'error': 'creator_idまたはassignee_idが不正です'}, status=400)
    due_date = None
    if 'due_date' in data and data['due_date']:
        due_date = parse_datetime(data['due_date'])
        if due_date is None:
            return JsonResponse({'error': 'due_dateの形式が不正です'}, status=400)
    alarm_minutes = data.get('alarm_minutes')
    if alarm_minutes == '':
        alarm_minutes = None
    task = Task.objects.create(
        title=data['title'],
        creator=creator,
        assignee=assignee,
        due_date=due_date,
        status=data['status'],
        alarm_minutes=alarm_minutes
    )
    return JsonResponse({
        'id': task.id,
        'title': task.title,
        'creator_id': task.creator.id,
        'assignee_id': task.assignee.id,
        'due_date': task.due_date,
        'status': task.status,
        'alarm_minutes': task.alarm_minutes,
        'created_at': task.created_at,
        'updated_at': task.updated_at,
    }, status=201)

def _parse_json_body(request):
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return None, JsonResponse({'error': 'リクエストボディが不正です。'}, status=400)
    if not isinstance(body, dict):
        return None, JsonResponse({'error': 'JSONオブジェクトを指定してください。'}, status=400)
    return body, None

def _validate_and_strip_fields(body, field_names):
    errors = {}
    for field in field_names:
        if field not in body:
            errors[field] = '必須項目です。'
        elif not isinstance(body[field], str):
            errors[field] = '文字列で指定してください。'
        elif not body[field].strip():
            errors[field] = '必須項目です。'
    if errors:
        return None, JsonResponse({'errors': errors}, status=400)
    normalized_fields = {field: body[field].strip() for field in field_names}
    return normalized_fields, None

@csrf_exempt
@require_POST
def register(request):
    body, error_response = _parse_json_body(request)
    if error_response: return error_response
    fields, error_response = _validate_and_strip_fields(body, ['name', 'password', 'secret_question', 'secret_answer'])
    if error_response: return error_response
    try:
        family = Family.objects.create(
            name=fields['name'],
            password=make_password(fields['password']),
            secret_question=fields['secret_question'],
            secret_answer=make_password(fields['secret_answer']),
        )
    except IntegrityError:
        return JsonResponse({'errors': {'name': 'この名前はすでに使われています。'}}, status=400)
    return JsonResponse(
        {
            'id': family.id,
            'name': family.name,
        },
        status=201,
    )

@csrf_exempt
@require_POST
def login(request):
    body, error_response = _parse_json_body(request)
    if error_response: return error_response
    fields, error_response = _validate_and_strip_fields(body, ['name', 'password'])
    if error_response: return error_response
    try:
        family = Family.objects.get(name=fields['name'])
    except Family.DoesNotExist:
        return JsonResponse({'error': '名前またはパスワードが違います。'}, status=401)
    if not check_password(fields['password'], family.password):
        return JsonResponse({'error': '名前またはパスワードが違います。'}, status=401)
    return JsonResponse({'id': family.id, 'name': family.name}, status=200)

@csrf_exempt
@require_http_methods(['DELETE'])
def delete_family_for_e2e(request, family_id):
    if not settings.DEBUG or not getattr(settings, 'E2E_CLEANUP_ENABLED', False):
        return JsonResponse({'error': 'この機能は開発環境でのみ利用できます。'}, status=403)
    expected_token = getattr(settings, 'E2E_CLEANUP_TOKEN', '')
    provided_token = request.headers.get('X-E2E-Cleanup-Token', '')
    if not expected_token or not constant_time_compare(provided_token, expected_token):
        return JsonResponse({'error': 'cleanupトークンが不正です。'}, status=403)
    family = get_object_or_404(Family, id=family_id)
    family.delete()
    return JsonResponse({'deleted_id': family_id}, status=200)
