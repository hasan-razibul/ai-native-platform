import json

import httpx

from models.intent import CreateServiceIntent


class OllamaProvider:
    def __init__(
            self,
            model: str = "qwen2.5:3b",
            base_url: str = "http://localhost:11434",
            timeout: float = 120.0,
    ) -> None:
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def interpret_service_request(
            self, request: str
    ) -> CreateServiceIntent:
        schema = CreateServiceIntent.model_json_schema()

        payload = {
            "model": self.model,
            "stream": False,
            "format": schema,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You interpret developer requests for an internal "
                        "developer platform. Return a service intent matching "
                        "the supplied JSON schema. Use action='create_service'. "
                        "Use only the allowed language and environment values. "
                        "If required information is missing or ambiguous, do "
                        "not invent infrastructure requirements."
                    ),
                },
                {
                    "role": "user",
                    "content": request,
                },
            ],
            "options": {
                "temperature": 0,
            },
        }

        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/api/chat",
                json=payload,
            )
            response.raise_for_status()

        content = response.json()["message"]["content"]
        data = json.loads(content)

        return CreateServiceIntent.model_validate(data)