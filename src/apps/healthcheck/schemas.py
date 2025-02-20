from dataclasses import dataclass


@dataclass
class HealthCheckResponseSchema:
    status: str = "api is working."


@dataclass
class HealthCheckDBResponseSchema:
    status: str = "db is working."
