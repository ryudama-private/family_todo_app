import json

import pytest
from django.contrib.auth.hashers import check_password

from family.models import Family


# 正常系: 登録成功
@pytest.mark.django_db
def test_register_success(client):
    response = client.post(
        "/auth/register/",
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
        "/auth/register/",
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
        "/auth/register/",
        data="not-json",
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json() == {"error": "リクエストボディが不正です。"}


# 異常系: 文字列以外の値（null）を送った場合、400エラーを返すこと
@pytest.mark.django_db
def test_register_null_fields_returns_400(client):
    response = client.post(
        "/auth/register/",
        data=json.dumps(
            {
                "name": None,
                "password": None,
                "secret_question": None,
                "secret_answer": None,
            }
        ),
        content_type="application/json",
    )

    assert response.status_code == 400
    payload = response.json()
    assert payload["errors"]["name"] == "文字列で指定してください。"
    assert payload["errors"]["password"] == "文字列で指定してください。"
    assert payload["errors"]["secret_question"] == "文字列で指定してください。"
    assert payload["errors"]["secret_answer"] == "文字列で指定してください。"


# 正常系: secret_answer がハッシュ化されて保存されること
@pytest.mark.django_db
def test_register_secret_answer_is_hashed(client):
    response = client.post(
        "/auth/register/",
        data=json.dumps(
            {
                "name": "お父さん",
                "password": "TestPass123!",
                "secret_question": "好きな食べ物は？",
                "secret_answer": "カレー",
            }
        ),
        content_type="application/json",
    )

    assert response.status_code == 201
    family = Family.objects.get(id=response.json()["id"])
    assert family.secret_answer != "カレー"
    assert check_password("カレー", family.secret_answer)


@pytest.mark.django_db
def test_delete_family_for_e2e_deletes_only_target_record(client, settings):
    settings.DEBUG = True
    target = Family.objects.create(
        name="e2e-target",
        password="hashed-password",
        secret_question="好きな色は？",
        secret_answer="hashed-answer",
    )
    other = Family.objects.create(
        name="keep-me",
        password="hashed-password",
        secret_question="好きな動物は？",
        secret_answer="hashed-answer",
    )

    response = client.delete(f"/auth/register/{target.id}/")

    assert response.status_code == 200
    assert response.json() == {"deleted_id": target.id}
    assert not Family.objects.filter(id=target.id).exists()
    assert Family.objects.filter(id=other.id).exists()


@pytest.mark.django_db
def test_delete_family_for_e2e_is_forbidden_when_debug_disabled(client, settings):
    settings.DEBUG = False
    family = Family.objects.create(
        name="e2e-target",
        password="hashed-password",
        secret_question="好きな色は？",
        secret_answer="hashed-answer",
    )

    response = client.delete(f"/auth/register/{family.id}/")

    assert response.status_code == 403
    assert response.json() == {"error": "この機能は開発環境でのみ利用できます。"}
    assert Family.objects.filter(id=family.id).exists()
