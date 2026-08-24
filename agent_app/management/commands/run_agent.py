from django.core.management.base import BaseCommand

from agent_app.agent import agent


class Command(BaseCommand):
    help = "Hello-world handshake between agent.py, pydantic-ai, the LLM and the database."

    def handle(self, *args, **options):
        result = agent.run_sync("Did we have any product incident and did it affect usage?")
        self.stdout.write(result.output)
