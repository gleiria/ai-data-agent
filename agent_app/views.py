import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from pydantic_ai.messages import ToolReturnPart

from agent_app.agent import agent
from agent_app.visualisations import get_chart


def dashboard(request):
    return render(request, "dashboard.html")


@require_POST
def ask_agent(request):
    body = json.loads(request.body)
    question = body.get("question", "").strip()

    if not question:
        return JsonResponse({"error": "No question provided."}, status=400)

    result = agent.run_sync(question)

    chart = None
    for message in result.all_messages():
        for part in message.parts:
            if isinstance(part, ToolReturnPart):
                tool_chart = get_chart(part.tool_name, part.content)
                if tool_chart is not None:
                    chart = tool_chart

    return JsonResponse({"answer": result.output, "chart": chart})
