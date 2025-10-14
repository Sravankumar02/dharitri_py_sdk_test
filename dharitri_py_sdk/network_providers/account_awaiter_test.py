import pytest

from dharitri_py_sdk.core.address import Address
from dharitri_py_sdk.core.transaction import Transaction
from dharitri_py_sdk.core.transaction_computer import TransactionComputer
from dharitri_py_sdk.network_providers.account_awaiter import AccountAwaiter
from dharitri_py_sdk.network_providers.api_network_provider import ApiNetworkProvider
from dharitri_py_sdk.network_providers.errors import (
    ExpectedAccountConditionNotReachedError,
)
from dharitri_py_sdk.network_providers.resources import AccountOnNetwork
from dharitri_py_sdk.testutils.mock_network_provider import (
    MockNetworkProvider,
    TimelinePointMarkCompleted,
    TimelinePointWait,
)
from dharitri_py_sdk.testutils.utils import create_account_rewa_balance
from dharitri_py_sdk.testutils.wallets import load_wallets


class TestAccountAwaiter:
    provider = MockNetworkProvider()
    watcher = AccountAwaiter(
        fetcher=provider,
        polling_interval_in_milliseconds=42,
        timeout_interval_in_milliseconds=42 * 42,
        patience_time_in_milliseconds=0,
    )

    def test_await_on_balance_increase(self):
        alice = Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh")
        # alice account is created with 1000 REWA
        initial_balance = self.provider.get_account(alice).balance

        # adds 7 REWA to the account balance
        self.provider.mock_account_balance_timeline_by_address(
            alice,
            [
                TimelinePointWait(40),
                TimelinePointWait(40),
                TimelinePointWait(45),
                TimelinePointMarkCompleted(),
            ],
        )

        def condition(account: AccountOnNetwork):
            return account.balance == initial_balance + create_account_rewa_balance(7)

        account = self.watcher.await_on_condition(alice, condition)
        assert account.balance == create_account_rewa_balance(1007)

    @pytest.mark.networkInteraction
    def test_await_for_account_balance_increase_on_network(self):
        alice = load_wallets()["alice"]
        alice_address = Address.new_from_bech32(alice.label)
        frank = Address.new_from_bech32("drt10xpcr2cqud9vm6q4axfv64ek63k7xywfcy8zyjp7pvx3kr4cnqlqv3scy7")

        api = ApiNetworkProvider("https://devnet-api.dharitri.org")
        watcher = AccountAwaiter(fetcher=api)
        tx_computer = TransactionComputer()
        value = 100_000

        transaction = Transaction(
            sender=alice_address,
            receiver=frank,
            gas_limit=50000,
            chain_id="D",
            value=value,
        )
        transaction.nonce = api.get_account(alice_address).nonce
        transaction.signature = alice.secret_key.sign(tx_computer.compute_bytes_for_signing(transaction))

        initial_balance = api.get_account(frank).balance

        def condition(account: AccountOnNetwork):
            return account.balance == initial_balance + value

        api.send_transaction(transaction)

        account_on_network = watcher.await_on_condition(frank, condition)
        assert account_on_network.balance == initial_balance + value

    @pytest.mark.networkInteraction
    def test_ensure_error_if_timeout(self):
        alice = load_wallets()["alice"]
        alice_address = Address.new_from_bech32(alice.label)
        bob = Address.new_from_bech32("drt18h03w0y7qtqwtra3u4f0gu7e3kn2fslj83lqxny39m5c4rwaectswerhd2")

        api = ApiNetworkProvider("https://devnet-api.dharitri.org")
        watcher = AccountAwaiter(
            fetcher=api,
            polling_interval_in_milliseconds=1000,
            timeout_interval_in_milliseconds=10000,
        )

        value = 100_000
        transaction = Transaction(
            sender=alice_address,
            receiver=bob,
            gas_limit=50000,
            chain_id="D",
            value=value,
        )
        transaction.nonce = api.get_account(alice_address).nonce

        tx_computer = TransactionComputer()
        transaction.signature = alice.secret_key.sign(tx_computer.compute_bytes_for_signing(transaction))

        initial_balance = api.get_account(bob).balance

        def condition(account: AccountOnNetwork):
            return account.balance == initial_balance + value

        api.send_transaction(transaction)

        with pytest.raises(ExpectedAccountConditionNotReachedError):
            watcher.await_on_condition(bob, condition)
