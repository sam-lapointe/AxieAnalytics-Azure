import pytest
import sys
import asyncpg
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from axies import (
    datetime,
    timezone,
    Axies,
)