import pytest

from agent_app.agent import get_customer_count
from agent_app.models import Customer


@pytest.mark.django_db
def test_get_customer_count_returns_db_count():
    Customer.objects.create(customer_id=1, segment="SMB", signup_date="2026-01-01")
    Customer.objects.create(customer_id=2, segment="Enterprise", signup_date="2026-01-02")

    assert get_customer_count() == 2


@pytest.mark.django_db
def test_get_customer_count_is_zero_when_empty():
    assert get_customer_count() == 0
