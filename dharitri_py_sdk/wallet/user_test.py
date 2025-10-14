import json
from pathlib import Path

import pytest

from dharitri_py_sdk.core import (
    Address,
    Message,
    MessageComputer,
    Transaction,
    TransactionComputer,
)
from dharitri_py_sdk.wallet.crypto.randomness import Randomness
from dharitri_py_sdk.wallet.user_keys import UserSecretKey
from dharitri_py_sdk.wallet.user_pem import UserPEM
from dharitri_py_sdk.wallet.user_signer import UserSigner
from dharitri_py_sdk.wallet.user_verifer import UserVerifier
from dharitri_py_sdk.wallet.user_wallet import UserWallet

testwallets = Path(__file__).parent.parent / "testutils" / "testwallets"
DUMMY_MNEMONIC = "bread type ride autumn corn maid benefit pole that normal orchard confirm napkin degree arrow guitar offer you enjoy bronze more onion push decorate"


def test_user_secret_key_create():
    buffer_hex = "2bbcdae7e193924fa0d301e7a12c7defc92a93bc5e587cc968f04fcb86022e1c"
    buffer = bytes.fromhex(buffer_hex)
    secret_key = UserSecretKey(buffer)
    secret_key_from_string = UserSecretKey.new_from_string(buffer_hex)

    assert secret_key.hex() == buffer_hex
    assert secret_key_from_string.hex() == buffer_hex


def test_user_secret_key_generate_public_key():
    assert (
        UserSecretKey.new_from_string("2bbcdae7e193924fa0d301e7a12c7defc92a93bc5e587cc968f04fcb86022e1c")
        .generate_public_key()
        .hex()
        == "391f932707a9dfa86d3bcbb3d5d0cc9f25ad0e680fe499f107d844b7e6ea71d5"
    )
    assert (
        UserSecretKey.new_from_string("8928add00f0d168620a76ec7af31a92f957038a1a2ed75778a4243248d319f2f")
        .generate_public_key()
        .hex()
        == "3ddf173c9e02c0e58fb1e552f473d98da6a4c3f23c7e034c912ee98a8dddce17"
    )
    assert (
        UserSecretKey.new_from_string("5aa2311a2274ff47cc804f12a4e8b28cf74650a0d1efcb8175b90eda4e3e6b4c")
        .generate_public_key()
        .hex()
        == "b05fe535c27f46911f74f8b7f2051c54f792fca08c7ab23c53e77ececd2cd928"
    )


def test_user_signer_from_pem_file():
    pubkey = UserSigner.from_pem_file(testwallets / "alice.pem", 0).get_pubkey()
    assert Address(pubkey.buffer, "drt").to_bech32() == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"

    pubkey = UserSigner.from_pem_file(testwallets / "bob.pem", 0).get_pubkey()
    assert Address(pubkey.buffer, "drt").to_bech32() == "drt18h03w0y7qtqwtra3u4f0gu7e3kn2fslj83lqxny39m5c4rwaectswerhd2"

    pubkey = UserSigner.from_pem_file(testwallets / "carol.pem", 0).get_pubkey()
    assert Address(pubkey.buffer, "drt").to_bech32() == "drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q"


def test_load_signers_from_pem():
    signers = UserSigner.from_pem_file_all(testwallets / "multipleUserKeys.pem")

    assert len(signers) == 3
    assert (
        Address(signers[0].get_pubkey().buffer, "drt").to_bech32()
        == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"
    )
    assert (
        Address(signers[1].get_pubkey().buffer, "drt").to_bech32()
        == "drt18h03w0y7qtqwtra3u4f0gu7e3kn2fslj83lqxny39m5c4rwaectswerhd2"
    )
    assert (
        Address(signers[2].get_pubkey().buffer, "drt").to_bech32()
        == "drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q"
    )


def test_user_wallet_to_keyfile_object_using_known_test_wallets_with_their_randomness():
    alice_secret_key = UserSecretKey.new_from_string("2bbcdae7e193924fa0d301e7a12c7defc92a93bc5e587cc968f04fcb86022e1c")
    alice_wallet = UserWallet.from_secret_key(
        alice_secret_key,
        "password",
        Randomness(
            salt=bytes.fromhex("2d17c9eda95babeb259e2ae8084233621251a3159cb0754e9d8abd119decbffe"),
            iv=bytes.fromhex("e37ea68b5d7073959c99847797274d17"),
            id="4fb08a12-5173-4db8-ba50-4cb2d7e52803",
        ),
    )

    bob_secret_key = UserSecretKey.new_from_string("8928add00f0d168620a76ec7af31a92f957038a1a2ed75778a4243248d319f2f")
    bob_wallet = UserWallet.from_secret_key(
        bob_secret_key,
        "password",
        Randomness(
            salt=bytes.fromhex("0ed454c339c031d6c5aeba5010a322085eef82448cde18559d6b16bac87d5fb0"),
            iv=bytes.fromhex("f5c7363ebd7042b5f7b77854fb7ec0d6"),
            id="ab35898c-d9c8-4890-ad31-0fa88459ba6b",
        ),
    )

    carol_secret_key = UserSecretKey.new_from_string("5aa2311a2274ff47cc804f12a4e8b28cf74650a0d1efcb8175b90eda4e3e6b4c")
    carol_wallet = UserWallet.from_secret_key(
        carol_secret_key,
        "password",
        Randomness(
            salt=bytes.fromhex("dc37a3fa33a0f56167060c74068aabf38b7a34d11d31540662a793fa03eb5604"),
            iv=bytes.fromhex("45bb55a60a79554ec8822220da0a66b4"),
            id="7858d06a-3249-4637-87e6-4c344c6df786",
        ),
    )

    alice_saved_path = testwallets / "alice.saved.json"
    bob_saved_path = testwallets / "bob.saved.json"
    carol_saved_path = testwallets / "carol.saved.json"

    alice_wallet.save(alice_saved_path, "drt")
    bob_wallet.save(bob_saved_path, "drt")
    carol_wallet.save(carol_saved_path, "drt")

    assert alice_saved_path.read_text().strip() == (testwallets / "alice.json").read_text().strip()
    assert bob_saved_path.read_text().strip() == (testwallets / "bob.json").read_text().strip()
    assert carol_saved_path.read_text().strip() == (testwallets / "carol.json").read_text().strip()

    alice_saved_path.unlink()
    bob_saved_path.unlink()
    carol_saved_path.unlink()


def test_user_wallet_encrypt_then_decrypt():
    alice_secret_key = UserSecretKey.new_from_string("2bbcdae7e193924fa0d301e7a12c7defc92a93bc5e587cc968f04fcb86022e1c")
    alice_wallet = UserWallet.from_secret_key(alice_secret_key, "password")
    alice_keyfile_object = alice_wallet.to_dict("drt")
    decrypted_secret_key = UserWallet.decrypt_secret_key(alice_keyfile_object, "password")
    assert decrypted_secret_key.buffer == alice_secret_key.buffer

    bob_secret_key = UserSecretKey.new_from_string("b8ca6f8203fb4b545a8e83c5384da033c415db155b53fb5b8eba7ff5a039d639")
    bob_wallet = UserWallet.from_secret_key(bob_secret_key, "password")
    bob_keyfile_object = bob_wallet.to_dict("drt")
    decrypted_secret_key = UserWallet.decrypt_secret_key(bob_keyfile_object, "password")
    assert decrypted_secret_key.buffer == bob_secret_key.buffer

    carol_secret_key = UserSecretKey.new_from_string("e253a571ca153dc2aee845819f74bcc9773b0586edead15a94cb7235a5027436")
    carol_wallet = UserWallet.from_secret_key(carol_secret_key, "password")
    carol_keyfile_object = carol_wallet.to_dict("drt")
    decrypted_secret_key = UserWallet.decrypt_secret_key(carol_keyfile_object, "password")
    assert decrypted_secret_key.buffer == carol_secret_key.buffer


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

    signer = UserSigner.from_pem_file(testwallets / "alice.pem")
    verifier = UserVerifier.from_address(
        Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh")
    )
    transaction_computer = TransactionComputer()

    tx.signature = signer.sign(transaction_computer.compute_bytes_for_signing(tx))
    assert (
        tx.signature.hex()
        == "bb930c96ae02700d70fd834da7f69bc01a16b4086374c6af6208ef5500996dccdc900e423248364d1a6451ec16b2728da662e0b0260a86caa9d0a9b61c6c2209"
    )
    assert verifier.verify(transaction_computer.compute_bytes_for_signing(tx), tx.signature)


def test_sign_message():
    message = Message(
        "hello".encode(),
        address=Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"),
    )
    message_computer = MessageComputer()

    signer = UserSigner.from_pem_file(testwallets / "alice.pem")
    verifier = UserVerifier.from_address(
        Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh")
    )

    message.signature = signer.sign(message_computer.compute_bytes_for_signing(message))
    assert (
        message.signature.hex()
        == "33edba0c691b5a3e8211a5fa63508a4f0c5ba7ac066413ea660e8ec9145c57521d13c304f21bd4687e9f4e118c8df0df6d20ad59b56dffbf749dd2b3b377740f"
    )
    assert verifier.verify(message_computer.compute_bytes_for_signing(message), message.signature)


def test_user_pem_save():
    path = testwallets / "alice.pem"
    path_saved = path.with_suffix(".saved")
    content_expected = path.read_text().strip()

    pem = UserPEM.from_file(path)
    pem.save(path_saved)
    content_actual = path_saved.read_text().strip()

    assert content_actual == content_expected
    path_saved.unlink()


def test_load_secret_key_but_without_kind_field():
    keystore_path = testwallets / "withoutKind.json"
    secret_key = UserWallet.load_secret_key(keystore_path, "password")
    actual_address = (secret_key.generate_public_key().to_address("drt")).to_bech32()
    assert actual_address == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"


def test_load_secret_key_with_unecessary_address_index():
    keystore_path = testwallets / "alice.json"

    with pytest.raises(Exception, match="address_index must not be provided when kind == 'secretKey'"):
        UserWallet.load_secret_key(keystore_path, "password", 42)


def test_create_keystore_file_with_mnemonic():
    wallet = UserWallet.from_mnemonic(DUMMY_MNEMONIC, "password")
    keyfile_object = wallet.to_dict()

    assert keyfile_object["version"] == 4
    assert keyfile_object["kind"] == "mnemonic"
    assert "bech32" not in keyfile_object


def test_create_keystore_with_mnemonic_with_randomness():
    expected_dummy_wallet_json = (testwallets / "withDummyMnemonic.json").read_text()
    expected_dummy_wallet_dict = json.loads(expected_dummy_wallet_json)

    randomness = Randomness(
        id="22efac61-f898-4682-9b96-2e4fb49f56d5",
        iv=bytes.fromhex("69f26c6e4181ebfbce9de4080122af15"),
        salt=bytes.fromhex("a3c74d0544a697f3d032da820627f95db417f13a86ec8468bba2acd116c34adf"),
    )

    wallet = UserWallet.from_mnemonic(DUMMY_MNEMONIC, "password", randomness)
    wallet_dict = wallet.to_dict()

    assert wallet_dict == expected_dummy_wallet_dict


def test_load_secret_key_with_mnemonic():
    keystore_path = testwallets / "withDummyMnemonic.json"

    assert (
        UserWallet.load_secret_key(keystore_path, "password", 0).generate_public_key().to_address("drt").to_bech32()
        == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"
    )
    assert (
        UserWallet.load_secret_key(keystore_path, "password", 1).generate_public_key().to_address("drt").to_bech32()
        == "drt1tzkwpg0et0s7fp46a7je9h0gv2v55t9mamqrhgja7wypp4yf5d0se3nzyj"
    )
    assert (
        UserWallet.load_secret_key(keystore_path, "password", 2).generate_public_key().to_address("drt").to_bech32()
        == "drt15hpu70r43r3hx9evqmu2z04097ye5t0jgrw3lhxw5rnge0k89nlsh83ydx"
    )


def test_decrypt_secret_key_with_keystore_mnemonic():
    user_wallet = UserWallet.from_mnemonic(DUMMY_MNEMONIC, "")
    mnemonic_json = user_wallet.to_dict()

    with pytest.raises(Exception, match="Expected kind to be secretKey, but it was mnemonic"):
        UserWallet.decrypt_secret_key(mnemonic_json, "")
