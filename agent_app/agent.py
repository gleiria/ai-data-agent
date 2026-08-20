from pydantic_ai import Agent

from agent_app.models import Customer

# this is the definition. What the egnt is.
agent = Agent(
    "google:gemini-3.1-flash-lite-preview",
    instructions="You are a data analyst for a SaaS company. Answer questions using the available data tools.",
)


@agent.tool_plain
def get_customer_count() -> int:
    """Return the total number of customers in the database."""
    return Customer.objects.count()
