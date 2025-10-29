from pathlib import Path

from dharitri_py_sdk.accounts.account import Account
from dharitri_py_sdk.core.address import Address
from dharitri_py_sdk.core.message import Message
from dharitri_py_sdk.core.transaction import Transaction
from dharitri_py_sdk.wallet.keypair import KeyPair
from dharitri_py_sdk.wallet.user_keys import UserSecretKey

testwallets = Path(__file__).parent.parent / "testutils" / "testwallets"
DUMMY_MNEMONIC = "moral volcano peasant pass circle pen over picture flat shop clap goat never lyrics gather prepare woman film husband gravity behind test tiger improve"
alice = testwallets / "alice.pem"


def test_create_account_from_pem():
    account = Account.new_from_pem(alice)

    assert account.secret_key.get_bytes().hex() == "413f42575f7f26fad3317a778771212fdb80245850981e48b58a4f25e344e8f9"
    assert account.address.to_bech32() == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"


def test_create_account_from_keystore():
    account = Account.new_from_keystore(testwallets / "withDummyMnemonic.json", "password")

    assert account.secret_key.get_bytes().hex() == "413f42575f7f26fad3317a778771212fdb80245850981e48b58a4f25e344e8f9"
    assert account.address.to_bech32() == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"


def test_create_account_from_mnemonic():
    account = Account.new_from_mnemonic(DUMMY_MNEMONIC)

    assert account.secret_key.get_bytes().hex() == "413f42575f7f26fad3317a778771212fdb80245850981e48b58a4f25e344e8f9"
    assert account.address.to_bech32() == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"


def test_create_account_from_keypair():
    secret_key = UserSecretKey.new_from_string("413f42575f7f26fad3317a778771212fdb80245850981e48b58a4f25e344e8f9")
    keypair = KeyPair(secret_key)
    account = Account.new_from_keypair(keypair)

    assert account.secret_key == secret_key
    assert account.address.to_bech32() == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"


def test_account_nonce_holder():
    account = Account.new_from_pem(alice)
    account.nonce = 42
    assert account.get_nonce_then_increment() == 42
    assert account.get_nonce_then_increment() == 43

    account.get_nonce_then_increment()
    account.get_nonce_then_increment()
    account.get_nonce_then_increment()
    assert account.nonce == 47


def test_sign_transaction():
    """
    Also see: https://github.com/TerraDharitri/drt-go-chain/blob/master/examples/construction_test.go
    """

    tx = Transaction(
        nonce=89,
        value=0,
        receiver=Address.new_from_bech32("drt1spyavw0956vq68xj8y4tenjpq2wd5a9p2c6j8gsz7ztyrnpxrruqlqde3c"),
        sender=Address.new_from_bech32("drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"),
        data=None,
        gas_price=1000000000,
        gas_limit=50000,
        chain_id="local-testnet",
        version=1,
        options=0,
    )

    account = Account.new_from_pem(alice)
    tx.signature = account.sign_transaction(tx)
    assert (
        tx.signature.hex()
        == "6d308fe0924019c84d0c5894507435d4eedea1d3f992df5506daed1f2a2ec27e0c8176067c7a71b1680b3fe661c3b726db58fab4c9be52e169d7d4e78fd42a02"
    )


def test_sign_message():
    message = Message(
        "hello".encode(),
        address=Address.new_from_bech32("drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"),
    )

    account = Account.new_from_pem(alice)
    message.signature = account.sign_message(message)
    assert (
        message.signature.hex()
        == "e9ddb76b9df89a4e9d500fc02138c9a2cf8a9e75a3dd52a345eadd87da18682b302a8a915c7776a5919a2d2274a88922ae932e4f600ebf4e164ebd3b16d11d03"
    )


def test_sign_tx_by_hash():
    account = Account.new_from_pem(alice)

    tx = Transaction(
        sender=Address.new_from_bech32("drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"),
        receiver=Address.new_from_bech32("drt1spyavw0956vq68xj8y4tenjpq2wd5a9p2c6j8gsz7ztyrnpxrruqlqde3c"),
        value=0,
        gas_limit=50000,
        version=2,
        options=1,
        chain_id="integration tests chain ID",
        nonce=89,
    )

    tx.signature = account.sign_transaction(tx)

    assert (
        tx.signature.hex()
        == "97500cef697c580695ddd2f589458bf1041da3a5a8e9217d497a84ede171d99236c71cdabb4b2abc82322d94a757338ca320a3016c7bb443ac6284cc4af9390f"
    )
