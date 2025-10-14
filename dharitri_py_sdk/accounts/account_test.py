from pathlib import Path

from dharitri_py_sdk.accounts.account import Account
from dharitri_py_sdk.core.address import Address
from dharitri_py_sdk.core.message import Message
from dharitri_py_sdk.core.transaction import Transaction
from dharitri_py_sdk.wallet.keypair import KeyPair
from dharitri_py_sdk.wallet.user_keys import UserSecretKey

testwallets = Path(__file__).parent.parent / "testutils" / "testwallets"
DUMMY_MNEMONIC = "bread type ride autumn corn maid benefit pole that normal orchard confirm napkin degree arrow guitar offer you enjoy bronze more onion push decorate"
alice = testwallets / "alice.pem"


def test_create_account_from_pem():
    account = Account.new_from_pem(alice)

    assert account.secret_key.get_bytes().hex() == "2bbcdae7e193924fa0d301e7a12c7defc92a93bc5e587cc968f04fcb86022e1c"
    assert account.address.to_bech32() == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"


def test_create_account_from_keystore():
    account = Account.new_from_keystore(testwallets / "withDummyMnemonic.json", "password")

    assert account.secret_key.get_bytes().hex() == "2bbcdae7e193924fa0d301e7a12c7defc92a93bc5e587cc968f04fcb86022e1c"
    assert account.address.to_bech32() == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"


def test_create_account_from_mnemonic():
    account = Account.new_from_mnemonic(DUMMY_MNEMONIC)

    assert account.secret_key.get_bytes().hex() == "2bbcdae7e193924fa0d301e7a12c7defc92a93bc5e587cc968f04fcb86022e1c"
    assert account.address.to_bech32() == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"


def test_create_account_from_keypair():
    secret_key = UserSecretKey.new_from_string("2bbcdae7e193924fa0d301e7a12c7defc92a93bc5e587cc968f04fcb86022e1c")
    keypair = KeyPair(secret_key)
    account = Account.new_from_keypair(keypair)

    assert account.secret_key == secret_key
    assert account.address.to_bech32() == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"


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
        receiver=Address.new_from_bech32("drt18h03w0y7qtqwtra3u4f0gu7e3kn2fslj83lqxny39m5c4rwaectswerhd2"),
        sender=Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"),
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
        == "bb930c96ae02700d70fd834da7f69bc01a16b4086374c6af6208ef5500996dccdc900e423248364d1a6451ec16b2728da662e0b0260a86caa9d0a9b61c6c2209"
    )


def test_sign_message():
    message = Message(
        "hello".encode(),
        address=Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"),
    )

    account = Account.new_from_pem(alice)
    message.signature = account.sign_message(message)

    assert (
        message.signature.hex()
        == "33edba0c691b5a3e8211a5fa63508a4f0c5ba7ac066413ea660e8ec9145c57521d13c304f21bd4687e9f4e118c8df0df6d20ad59b56dffbf749dd2b3b377740f"
    )


def test_sign_tx_by_hash():
    account = Account.new_from_pem(alice)

    tx = Transaction(
        sender=Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"),
        receiver=Address.new_from_bech32("drt18h03w0y7qtqwtra3u4f0gu7e3kn2fslj83lqxny39m5c4rwaectswerhd2"),
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
        == "17e608f5ae9897b500046cf896cc5ea3de5208e8b42781733a9ae5a0f1ef11a5a0710b30b9df2bcc550fd83a379ffbb5dab20a6d803c755ca969a294f563ac08"
    )
