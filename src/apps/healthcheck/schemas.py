from dataclasses import dataclass


@dataclass
class HealthCheckResponseSchema:
    status: str = "ok"
