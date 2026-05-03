import pytest
import random
from family.models import Family, Task


@pytest.mark.django_db
def test_delete_task_api(client):
    creator = Family.objects.create(name='del_creator', password='pw1', secret_question='q1', secret_answer='a1')
    assignee = Family.objects.create(name='del_assignee', password='pw2', secret_question='q2', secret_answer='a2')
    task = Task.objects.create(title='削除タスク', creator=creator, assignee=assignee, due_date='2026-12-31T00:00:00Z', status='未対応')
    task_id = task.id
    url = f'/auth/todos/{task_id}/'
    # 正常系: 削除成功
    response = client.delete(url)
    assert response.status_code == 200
    assert response.json()['deleted_id'] == task_id
    # DBから削除されていること
    assert not Task.objects.filter(id=task_id).exists()
    # 存在しないtask_idは404
    url_notfound = f'/auth/todos/{random.randint(10000, 99999)}/'
    response = client.delete(url_notfound)
    assert response.status_code == 404
