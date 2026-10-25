from typing import Protocol

from models.intent import CreateServiceIntent


class LLMProvider(Protocol):
    def interpret_service_request(
            self, request: str
    ) -> CreateServiceIntent:
        """Convert a natural-language request into a validated service intent."""
        ...