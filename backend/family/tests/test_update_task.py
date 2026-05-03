import json
import pytest
import random
from family.models import Family, Task

@pytest.mark.django_db
def test_update_task_title_api(client):
    creator = Family.objects.create(name='creator2', password='pw1', secret_question='q1', secret_answer='a1')
    assignee = Family.objects.create(name='assignee2', password='pw2', secret_question='q2', secret_answer='a2')
    task = Task.objects.create(title='元のタイトル', creator=creator, assignee=assignee, due_date='2026-12-31T00:00:00Z', status='未対応')
    url = f'/auth/todos/{task.id}/title/'
    payload = {'title': '新しいタイトル'}
    response = client.patch(url, data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == '新しいタイトル'
    # 空文字はエラー
    response = client.patch(url, data=json.dumps({'title': '  '}), content_type='application/json')
    assert response.status_code == 400
    # 存在しないIDは404
    url_notfound = f'/auth/todos/{random.randint(10000,99999)}/title/'
    response = client.patch(url_notfound, data=json.dumps({'title': 'abc'}), content_type='application/json')
    assert response.status_code == 404
    # JSON配列はエラー
    response = client.patch(url, data='[]', content_type='application/json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_update_task_assignee_api(client):
    creator = Family.objects.create(name='owner', password='pw1', secret_question='q1', secret_answer='a1')
    assignee1 = Family.objects.create(name='old_assignee', password='pw2', secret_question='q2', secret_answer='a2')
    assignee2 = Family.objects.create(name='new_assignee', password='pw3', secret_question='q3', secret_answer='a3')
    task = Task.objects.create(title='担当者変更タスク', creator=creator, assignee=assignee1, due_date='2026-12-31T00:00:00Z', status='未対応')
    url = f'/auth/todos/{task.id}/assignee_id/'
    # 正常系: 担当者変更
    response = client.patch(url, data=json.dumps({'assignee_id': assignee2.id}), content_type='application/json')
    assert response.status_code == 200
    assert response.json()['assignee_id'] == assignee2.id
    # 整数字符列も許可
    response = client.patch(url, data=json.dumps({'assignee_id': str(assignee1.id)}), content_type='application/json')
    assert response.status_code == 200
    assert response.json()['assignee_id'] == assignee1.id
    # 非整数はエラー
    response = client.patch(url, data=json.dumps({'assignee_id': 'abc'}), content_type='application/json')
    assert response.status_code == 400
    # assignee_idなしはエラー
    response = client.patch(url, data=json.dumps({}), content_type='application/json')
    assert response.status_code == 400
    # 存在しないassignee_idはエラー
    response = client.patch(url, data=json.dumps({'assignee_id': 99999}), content_type='application/json')
    assert response.status_code == 400
    # 存在しないtask_idは404
    url_notfound = f'/auth/todos/{random.randint(10000,99999)}/assignee_id/'
    response = client.patch(url_notfound, data=json.dumps({'assignee_id': assignee2.id}), content_type='application/json')
    assert response.status_code == 404
    # JSON配列はエラー
    response = client.patch(url, data='[]', content_type='application/json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_update_task_status_api(client):
    creator = Family.objects.create(name='status_creator', password='pw1', secret_question='q1', secret_answer='a1')
    assignee = Family.objects.create(name='status_assignee', password='pw2', secret_question='q2', secret_answer='a2')
    task = Task.objects.create(title='進行状況変更タスク', creator=creator, assignee=assignee, due_date='2026-12-31T00:00:00Z', status='未対応')
    url = f'/auth/todos/{task.id}/status/'
    # 正常系: 進行状況変更
    response = client.patch(url, data=json.dumps({'status': '進行中'}), content_type='application/json')
    assert response.status_code == 200
    assert response.json()['status'] == '進行中'
    # 空文字はエラー
    response = client.patch(url, data=json.dumps({'status': '  '}), content_type='application/json')
    assert response.status_code == 400
    # statusキーなしはエラー
    response = client.patch(url, data=json.dumps({}), content_type='application/json')
    assert response.status_code == 400
    # 存在しないtask_idは404
    url_notfound = f'/auth/todos/{random.randint(10000,99999)}/status/'
    response = client.patch(url_notfound, data=json.dumps({'status': '完了'}), content_type='application/json')
    assert response.status_code == 404
    # JSON配列はエラー
    response = client.patch(url, data='[]', content_type='application/json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_update_task_due_date_api(client):
    creator = Family.objects.create(name='due_creator', password='pw1', secret_question='q1', secret_answer='a1')
    assignee = Family.objects.create(name='due_assignee', password='pw2', secret_question='q2', secret_answer='a2')
    task = Task.objects.create(title='期限変更タスク', creator=creator, assignee=assignee, due_date='2026-12-31T00:00:00Z', status='未対応')
    url = f'/auth/todos/{task.id}/due_date/'
    # 正常系: 期限変更
    response = client.patch(url, data=json.dumps({'due_date': '2027-01-15T09:30:00Z'}), content_type='application/json')
    assert response.status_code == 200
    assert response.json()['due_date'] == '2027-01-15T09:30:00Z'
    # 空文字はエラー
    response = client.patch(url, data=json.dumps({'due_date': '  '}), content_type='application/json')
    assert response.status_code == 400
    # due_dateキーなしはエラー
    response = client.patch(url, data=json.dumps({}), content_type='application/json')
    assert response.status_code == 400
    # 形式不正はエラー
    response = client.patch(url, data=json.dumps({'due_date': 'not-a-datetime'}), content_type='application/json')
    assert response.status_code == 400
    # 存在しないtask_idは404
    url_notfound = f'/auth/todos/{random.randint(10000,99999)}/due_date/'
    response = client.patch(url_notfound, data=json.dumps({'due_date': '2027-01-15T09:30:00Z'}), content_type='application/json')
    assert response.status_code == 404
    # JSON配列はエラー
    response = client.patch(url, data='[]', content_type='application/json')
    assert response.status_code == 400
