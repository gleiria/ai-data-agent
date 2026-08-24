# Tools whose output can be plotted, and how to plot it.
# "target" is the id of the dashboard <div> the chart should render into.
CHART_TOOLS = {
    "get_customer_distribution_by_segment": {
        "chart_type": "bar",
        "title": "Customers by Segment",
        "target": "chart-main",
    },
    "get_revenue_by_segment": {
        "chart_type": "bar",
        "title": "Revenue by Segment",
        "target": "chart-main",
    },
    "get_daily_usage_totals": {
        "chart_type": "line",
        "title": "Usage Over Time",
        "target": "chart-main",
    },
}


def get_chart(tool_name, data):
    """Return chart config + data for a tool's output, or None if it isn't chartable."""
    config = CHART_TOOLS.get(tool_name)
    if config is None:
        return None
    return {**config, "data": data}
