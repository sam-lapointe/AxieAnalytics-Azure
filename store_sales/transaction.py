import asyncpg
import logging
import aiohttp
from contract import Contract
from web3 import Web3, AsyncWeb3


class Transaction:
    """
    Represents a Ronin blockchain sale transaction and interacts with associated contracts to gather specific data about the sale.
    """
    def __init__(self, conn: asyncpg.Connection, w3: AsyncWeb3, http_client: aiohttp.ClientSession):
        self.__conn = conn
        self.__w3 = w3
        self.__http_client = http_client


    async def __get_receipt(self, transaction_hash):
        """Returns the transaction receipt."""
        try:
            receipt = await self.__w3.eth.get_transaction_receipt(transaction_hash)
            return receipt

        except Exception as e:
            logging.error(f"[__get_receipt] An unexpected error occured while retrieving receipt for transaction {transaction_hash}: {e}")
            raise e
    
    """
    This might be better as a classmethod.
    """
    async def process_logs(self, transaction_hash) -> list:
        """
        Looks for specifc data in the logs and returns a list of the sold prices and assets IDs.
        """
        try:
            logging.info(f"[__process_logs] Processing logs for transaction {transaction_hash}...")
            receipt = await self.__get_receipt(transaction_hash)
            logs = receipt["logs"]
            sender = receipt["from"]
            recipient = receipt["to"]

            weth_contract = await Contract.create(self.__conn, self.__w3, self.__http_client, "0xc99a6a985ed2cac1ef41640596c5a5f9f4e19ef5")
            axie_proxy_contract = await Contract.create(self.__conn, self.__w3, self.__http_client, "0x32950db2a7164ae833121501c797d79e7b79d74c")

            prices = []
            axies = []

            for log in logs:
                topic = f"0x{log['topics'][0].hex()}"
                """
                Every payment is converted into WETH and transferred to the contract (recipient).
                If the payment was made directly in WETH, the WETH is transfered from the sender directly to the contract (recipient).

                Else, the sender transfer the currency to the contract, which then proceeds to exchange it for WETH.
                This causes multiple events, the important one is a transfer from the WETH contract to the contract (recipient).
                """
                if log["address"] == weth_contract.get_contract_address() and weth_contract.get_event_name(topic) == "Transfer":
                    event_data = weth_contract.get_event_data(topic, log)
                    if event_data["args"]["_to"] == recipient:
                        prices.append(Web3.from_wei(event_data["args"]["_value"], "ether"))
                
                """
                Every Axie sales call the Axie Proxy contract with the event Transfer to transfer the Axie from the seller to buyer.
                """
                if log["address"] == axie_proxy_contract.get_contract_address and axie_proxy_contract.get_event_name(topic) == "Transfer":
                    event_data = axie_proxy_contract.get_event_data(topic, log)
                    axies.append(event_data["args"]["_tokenId"])

            """
            All events in a transaction are in the same order wheter it contains multiple sales or only one.
            First there is the currency transfer and swaps if needed, then the asset transfer and it is repeated 
            in this order if there are many sales   in the transaction.
            """
            sales_list = [{"price_weth": price, "axie_id": axie_id} for price, axie_id in zip(prices, axies)]
            return sales_list
        
        except Exception as e:
            logging.error(f"[__process_logs] An unexpected error occured while processing logs for transaction {transaction_hash}: {e}")
            raise e