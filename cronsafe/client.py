"""CronSafe Python client - uses only stdlib (no dependencies)."""

import urllib.request
import urllib.parse
import urllib.error

DEFAULT_BASE_URL = "https://api.getcronsafe.com"


class CronSafeError(Exception):
    """Raised when a CronSafe API call fails."""
    pass


class CronSafe:
    """CronSafe API client.

    Args:
        base_url: API base URL (default: https://api.getcronsafe.com).
        timeout: Request timeout in seconds (default: 30).
    """

    def __init__(self, base_url=DEFAULT_BASE_URL, timeout=30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def ping(self, slug, status=None, output=None):
        """Send a ping to a CronSafe monitor.

        Args:
            slug: Monitor slug from your CronSafe dashboard.
            status: Optional status - "success" (default) or "fail".
            output: Optional text output to attach.

        Returns:
            True if accepted (2xx response).

        Raises:
            CronSafeError: If the request fails.
        """
        url = f"{self.base_url}/ping/{slug}"
        params = {}
        if status == "fail":
            params["status"] = "fail"
        if output:
            params["output"] = output
        if params:
            url += "?" + urllib.parse.urlencode(params)
        return self._request(url)

    def pingStart(self, slug):
        """Signal the start of a job for duration tracking.

        Args:
            slug: Monitor slug.

        Returns:
            True if accepted.
        """
        url = f"{self.base_url}/ping/{slug}/start"
        return self._request(url)

    def pingFail(self, slug, output=None):
        """Signal a job failure.

        Args:
            slug: Monitor slug.
            output: Optional error message.

        Returns:
            True if accepted.
        """
        return self.ping(slug, status="fail", output=output)

    def _request(self, url):
        """Make an HTTP GET request.

        Returns:
            True if accepted (2xx).

        Raises:
            CronSafeError: On network or HTTP errors.
        """
        try:
            req = urllib.request.Request(url)
            resp = urllib.request.urlopen(req, timeout=self.timeout)
            code = resp.getcode()
            if 200 <= code < 300:
                return True
            raise CronSafeError(f"HTTP {code}")
        except urllib.error.HTTPError as e:
            raise CronSafeError(f"HTTP {e.code}: {e.reason}") from e
        except urllib.error.URLError as e:
            raise CronSafeError(f"Request failed: {e.reason}") from e


# ---------------------------------------------------------------------------
# Module-level convenience functions
# ---------------------------------------------------------------------------

_default_client = None


def _get_client():
    global _default_client
    if _default_client is None:
        _default_client = CronSafe()
    return _default_client


def ping(slug, status=None, output=None):
    """Send a success ping. See CronSafe.ping for details."""
    return _get_client().ping(slug, status=status, output=output)


def ping_start(slug):
    """Signal job start. See CronSafe.pingStart for details."""
    return _get_client().pingStart(slug)


def ping_fail(slug, output=None):
    """Signal failure. See CronSafe.pingFail for details."""
    return _get_client().pingFail(slug, output=output)
