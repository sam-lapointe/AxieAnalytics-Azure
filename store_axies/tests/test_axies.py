import pytest
import sys
import asyncpg
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from axies import Axie


# Mock the database connection.
@pytest.fixture
def mock_connection(mocker):
    """Create a mock database connection."""
    return mocker.AsyncMock()


@pytest.fixture
def axie_instance(mock_connection):
    """Create an Axie instance with a mock connection."""
    return Axie(
        connection=mock_connection,
        api_key="test_api_key",
        transaction_hash="test_hash",
        axie_id=12345,
        sale_date=1740000000,
    )


@pytest.mark.parametrize(
    "input, expected_result",
    [
        (
            # Axie Sold Level 19Max -> Ascended -> Earned AXP (Different date than sale date) -> Processed Delayed
            {
                "sale_date": "",
                "axie_axp_info": {"level": 20, "xp": 12000},
                "earned_axp_stat": {
                    "2025-06-03": [
                        {"source_id": "7", "xp": 10000},
                    ],
                    "2025-06-02": [
                        {"source_id": "7", "xp": 2000},
                    ]
                },
                "axie_activities": [
                    {
                        # Ascended after sale date
                        "activityType": "AscendAxie",
                        "createdAt": 1741000000,
                        "activityDetails": {"level": 20},
                    },
                ],
            },
            {"level": 19, "xp": 18870},
        ),
        (
            # Axie Sold Level 19Max -> Ascended -> Processed Delayed
            {
                "sale_date": "",
                "axie_axp_info": {"level": 20, "xp": 0},
                "earned_axp_stat": {},
                "axie_activities": [
                    {
                        # Ascended after sale date
                        "activityType": "AscendAxie",
                        "createdAt": 1741000000,
                        "activityDetails": {"level": 20},
                    },
                ],
            },
            {"level": 19, "xp": 18870},
        ),
        (
            # Axie Sold Level 17 -> Earn AXP (Different date than sale date) up to Level 19Max -> Processed Delayed
            {
                "sale_date": "",
                "axie_axp_info": {"level": 19, "xp": 18870},
                "earned_axp_stat": {
                    "2025-06-03": [
                        {"source_id": "7", "xp": 10000},
                        {"source_id": "2", "xp": 480},
                    ],
                    "2025-06-02": [
                        {"source_id": "7", "xp": 2000},
                        {"source_id": "3", "xp": 5000},
                    ],
                    "2025-06-01": [
                        {"source_id": "7", "xp": 10000},
                        {"source_id": "4", "xp": 3000},
                    ],
                    "2025-05-31": [
                        {"source_id": "7", "xp": 10000},
                        {"source_id": "5", "xp": 2000},
                    ],
                },
                "axie_activities": [
                    {
                        # Ascended before sale date
                        "activityType": "AscendAxie",
                        "createdAt": 1739000000,
                        "activityDetails": {"level": 10},
                    },
                ],
            },
            {"level": 17, "xp": 8000},
        ),
        (
            # Axie Sold Level 19 -> Earn AXP (Same date as sale date) up to Level 19Max -> Ascended -> Earn AXP -> Processed Delayed
            {
                "sale_date": "",
                "axie_axp_info": {"level": 20, "xp": 12000},
                "earned_axp_stat": {
                    "2025-06-03": [
                        {"source_id": "7", "xp": 10000},
                        {"source_id": "2", "xp": 2000},
                    ],
                    # This is the date of the sale
                    "2025-02-19": [
                        {"source_id": "7", "xp": 8870},
                    ],
                },
                "axie_activities": [
                    {
                        # Ascended after sale date
                        "activityType": "AscendAxie",
                        "createdAt": 1741000000,
                        "activityDetails": {"level": 20},
                    },
                ],
            },
            # The AXP earned on the sale date is not counted towards the level estimation.
            {"level": 19, "xp": 18870},
        ),
        (
            # Axie Sold Level 29 -> Earn AXP (Same date as sale date) up to Level 29Max -> Ascended -> Processed Same Day
            {
                "sale_date": "today",
                "axie_axp_info": {"level": 30, "xp": 2000},
                "earned_axp_stat": {
                    "2025-02-19": [
                        {"source_id": "7", "xp": 10000},
                        {"source_id": "2", "xp": 2000},
                    ],
                },
                "axie_activities": [
                    {
                        # Ascended after sale
                        "activityType": "AscendAxie",
                        "createdAt": 1740000500,
                        "activityDetails": {"level": 30},
                    },
                ],
            },
            {"level": 29, "xp": 47470},
        ),
        (
            # Axie Sold Level 20 -> Processed Same Day
            {
                "sale_date": "today",
                "axie_axp_info": {"level": 20, "xp": 0},
                "earned_axp_stat": {},
                "axie_activities": [],
            },
            {"level": 20, "xp": 0},
        ),
    ]
)
@pytest.mark.asyncio
async def test_estimate_axie_level(monkeypatch, axie_instance, input, expected_result):
    """Test the estimate_axie_level method."""
    
    if input["sale_date"] == "today":
        # Mock today's date.
        mock_today_date = datetime(2025, 2, 19, 12, 0, 0, tzinfo=timezone.utc)
        monkeypatch.setattr("axies.datetime", mock_today_date)
    
    axp_info = await axie_instance._Axie__estimate_axie_level(
        axie_axp_info=input["axie_axp_info"],
        earned_axp_stat=input["earned_axp_stat"],
        axie_activities=input["axie_activities"],
    )
    
    assert axp_info == expected_result