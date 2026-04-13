import json

import pytest
from django.contrib.auth.hashers import check_password

from family.models import Family


# 正常系: 登録成功
@pytest.mark.django_db
def test_register_success(client):
    response = client.post(
        "/auth/register",
        data=json.dumps(
            {
                "name": "お母さん",
                "password": "TestPass123!",
                "secret_question": "初めて飼ったペットの名前は？",
                "secret_answer": "ポチ",
            }
        ),
        content_type="application/json",
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["name"] == "お母さん"
    assert "id" in payload
    assert "created_at" in payload
    assert "updated_at" in payload

    family = Family.objects.get(id=payload["id"])
    assert family.name == "お母さん"
    assert check_password("TestPass123!", family.password)


# 異常系: 必須項目が空の場合、バリデーションエラーになること
@pytest.mark.django_db
def test_register_validation_error_when_required_fields_missing(client):
    response = client.post(
        "/auth/register",
        data=json.dumps(
            {
                "name": "",
                "password": "",
                "secret_question": "",
                "secret_answer": "",
            }
        ),
        content_type="application/json",
    )

    assert response.status_code == 400
    payload = response.json()
    assert "errors" in payload
    assert payload["errors"]["name"] == "必須項目です。"
    assert payload["errors"]["password"] == "必須項目です。"
    assert payload["errors"]["secret_question"] == "必須項目です。"
    assert payload["errors"]["secret_answer"] == "必須項目です。"


# 異常系: 不正なJSONの場合、400エラーを返すこと
@pytest.mark.django_db
def test_register_invalid_json_returns_400(client):
    response = client.post(
        "/auth/register",
        data="not-json",
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json() == {"error": "リクエストボディが不正です。"}
