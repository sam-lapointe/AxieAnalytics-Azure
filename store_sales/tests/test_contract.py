import pytest
from store_sales.contract import Contract, ContractNotFoundError, EventNotFoundError


# TODO: Test Contract.create() and also for infinite recursion


# TODO: Test Contract.__get_contract_data() when contract not in database and in database


# TODO: Test Contract.__get_contract_data for ContractNotFoundError


# TODO Test __add_contract_data for fetching and storing contract


# TODO Test __add_contract_data for UniqueViolationError


# TODO Test get_contract_address


# TODO Test get_event_name


# TODO Test get_event_data


# TODO Test get_event_signature_hash


# TODO Test get_event_signature_hash for EventNotFoundError