import json
import pytest
from django.contrib.auth.hashers import make_password
from family.models import Family

@pytest.mark.django_db
def test_login_success(client):
    family = Family.objects.create(
        name="お母さん",
        password=make_password("TestPass123!"),
        secret_question="好きな食べ物は？",
        secret_answer=make_password("カレー"),
    )

    response = client.post(
        "/auth/login/",
        data=json.dumps(
            {
                "name": "お母さん",
                "password": "TestPass123!",
            }
        ),
        content_type="application/json",
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == family.id
    assert payload["name"] == "お母さん"
    assert set(payload.keys()) == {"id", "name"}

@pytest.mark.django_db
def test_login_returns_401_when_name_is_invalid(client):
    Family.objects.create(
        name="お父さん",
        password=make_password("TestPass123!"),
        secret_question="好きな色は？",
        secret_answer=make_password("青"),
    )

    response = client.post(
        "/auth/login/",
        data=json.dumps(
            {
                "name": "存在しない名前",
                "password": "TestPass123!",
            }
        ),
        content_type="application/json",
    )

    assert response.status_code == 401
    assert response.json() == {"error": "名前またはパスワードが違います。"}

@pytest.mark.django_db
def test_login_returns_401_when_password_is_invalid(client):
    Family.objects.create(
        name="お父さん",
        password=make_password("CorrectPass123!"),
        secret_question="好きな色は？",
        secret_answer=make_password("青"),
    )

    response = client.post(
        "/auth/login/",
        data=json.dumps(
            {
                "name": "お父さん",
                "password": "WrongPass123!",
            }
        ),
        content_type="application/json",
    )

    assert response.status_code == 401
    assert response.json() == {"error": "名前またはパスワードが違います。"}

@pytest.mark.django_db
def test_login_validation_error_when_required_fields_missing(client):
    response = client.post(
        "/auth/login/",
        data=json.dumps(
            {
                "name": "",
                "password": "",
            }
        ),
        content_type="application/json",
    )

    assert response.status_code == 400
    payload = response.json()
    assert "errors" in payload
    assert payload["errors"]["name"] == "必須項目です。"
    assert payload["errors"]["password"] == "必須項目です。"

@pytest.mark.django_db
@pytest.mark.parametrize(
    "request_body, expected_missing_keys",
    [
        ({}, ["name", "password"]),
        ({"name": "お母さん"}, ["password"]),
    ],
)
def test_login_returns_400_when_required_keys_are_missing(
    client,
    request_body,
    expected_missing_keys,
):
    response = client.post(
        "/auth/login/",
        data=json.dumps(request_body),
        content_type="application/json",
    )

    assert response.status_code == 400
    payload = response.json()
    assert "errors" in payload
    for key in expected_missing_keys:
        assert key in payload["errors"]

@pytest.mark.django_db
def test_login_invalid_json_returns_400(client):
    response = client.post(
        "/auth/login/",
        data="not-json",
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json() == {"error": "リクエストボディが不正です。"}

@pytest.mark.django_db
def test_login_null_fields_returns_400(client):
    response = client.post(
        "/auth/login/",
        data=json.dumps(
            {
                "name": None,
                "password": None,
            }
        ),
        content_type="application/json",
    )

    assert response.status_code == 400
    payload = response.json()
    assert payload["errors"]["name"] == "文字列で指定してください。"
    assert payload["errors"]["password"] == "文字列で指定してください。"
