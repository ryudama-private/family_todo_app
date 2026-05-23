import pytest
from django.urls import reverse

from family.models import Family


@pytest.mark.django_db
def test_list_families_returns_id_and_name_in_id_order(client):
    first = Family.objects.create(
        name="お母さん",
        password="pw1",
        secret_question="q1",
        secret_answer="a1",
    )
    second = Family.objects.create(
        name="お父さん",
        password="pw2",
        secret_question="q2",
        secret_answer="a2",
    )

    response = client.get(reverse("list_families"))

    assert response.status_code == 200
    assert response.json() == {
        "families": [
            {"id": first.id, "name": "お母さん"},
            {"id": second.id, "name": "お父さん"},
        ]
    }
