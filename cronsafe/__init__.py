"""CronSafe - Python SDK for CronSafe cron job monitoring."""

__version__ = "1.0.0"

from .client import CronSafe, ping, ping_start, ping_fail

__all__ = ["CronSafe", "ping", "ping_start", "ping_fail"]
