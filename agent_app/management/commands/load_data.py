import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from agent_app.models import Customer, DailyUsage, ProductIncident, Subscription

DAILY_USAGE_BATCH_SIZE = 5000


class Command(BaseCommand):
    help = "Load customer, subscription, daily_usage and product_incident CSVs into the database."

    def add_arguments(self, parser):
        parser.add_argument(
            "--data-dir",
            required=True,
            help="Directory containing customer.csv, subscription.csv, daily_usage.csv and product_incident.csv",
        )

    def handle(self, *args, **options):
        data_dir = Path(options["data_dir"])
        if not data_dir.is_dir():
            raise CommandError(f"Data directory not found: {data_dir}")

        with transaction.atomic():
            self.load_customers(data_dir / "customer.csv")
            self.load_subscriptions(data_dir / "subscription.csv")
            self.load_daily_usage(data_dir / "daily_usage.csv")
            self.load_product_incidents(data_dir / "product_incident.csv")

    def load_customers(self, path):
        rows = self.read_csv(path)
        customers = [
            Customer(
                customer_id=int(row["customer_id"]),
                segment=row["segment"],
                signup_date=row["signup_date"],
            )
            for row in rows
        ]
        Customer.objects.bulk_create(
            customers,
            update_conflicts=True,
            update_fields=["segment", "signup_date"],
            unique_fields=["customer_id"],
        )
        self.stdout.write(f"Loaded {len(customers)} customers")

    def load_subscriptions(self, path):
        rows = self.read_csv(path)
        subscriptions = [
            Subscription(
                subscription_id=int(row["subscription_id"]),
                customer_id=int(row["customer_id"]),
                plan=row["plan"],
                price=row["price"],
                start_date=row["start_date"],
                status=row["status"],
            )
            for row in rows
        ]
        Subscription.objects.bulk_create(
            subscriptions,
            update_conflicts=True,
            update_fields=["customer_id", "plan", "price", "start_date", "status"],
            unique_fields=["subscription_id"],
        )
        self.stdout.write(f"Loaded {len(subscriptions)} subscriptions")

    def load_daily_usage(self, path):
        rows = self.read_csv(path)
        usage_rows = [
            DailyUsage(
                customer_id=int(row["customer_id"]),
                date=row["date"],
                usage=int(row["usage"]),
            )
            for row in rows
        ]
        DailyUsage.objects.bulk_create(
            usage_rows,
            update_conflicts=True,
            update_fields=["usage"],
            unique_fields=["customer_id", "date"],
            batch_size=DAILY_USAGE_BATCH_SIZE,
        )
        self.stdout.write(f"Loaded {len(usage_rows)} daily usage rows")

    def load_product_incidents(self, path):
        rows = self.read_csv(path)
        incidents = [
            ProductIncident(
                incident_id=int(row["incident_id"]),
                date=row["date"],
                severity=row["severity"],
            )
            for row in rows
        ]
        ProductIncident.objects.bulk_create(
            incidents,
            update_conflicts=True,
            update_fields=["date", "severity"],
            unique_fields=["incident_id"],
        )
        self.stdout.write(f"Loaded {len(incidents)} product incidents")

    def read_csv(self, path):
        if not path.exists():
            raise CommandError(f"CSV file not found: {path}")
        with path.open(newline="") as f:
            return list(csv.DictReader(f))
