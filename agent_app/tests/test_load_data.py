import pytest
from django.core.management import call_command

from agent_app.models import Customer, DailyUsage, ProductIncident, Subscription


@pytest.fixture
def data_dir(tmp_path):
    (tmp_path / "customer.csv").write_text(
        "customer_id,segment,signup_date\n"
        "0,SMB,2026-05-25\n"
        "1,Enterprise,2026-06-10\n"
    )
    (tmp_path / "subscription.csv").write_text(
        "subscription_id,customer_id,plan,price,start_date,status\n"
        "0,0,Basic,30,2026-05-25,active\n"
        "1,1,Enterprise,200,2026-06-10,active\n"
    )
    (tmp_path / "daily_usage.csv").write_text(
        "customer_id,date,usage\n"
        "0,2026-05-25,41\n"
        "0,2026-05-26,29\n"
        "1,2026-06-10,10\n"
    )
    (tmp_path / "product_incident.csv").write_text(
        "incident_id,date,severity\n" "1,2026-05-15,major\n"
    )
    return tmp_path


@pytest.mark.django_db
def test_load_data_populates_models(data_dir):
    call_command("load_data", data_dir=str(data_dir))

    assert Customer.objects.count() == 2
    assert Subscription.objects.count() == 2
    assert DailyUsage.objects.count() == 3
    assert ProductIncident.objects.count() == 1

    customer = Customer.objects.get(pk=0)
    assert customer.subscription.plan == "Basic"


@pytest.mark.django_db
def test_load_data_is_idempotent(data_dir):
    call_command("load_data", data_dir=str(data_dir))
    call_command("load_data", data_dir=str(data_dir))

    assert Customer.objects.count() == 2
    assert DailyUsage.objects.count() == 3
