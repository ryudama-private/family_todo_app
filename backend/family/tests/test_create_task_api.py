import json
import pytest
from django.urls import reverse
from family.models import Family

@pytest.mark.django_db
def test_create_task_api(client):
    creator = Family.objects.create(name='creator', password='pw1', secret_question='q1', secret_answer='a1')
    assignee = Family.objects.create(name='assignee', password='pw2', secret_question='q2', secret_answer='a2')
    url = reverse('create_task')
    payload = {
        'title': 'テストタスク',
        'creator_id': creator.id,
        'assignee_id': assignee.id,
        'due_date': '2026-12-31T00:00:00Z',
        'status': '未対応'
    }
    response = client.post(url, data=json.dumps(payload), content_type='application/json')   
    assert response.status_code == 201
    data = response.json()
    assert data['title'] == 'テストタスク'

@pytest.mark.django_db
def test_create_task_api_required_fields(client):
    url = reverse('create_task')
    payload = {'title': '', 'creator_id': '', 'assignee_id': '', 'status': ''}
    response = client.post(url, data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_create_task_api_invalid_family(client):
    url = reverse('create_task')
    payload = {
        'title': 'タスク',
        'creator_id': 9999,
        'assignee_id': 8888,
        'status': '未対応'
    }
    response = client.post(url, data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_create_task_api_with_due_and_alarm(client):
    creator = Family.objects.create(name='c', password='pw1', secret_question='q1', secret_answer='a1')
    assignee = Family.objects.create(name='a', password='pw2', secret_question='q2', secret_answer='a2')
    url = reverse('create_task')
    payload = {
        'title': '期限付きタスク',
        'creator_id': creator.id,
        'assignee_id': assignee.id,
        'status': '進行中',
        'due_date': '2026-05-01T12:00:00Z',
        'alarm_minutes': 30
    }
    response = client.post(url, data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_task_api_returns_400_when_json_is_not_object(client):
    url = reverse('create_task')
    response = client.post(url, data='[]', content_type='application/json')
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_task_api_due_date_is_required(client):
    creator = Family.objects.create(name='creator_required', password='pw1', secret_question='q1', secret_answer='a1')
    assignee = Family.objects.create(name='assignee_required', password='pw2', secret_question='q2', secret_answer='a2')
    url = reverse('create_task')

    payload_missing = {
        'title': 'タスク',
        'creator_id': creator.id,
        'assignee_id': assignee.id,
        'status': '未対応'
    }
    response = client.post(url, data=json.dumps(payload_missing), content_type='application/json')
    assert response.status_code == 400

    payload_blank = {
        'title': 'タスク',
        'creator_id': creator.id,
        'assignee_id': assignee.id,
        'due_date': '',
        'status': '未対応'
    }
    response = client.post(url, data=json.dumps(payload_blank), content_type='application/json')
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_task_api_invalid_due_date_format_returns_400(client):
    creator = Family.objects.create(name='creator_invalid_due', password='pw1', secret_question='q1', secret_answer='a1')
    assignee = Family.objects.create(name='assignee_invalid_due', password='pw2', secret_question='q2', secret_answer='a2')
    url = reverse('create_task')
    payload = {
        'title': 'タスク',
        'creator_id': creator.id,
        'assignee_id': assignee.id,
        'due_date': 'not-a-datetime',
        'status': '未対応'
    }
    response = client.post(url, data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 400
