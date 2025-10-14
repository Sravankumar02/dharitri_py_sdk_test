from dharitri_py_sdk.core.address import Address
from dharitri_py_sdk.core.transaction import Transaction
from dharitri_py_sdk.core.transaction_computer import TransactionComputer
from dharitri_py_sdk.wallet.keypair import KeyPair
from dharitri_py_sdk.wallet.user_keys import UserSecretKey


def test_create_keypair():
    buffer_hex = "2bbcdae7e193924fa0d301e7a12c7defc92a93bc5e587cc968f04fcb86022e1c"
    buffer = bytes.fromhex(buffer_hex)

    user_secret_key = UserSecretKey(buffer)
    keypair = KeyPair.new_from_bytes(buffer)

    secret_key = keypair.get_secret_key()
    assert secret_key.hex() == buffer_hex
    assert secret_key == user_secret_key

    keypair = KeyPair(secret_key)
    assert keypair.get_secret_key() == user_secret_key
    assert keypair.get_public_key() == user_secret_key.generate_public_key()

    keypair = KeyPair.generate()
    pubkey = keypair.get_public_key()
    secret_key = keypair.get_secret_key()
    assert len(pubkey.get_bytes()) == 32
    assert len(secret_key.get_bytes()) == 32


def test_sign_and_verify_transaction():
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

    buffer_hex = "2bbcdae7e193924fa0d301e7a12c7defc92a93bc5e587cc968f04fcb86022e1c"
    buffer = bytes.fromhex(buffer_hex)
    keypair = KeyPair.new_from_bytes(buffer)

    transaction_computer = TransactionComputer()
    serialized_tx = transaction_computer.compute_bytes_for_signing(tx)

    tx.signature = keypair.sign(serialized_tx)
    assert (
        tx.signature.hex()
        == "bb930c96ae02700d70fd834da7f69bc01a16b4086374c6af6208ef5500996dccdc900e423248364d1a6451ec16b2728da662e0b0260a86caa9d0a9b61c6c2209"
    )
    assert keypair.verify(serialized_tx, tx.signature)
