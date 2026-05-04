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


def _serialize_task(task):
    return {
        'id': task.id,
        'title': task.title,
        'creator_id': task.creator.id,
        'assignee_id': task.assignee.id,
        'due_date': task.due_date,
        'status': task.status,
        'alarm_minutes': task.alarm_minutes,
    }


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def todos(request):
    if request.method == 'GET':
        return list_tasks(request)
    return create_task(request)


def list_tasks(request):
    tasks = Task.objects.select_related('creator', 'assignee').order_by('id')
    return JsonResponse({'tasks': [_serialize_task(task) for task in tasks]}, status=200)

@csrf_exempt
@require_http_methods(['DELETE'])
def delete_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({'error': '指定されたタスクが存在しません'}, status=404)
    task.delete()
    return JsonResponse({'deleted_id': task_id}, status=200)

@csrf_exempt
@require_http_methods(['PATCH'])
def update_task_alarm_minutes(request, task_id):
    data, error_response = _parse_json_body(request)
    if error_response:
        return error_response
    if 'alarm_minutes' not in data:
        return JsonResponse({'error': 'alarm_minutesは必須です'}, status=400)
    alarm_minutes = data['alarm_minutes']
    if alarm_minutes is not None:
        if isinstance(alarm_minutes, bool) or not isinstance(alarm_minutes, int):
            return JsonResponse({'error': 'alarm_minutesは整数またはnullで指定してください'}, status=400)
        if alarm_minutes < 0:
            return JsonResponse({'error': 'alarm_minutesは0以上の整数で指定してください'}, status=400)
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({'error': '指定されたタスクが存在しません'}, status=404)
    task.alarm_minutes = alarm_minutes
    task.save()
    return JsonResponse({'alarm_minutes': task.alarm_minutes}, status=200)

@csrf_exempt
@require_http_methods(['PATCH'])
def update_task_due_date(request, task_id):
    data, error_response = _parse_json_body(request)
    if error_response:
        return error_response
    due_date_str = data.get('due_date')
    if not isinstance(due_date_str, str) or not due_date_str.strip():
        return JsonResponse({'error': 'due_dateは必須です'}, status=400)
    due_date = parse_datetime(due_date_str.strip())
    if due_date is None:
        return JsonResponse({'error': 'due_dateの形式が不正です'}, status=400)
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({'error': '指定されたタスクが存在しません'}, status=404)
    task.due_date = due_date
    task.save()
    return JsonResponse({'due_date': task.due_date}, status=200)

@csrf_exempt
@require_http_methods(['PATCH'])
def update_task_status(request, task_id):
    data, error_response = _parse_json_body(request)
    if error_response:
        return error_response
    status = data.get('status')
    if not isinstance(status, str) or not status.strip():
        return JsonResponse({'error': 'statusは必須です'}, status=400)
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({'error': '指定されたタスクが存在しません'}, status=404)
    task.status = status.strip()
    task.save()
    return JsonResponse({'status': task.status}, status=200)

@csrf_exempt
@require_http_methods(['PATCH'])
def update_task_assignee(request, task_id):
    data, error_response = _parse_json_body(request)
    if error_response:
        return error_response
    assignee_id = data.get('assignee_id')
    if assignee_id is None:
        return JsonResponse({'error': 'assignee_idは必須です'}, status=400)
    if isinstance(assignee_id, bool):
        return JsonResponse({'error': 'assignee_idは整数で指定してください'}, status=400)
    try:
        assignee_id = int(assignee_id)
    except (TypeError, ValueError):
        return JsonResponse({'error': 'assignee_idは整数で指定してください'}, status=400)
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({'error': '指定されたタスクが存在しません'}, status=404)
    try:
        assignee = Family.objects.get(id=assignee_id)
    except Family.DoesNotExist:
        return JsonResponse({'error': '指定された担当者が存在しません'}, status=400)
    task.assignee = assignee
    task.save()
    return JsonResponse({'assignee_id': task.assignee.id}, status=200)

@csrf_exempt
@require_http_methods(['PATCH'])
def update_task_title(request, task_id):
    data, error_response = _parse_json_body(request)
    if error_response:
        return error_response
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

def create_task(request):
    data, error_response = _parse_json_body(request)
    if error_response:
        return error_response
    required_fields = ['title', 'creator_id', 'assignee_id', 'due_date', 'status']
    for field in required_fields:
        if not data.get(field):
            return JsonResponse({'error': f'{field}は必須です'}, status=400)
    try:
        creator = Family.objects.get(id=data['creator_id'])
        assignee = Family.objects.get(id=data['assignee_id'])
    except Family.DoesNotExist:
        return JsonResponse({'error': 'creator_idまたはassignee_idが不正です'}, status=400)
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
    return JsonResponse(_serialize_task(task), status=201)

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
