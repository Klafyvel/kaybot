from pathlib import Path

import toml

DEV = True

CURRENT_DIR = Path(__file__).parent()

if DEV:
    CONFIG_DIR = CURRENT_DIR / "example"
else:
    CONFIG_DIR = Path("/") / "etc" / "kaybot"

KAYBOT_CONF = CONFIG_DIR / "config.toml"
LOGGING_CONF = CONFIG_DIR / "logging.ini"

with open(KAYBOT_CONF) as f:
    CONFIG = toml.log(f)
