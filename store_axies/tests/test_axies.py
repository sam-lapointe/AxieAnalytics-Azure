import pytest
import sys
import asyncpg
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from axies import (
    datetime,
    timezone,
    Axie,
)


# Mock the database connection.
@pytest.fixture
def mock_connection(mocker):
    """Create a mock database connection."""
    return mocker.AsyncMock()

# Mock aiohttp.ClientSession
@pytest.fixture
def mock_aiohttp_session(mocker):
    """Create a mock aiohttp.ClientSession."""
    mocker.patch(
        "store_axies.axies.aiohttp.ClientSession"
    )

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

@pytest.mark.asyncio
async def test_get_axie_data(mocker, axie_instance, mock_aiohttp_session):
    """Test the get_axie_data method."""

    # Mock the response from the API
    mock_response = {
        "id": 12345,
        "name": "Test Axie",
        "class": "Aquatic",
        "parts": ["Tail", "Back", "Horn"],
        "price": 1000,
    }
    
    axie_instance._get_axie_data = mocker.AsyncMock(return_value=mock_response)
    
    result = await axie_instance.get_axie_data()
    
    assert result == mock_response
    axie_instance._get_axie_data.assert_called_once()