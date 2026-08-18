from django.db import models


SEGMENT_CHOICES = [
    ("SMB", "SMB"),
    ("Mid_market", "Mid-Market"),
    ("Enterprise", "Enterprise"),
]


class Customer(models.Model):
    customer_id = models.IntegerField(primary_key=True)
    segment = models.CharField(max_length=20, choices=SEGMENT_CHOICES)
    signup_date = models.DateField()

    def __str__(self):
        return f"Customer {self.customer_id}"


PLAN_CHOICES = [
    ("Basic", "Basic"),
    ("Pro", "Pro"),
    ("Enterprise", "Enterprise"),
]


class Subscription(models.Model):
    subscription_id = models.IntegerField(primary_key=True)
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, related_name="subscription"
    )
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"Subscription {self.subscription_id} ({self.customer_id})"


class DailyUsage(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="daily_usage"
    )
    date = models.DateField()
    usage = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["customer", "date"], name="unique_customer_usage_date"
            )
        ]
        indexes = [models.Index(fields=["customer", "date"])]

    def __str__(self):
        return f"{self.customer_id} usage on {self.date}"


class ProductIncident(models.Model):
    incident_id = models.IntegerField(primary_key=True)
    date = models.DateField()
    severity = models.CharField(max_length=20)

    def __str__(self):
        return f"Incident {self.incident_id} ({self.severity})"
