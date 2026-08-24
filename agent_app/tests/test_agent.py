import pytest

from agent_app.agent import (
    get_customer_count,
    get_customer_distribution_by_segment,
    get_daily_usage_totals,
    get_incidents,
    get_revenue_by_segment,
)
from agent_app.models import Customer, DailyUsage, ProductIncident, Subscription


@pytest.mark.django_db
def test_get_customer_count_returns_db_count():
    Customer.objects.create(customer_id=1, segment="SMB", signup_date="2026-01-01")
    Customer.objects.create(customer_id=2, segment="Enterprise", signup_date="2026-01-02")

    assert get_customer_count() == 2


@pytest.mark.django_db
def test_get_customer_count_is_zero_when_empty():
    assert get_customer_count() == 0


@pytest.mark.django_db
def test_get_revenue_by_segment_sums_price_per_segment():
    smb_1 = Customer.objects.create(customer_id=1, segment="SMB", signup_date="2026-01-01")
    smb_2 = Customer.objects.create(customer_id=2, segment="SMB", signup_date="2026-01-02")
    enterprise = Customer.objects.create(customer_id=3, segment="Enterprise", signup_date="2026-01-03")

    Subscription.objects.create(
        subscription_id=1, customer=smb_1, plan="Basic", price=30, start_date="2026-01-01", status="active"
    )
    Subscription.objects.create(
        subscription_id=2, customer=smb_2, plan="Basic", price=30, start_date="2026-01-02", status="active"
    )
    Subscription.objects.create(
        subscription_id=3, customer=enterprise, plan="Enterprise", price=200, start_date="2026-01-03", status="active"
    )

    assert get_revenue_by_segment() == {"SMB": 60.0, "Enterprise": 200.0}


@pytest.mark.django_db
def test_get_revenue_by_segment_is_empty_when_no_customers():
    assert get_revenue_by_segment() == {}


@pytest.mark.django_db
def test_get_customer_distribution_by_segment_counts_rows_not_ids():
    # customer_id values are deliberately large/uneven so a Sum-instead-of-Count
    # regression (summing IDs rather than counting rows) would fail this test.
    Customer.objects.create(customer_id=101, segment="SMB", signup_date="2026-01-01")
    Customer.objects.create(customer_id=202, segment="SMB", signup_date="2026-01-02")
    Customer.objects.create(customer_id=303, segment="Enterprise", signup_date="2026-01-03")

    assert get_customer_distribution_by_segment() == {"SMB": 2, "Enterprise": 1}


@pytest.mark.django_db
def test_get_customer_distribution_by_segment_is_empty_when_no_customers():
    assert get_customer_distribution_by_segment() == {}


@pytest.mark.django_db
def test_get_daily_usage_totals_sums_usage_per_day():
    customer_1 = Customer.objects.create(customer_id=1, segment="SMB", signup_date="2026-01-01")
    customer_2 = Customer.objects.create(customer_id=2, segment="Enterprise", signup_date="2026-01-01")

    DailyUsage.objects.create(customer=customer_1, date="2026-01-01", usage=10)
    DailyUsage.objects.create(customer=customer_2, date="2026-01-01", usage=15)
    DailyUsage.objects.create(customer=customer_1, date="2026-01-02", usage=5)

    assert get_daily_usage_totals() == {"2026-01-01": 25, "2026-01-02": 5}


@pytest.mark.django_db
def test_get_daily_usage_totals_is_empty_when_no_usage():
    assert get_daily_usage_totals() == {}


@pytest.mark.django_db
def test_get_incidents_returns_all_incidents_ordered_by_date():
    ProductIncident.objects.create(incident_id=2, date="2026-06-01", severity="minor")
    ProductIncident.objects.create(incident_id=1, date="2026-05-15", severity="major")

    assert get_incidents() == [
        {"incident_id": 1, "date": "2026-05-15", "severity": "major"},
        {"incident_id": 2, "date": "2026-06-01", "severity": "minor"},
    ]


@pytest.mark.django_db
def test_get_incidents_is_empty_when_no_incidents():
    assert get_incidents() == []
