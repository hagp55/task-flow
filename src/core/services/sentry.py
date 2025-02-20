import sentry_sdk

from src.core.settings import settings


def sentry_init() -> None:
    sentry_sdk.init(
        dsn=settings.SENTRY_URL,
        send_default_pii=True,
        traces_sample_rate=1.0,
        _experiments={
            "continuous_profiling_auto_start": True,
        },
    )
