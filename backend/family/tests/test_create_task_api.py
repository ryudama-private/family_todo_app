import json
import pytest
from django.urls import reverse
from family.models import Family, Task

@pytest.mark.django_db
def test_create_task_api(client):
    # 事前にFamilyを2件作成
    creator = Family.objects.create(name="creator", password="pw1", secret_question="q1", secret_answer="a1")
    assignee = Family.objects.create(name="assignee", password="pw2", secret_question="q2", secret_answer="a2")

    url = reverse("create_task")
    payload = {
        "title": "テストタスク",
        "creator_id": creator.id,
        "assignee_id": assignee.id,
        "due_date": "2026-12-31",
        "status": "未対応"
    }
    response = client.post(url, data=json.dumps(payload), content_type="application/json")   
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "テストタスク"
    assert data["creator_id"] == creator.id
    assert data["assignee_id"] == assignee.id
    assert data["status"] == "未対応"
    assert data["due_date"] == "2026-12-31T00:00:00"
    assert data["alarm_minutes"] is None

@pytest.mark.django_db
def test_create_task_api_required_fields(client):
    url = reverse("create_task")
    # 必須項目が1つでも欠けている場合は400
    payload = {"title": "", "creator_id": "", "assignee_id": "", "status": ""}
    response = client.post(url, data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 400

@pytest.mark.django_db
def test_create_task_api_invalid_family(client):
    url = reverse("create_task")
    # 存在しないFamily ID
    payload = {
        "title": "タスク",
        "creator_id": 9999,
        "assignee_id": 8888,
        "status": "未対応"
    }
    response = client.post(url, data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 400
    assert "creator_id" in response.json().get("error", "") or "assignee_id" in response.json().get("error", "")

@pytest.mark.django_db
def test_create_task_api_with_due_and_alarm(client):
    creator = Family.objects.create(name="c", password="pw1", secret_question="q1", secret_answer="a1")
    assignee = Family.objects.create(name="a", password="pw2", secret_question="q2", secret_answer="a2")
    url = reverse("create_task")
    payload = {
        "title": "期限付きタスク",
        "creator_id": creator.id,
        "assignee_id": assignee.id,
        "status": "進行中",
        "due_date": "2026-05-01T12:00:00Z",
        "alarm_minutes": 30
    }
    response = client.post(url, data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 201
    data = response.json()
    assert data["due_date"].startswith("2026-05-01T12:00:00")
    assert data["alarm_minutes"] == 30
