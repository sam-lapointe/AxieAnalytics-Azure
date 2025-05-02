import asyncpg
import logging
import aiohttp
import time
from web3 import Web3, AsyncWeb3


NOT_PROXY_VERSION_NUMBER = 255  # Indicates a non-proxy contract


class ContractNotFoundError(Exception):
    pass


class Contract:
    """
    Represents a smart contract and provides methods to interact with it.

    Attributes:
        conn: Database connection object.
        w3: Web3 instance for interacting with the Ethereum blockchain.
        http_client: HTTP client for making API requests.
        contract_address: The address of the contract.
    """

    visited_contracts_addresses = set()  # Class-level set to track visited contracts addresses.

    def __init__(self, conn: asyncpg.Connection, w3: AsyncWeb3, http_client: aiohttp.ClientSession, contract_address: str):
        self.__eip1967_slot = "0x360894A13BA1A3210667C828492DB98DCA3E2076CC3735A920A3CA505D382BBC"
        self.__conn = conn
        self.__w3 = w3
        self.__http_client = http_client
        self.__contract_address = Web3.to_checksum_address(contract_address)
        self.__name = None
        self.__is_proxy = None
        self.__implementation = None
        self.__abi = None
        self.__contract = None


    @classmethod
    async def create(cls, conn: asyncpg.Connection, w3: AsyncWeb3, http_client: aiohttp.ClientSession, contract_address: str):
        """
        Factory method to create and initialize a Contract instance asynchronously.
        """

        # Create an instance of the class
        instance = cls(conn, w3, http_client, contract_address)

        # Perform asynchronous initialization
        await instance.__get_contract_data()

        return instance


    async def __get_contract_data(self) -> None:
        """
        Retrieves the contract data from the database or call __add_contract_data if it isn't in the database.
        It then set the object's variables.
        """
        try:
            # Check for infinite recursion
            if self.__contract_address in Contract.visited_contracts_addresses:
                raise ValueError(f"Infinite recursion detected for contract {self.__contract_address}.")
            Contract.visited_contracts_addresses.add(self.__contract_address)

            # Retrieve contract data from database.
            contract_data = await self.__conn.fetchrow(
                "SELECT * FROM contracts WHERE contract_address = $1", self.__contract_address
            )
            if contract_data is None:
                logging.info(f"[__get_contract_data] Contract {self.__contract_address} is not in the database.")
                # Call method to retrieve the contract data and add it to the database.
                await self.__add_contract_data()
                # Retrieve contract data from database after it has been added.
                contract_data = await self.__conn.fetchrow(
                    "SELECT * FROM contracts WHERE contract_address = $1", self.__contract_address
                )
                if contract_data is None:
                    logging.error(f"[__get_contract_data] Contract {self.__contract_address} is not in the database after calling self.__add_contract_data().")
                    raise ContractNotFoundError(f"Contract {self.__contract_address} is not in the database after calling self.__add_contract_data().")
            
            # TODO: Set object variables
            self.__name = contract_data["contract_name"]
            self.__is_proxy = contract_data["is_proxy"]
            self.__abi = contract_data["abi"]
            self.__contract = self.__w3.eth.contract(address=self.__contract_address, abi=self.__abi)
            implementation_address = contract_data["implementation_address"]

            if self.__is_proxy:
                logging.info(f"[__get_contract_data] Contract {self.__contract_address} ({self.__name}) is a proxy. Fetching implementation contract at {self.__implementation}.")
                if not implementation_address:
                    raise ValueError(f"Implementation address is missing for proxy contract {self.__contract_address} ({self.__name}).")
                
                # Create an instance of the implementation contract
                self.__implementation = await Contract.create(
                    self.__conn, self.__w3, self.__http_client, implementation_address
                )
        except Exception as e:
            logging.error(f"[__get_contract_data] An unexpected error occured: {e}")
            raise e
        finally:
            # Remove the address from the visited set after processing
            Contract.visited_contracts_addresses.discard(self.__contract_address)


    async def __add_contract_data(self) -> None:
        """
        Retrieves the contracts information from roninchain.com and adds it to the database.
        """
        try:
            logging.info(f"[__add_contract_data] Fetching data for contract {self.__contract_address} from roninchain.com...")

            abi_url = f"https://explorer-kintsugi.roninchain.com/v2/2020/contract/{self.__contract_address}/abi"
            contract_url = f"https://skynet-api.roninchain.com/ronin/explorer/v2/accounts/{self.__contract_address}"

            # Get contract data from roninchain.com.
            async with self.__http_client.get(abi_url) as abi_response:
                abi_data = await abi_response.json()

            async with self.__http_client.get(contract_url) as contract_response:
                contract_data = await contract_response.json()

            abi = abi_data["result"]["output"]["abi"]

            """
            The contract verifiedName or proxyVersion might not be returned depending of the contract creator.
            Because this application is monitoring only SkyMavis contracts for AxieInfinity, these values are returned.
            If this is no longer the case, an alternative will need to be implemented to verify if the contract is a Proxy.
            The contract_name is not very important and could be set to Unnamed if missing.
            """
            contract_name = contract_data["result"]["contract"]["verifiedName"]
            contract_proxy_version = contract_data["result"]["contract"]["proxyVersion"]
            is_contract_proxy = False if contract_proxy_version == NOT_PROXY_VERSION_NUMBER else True
            implementation_address = await self.__w3.eth.get_storage_at(self.get_checksum_contract_address, self.__eip1967_slot).hex()[24:]

            current_epoch_time = int(time.time() * 1000)

            contract = (
                self.__contract_address,
                contract_name,
                abi,
                is_contract_proxy,
                implementation_address,
                current_epoch_time,
                current_epoch_time,
            )

            # Add the contract to the database.
            logging.info(f"[__add_contract_data] Adding contract {self.__contract_address} ({contract_name}) to the database...")
            await self.__conn.execute(
                '''
                INSERT INTO contracts(
                    contract_address,
                    contract_name,
                    abi,
                    is_proxy,
                    implementation_address,
                    created_at,
                    modified_at                      
                )                       
                ''',
                contract
            )
            logging.info(f"[__add_contract_data] Successfully added contract {self.__contract_address} ({contract_name}) to the database.")
 
        except Exception as e:
            logging.error(f"[__add_contract_data] An unexpected error occured while retrieving contract {self.__contract_address} ({contract_name}) or adding it to the database: {e}")
            raise e  


    def get_event_name(self, topic: str) -> str:
        """
        Returns the event name using the topic.
        """
        if self.__is_proxy:
            return self.__implementation.get_event_name(topic)
        else:
            return self.__contract.get_event_by_topic(topic).name


    def get_event_data(self, topic: str, log: dict) -> dict:
        """
        Returns the decoded log data in a dictionnary.
        """
        event_name = self.get_event_name(topic)

        if self.__is_proxy:
            event_class = getattr(self.__implementation.__contract.events, event_name)
        else:
            event_class = getattr(self.__contract.events, event_name)

        return event_class.process_log(log)
