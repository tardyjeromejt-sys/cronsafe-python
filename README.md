# CronSafe Python SDK

Official Python SDK for [CronSafe](https://getcronsafe.com) - cron job monitoring with 15 features.

## Installation

```bash
pip install cronsafe
```

## Quick Start

```python
import cronsafe
cronsafe.ping("your-monitor-slug")
```

## Usage

### Simple ping
```python
cronsafe.ping("nightly-backup")
```

### Signal job start
```python
cronsafe.ping_start("nightly-backup")
# ... your job ...
cronsafe.ping("nightly-backup")
```

### Signal failure
```python
try:
    run_backup()
    cronsafe.ping("nightly-backup")
except Exception as e:
    cronsafe.ping_fail("nightly-backup", output=str(e))
```

### Custom client
```python
from cronsafe import CronSafe
client = CronSafe(base_url="https://api.getcronsafe.com", timeout=30)
client.ping("my-monitor")
```

## API Reference

- `cronsafe.ping(slug, output=None)` - Send success ping
- `cronsafe.ping_start(slug)` - Signal job start
- `cronsafe.ping_fail(slug, output=None)` - Signal failure

## Links
- [getcronsafe.com](https://getcronsafe.com)
- [Documentation](https://getcronsafe.com/docs)

## License
MIT
