from pydantic import BaseModel, Field
from typing import Literal


class ServiceSpec(BaseModel):
    name: str = Field(min_length=1, max_length=63)
    language: Literal["python", "go"]
    port: int = Field(ge=1, le=65535)
    replicas: int = Field(ge=1, le=10)


class CreateServiceIntent(BaseModel):
    action: Literal["create_service"]
    service: ServiceSpec
    environment: Literal["dev", "staging", "production"]
