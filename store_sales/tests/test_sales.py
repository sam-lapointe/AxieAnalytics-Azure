import pytest
import sys
import asyncpg
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sales import (
    datetime,
    timezone,
    StoreSales,
)


# Mock the current time.
@pytest.fixture
def current_time(mocker):
    mock_current_time = datetime(2025, 5, 9, 12, 0, 0, tzinfo=timezone.utc)
    mock_datetime = mocker.patch("sales.datetime")
    mock_datetime.now.return_value = mock_current_time
    return mock_current_time


# Mock the database connection.
@pytest.fixture
def conn(mocker):
    return mocker.AsyncMock()


# Mock the ServiceBus Sender.
@pytest.fixture
def servicebus_sender(mocker):
    sender = mocker.AsyncMock()
    sender.send_messages = mocker.AsyncMock()
    return sender


# Test the StoreSales.add_to_db method.
@pytest.mark.parametrize(
    "sale_params, already_exists",
    [
        (
            {
                "block_number": 44153279,
                "block_timestamp": 1712773221,
                "transaction_hash": "0xb05e64ab435371a5c4b6e23f416a37fec881419228db0e35d9b3549204f549eb",
                "sales_list": [
                    {
                        "price_weth": 0.001836535870831618,
                        "axie_id": 11649154,
                    },
                ],
            },
            False,
        ),
        (
            {
                "block_number": 44153279,
                "block_timestamp": 1712773221,
                "transaction_hash": "0xb05e64ab435371a5c4b6e23f416a37fec881419228db0e35d9b3549204f549eb",
                "sales_list": [
                    {
                        "price_weth": 0.001836535870831618,
                        "axie_id": 11649154,
                    },
                    {
                        "price_weth": 0.02,
                        "axie_id": 123456789,
                    },
                ],
            },
            False,
        ),
        (
            {
                "block_number": 44153279,
                "block_timestamp": 1712773221,
                "transaction_hash": "0xb05e64ab435371a5c4b6e23f416a37fec881419228db0e35d9b3549204f549eb",
                "sales_list": [
                    {
                        "price_weth": 0.001836535870831618,
                        "axie_id": 11649154,
                    },
                ],
            },
            True,
        ),
        (
            {
                "block_number": 44153279,
                "block_timestamp": 1712773221,
                "transaction_hash": "0xb05e64ab435371a5c4b6e23f416a37fec881419228db0e35d9b3549204f549eb",
                "sales_list": [],
            },
            False,
        ),
    ],
)
@pytest.mark.asyncio
async def test_add_to_db(mocker, current_time, conn, sale_params, already_exists):
    # Create the StoreSales instance.
    store_sales = StoreSales(
        conn=conn,
        servicebus_sender=mocker.AsyncMock(),
        sales_list=sale_params["sales_list"],
        block_number=sale_params["block_number"],
        block_timestamp=sale_params["block_timestamp"],
        transaction_hash=sale_params["transaction_hash"],
    )

    num_sales = len(sale_params["sales_list"])

    if num_sales == 0:
        # If there are no sales, the function should return early.
        await store_sales.add_to_db()
        conn.execute.assert_not_called()
        return
    else:
        # If there are sales, the function should attempt to add them to the database.
        if already_exists:
            # If the sale already exists, it should handle the UniqueViolationError.
            conn.execute.side_effect = asyncpg.exceptions.UniqueViolationError(
                "Unique violation"
            )
            await store_sales.add_to_db()
            conn.execute.assert_called_once()
            assert conn.execute.call_count == num_sales
        else:
            # If the sale does not exist, it should add it to the database.
            conn.execute.side_effect = None
            await store_sales.add_to_db()
            assert conn.execute.call_count == num_sales

            for i in range(num_sales):
                axie_sale = {
                    "block_number": sale_params["block_number"],
                    "transaction_hash": sale_params["transaction_hash"],
                    "sale_date": sale_params["block_timestamp"],
                    "price_eth": sale_params["sales_list"][i]["price_weth"],
                    "axie_id": sale_params["sales_list"][i]["axie_id"],
                    "created_at": current_time,
                    "modified_at": current_time,
                }

                # The indentation of the query string is important to match the expected format.
                conn.execute.assert_any_call(
                        """
                        INSERT INTO axie_sales(
                            block_number,
                            transaction_hash,
                            sale_date,
                            price_eth,
                            axie_id,
                            created_at,
                            modified_at
                        )
                        VALUES (
                            $1, $2, $3, $4, $5, $6, $7
                        )
                        """,
                    *axie_sale.values(),
                )


@pytest.mark.parametrize(
    "axie_sale, expected_message",
    [
        (
            {
                "block_number": 44153279,
                "transaction_hash": "0xb05e64ab435371a5c4b6e23f416a37fec881419228db0e35d9b3549204f549eb",
                "sale_date": 1712773221,
                "price_eth": 0.001836535870831618,
                "axie_id": 11649154,
                "created_at": datetime(2025, 5, 9, 12, 0, 0, tzinfo=timezone.utc),
                "modified_at": datetime(2025, 5, 9, 12, 0, 0, tzinfo=timezone.utc),
            },
            {
                "transaction_hash": "0xb05e64ab435371a5c4b6e23f416a37fec881419228db0e35d9b3549204f549eb",
                "axie_id": 11649154,
            },
        ),
        (
            {
                "block_number": 44153279,
                "transaction_hash": "0xb05e64ab435371a5c4b6e23f416a37fec881419228db0e35d9b3549204f549eb",
                "sale_date": 1712773221,
                "price_eth": 0.02,
                "axie_id": 123456789,
                "created_at": datetime(2025, 5, 9, 12, 0, 0, tzinfo=timezone.utc),
                "modified_at": datetime(2025, 5, 9, 12, 0, 0, tzinfo=timezone.utc),
            },
            {
                "transaction_hash": "0xb05e64ab435371a5c4b6e23f416a37fec881419228db0e35d9b3549204f549eb",
                "axie_id": 123456789,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_send_topic_message(servicebus_sender, axie_sale, expected_message):
    # Create the StoreSales instance.
    store_sales = StoreSales(
        conn=None,
        servicebus_sender=servicebus_sender,
        sales_list=[axie_sale],
        block_number=axie_sale["block_number"],
        block_timestamp=axie_sale["sale_date"],
        transaction_hash=axie_sale["transaction_hash"],
    )

    # Call the method to test.
    await store_sales._StoreSales__send_topic_message(axie_sale)

    # Check that the send_messages method was called with the expected message.
    servicebus_sender.send_messages.assert_called_once()
    sent_message = servicebus_sender.send_messages.call_args[0][0]

    sent_message_body = json.loads(
        b"".join(sent_message.body).decode("utf-8").replace("'", '"')
    )
    assert sent_message_body == expected_message
