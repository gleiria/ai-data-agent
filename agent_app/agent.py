from django.db.models import Count, Sum
from pydantic_ai import Agent

from agent_app.models import Customer, DailyUsage, ProductIncident

# this is the definition. What the egnt is.
agent = Agent(
    "google:gemini-3.1-flash-lite-preview",
    instructions=(
        "You are a data analyst for a SaaS company. Answer questions using the "
        "available data tools. Only state numbers returned by a tool call — if no "
        "tool provides the figure needed, say so instead of estimating or guessing."
    ),
)


@agent.tool_plain
def get_customer_count() -> int:
    """Return the total number of customers in the database."""
    return Customer.objects.count()


@agent.tool_plain
def get_customer_distribution_by_segment() -> dict[str, int]:
    """Return the number of customers per segment."""
    rows = Customer.objects.values("segment").annotate(count=Count("customer_id")).order_by("segment")
    return {row["segment"]: row["count"] for row in rows}


@agent.tool_plain
def get_revenue_by_segment() -> dict[str, float]:
    """Return total subscription revenue grouped by customer segment."""
    rows = (
        Customer.objects.values("segment")
        .annotate(total_revenue=Sum("subscription__price"))
        .order_by("segment")
    )
    return {row["segment"]: float(row["total_revenue"] or 0) for row in rows}


@agent.tool_plain
def get_daily_usage_totals() -> dict[str, int]:
    """Return total product usage (summed across all customers) per day."""
    rows = DailyUsage.objects.values("date").annotate(total_usage=Sum("usage")).order_by("date")
    return {row["date"].isoformat(): row["total_usage"] for row in rows}


@agent.tool_plain
def get_incidents() -> list[dict]:
    """Return all logged product incidents, with their date and severity."""
    rows = ProductIncident.objects.order_by("date")
    return [
        {"incident_id": row.incident_id, "date": row.date.isoformat(), "severity": row.severity}
        for row in rows
    ]


