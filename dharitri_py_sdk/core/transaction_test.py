import re
from pathlib import Path

import pytest

from dharitri_py_sdk.core.address import Address
from dharitri_py_sdk.core.constants import MIN_TRANSACTION_VERSION_THAT_SUPPORTS_OPTIONS
from dharitri_py_sdk.core.errors import BadUsageError, NotEnoughGasError
from dharitri_py_sdk.core.proto.transaction_serializer import ProtoSerializer
from dharitri_py_sdk.core.transaction import Transaction
from dharitri_py_sdk.core.transaction_computer import TransactionComputer
from dharitri_py_sdk.testutils.wallets import load_wallets
from dharitri_py_sdk.wallet import UserSecretKey
from dharitri_py_sdk.wallet.user_pem import UserPEM
from dharitri_py_sdk.wallet.user_verifer import UserVerifier


class NetworkConfig:
    def __init__(self, min_gas_limit: int = 50000) -> None:
        self.min_gas_limit = min_gas_limit
        self.gas_per_data_byte = 1500
        self.gas_price_modifier = 0.01
        self.chain_id = "D"


class TestTransaction:
    wallets = load_wallets()
    alice = wallets["alice"]
    bob = wallets["bob"]
    carol = wallets["carol"]
    transaction_computer = TransactionComputer()

    def test_serialize_for_signing(self):
        sender = Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh")
        receiver = Address.new_from_bech32("drt18h03w0y7qtqwtra3u4f0gu7e3kn2fslj83lqxny39m5c4rwaectswerhd2")

        transaction = Transaction(
            nonce=89,
            sender=sender,
            receiver=receiver,
            value=0,
            gas_limit=50000,
            gas_price=1000000000,
            chain_id="D",
            version=1,
        )
        serialized_tx = self.transaction_computer.compute_bytes_for_signing(transaction)
        assert (
            serialized_tx.decode()
            == r"""{"nonce":89,"value":"0","receiver":"drt18h03w0y7qtqwtra3u4f0gu7e3kn2fslj83lqxny39m5c4rwaectswerhd2","sender":"drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh","gasPrice":1000000000,"gasLimit":50000,"chainID":"D","version":1}"""
        )

        transaction = Transaction(
            nonce=90,
            sender=sender,
            receiver=receiver,
            value=1000000000000000000,
            data=b"hello",
            gas_limit=70000,
            gas_price=1000000000,
            chain_id="D",
            version=1,
        )
        serialized_tx = self.transaction_computer.compute_bytes_for_signing(transaction)
        assert (
            serialized_tx.decode()
            == r"""{"nonce":90,"value":"1000000000000000000","receiver":"drt18h03w0y7qtqwtra3u4f0gu7e3kn2fslj83lqxny39m5c4rwaectswerhd2","sender":"drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh","gasPrice":1000000000,"gasLimit":70000,"data":"aGVsbG8=","chainID":"D","version":1}"""
        )

    def test_with_usernames(self):
        transaction = Transaction(
            chain_id="T",
            sender=Address.new_from_bech32(self.carol.label),
            receiver=Address.new_from_bech32(self.alice.label),
            nonce=204,
            gas_limit=50000,
            sender_username="carol",
            receiver_username="alice",
            value=1000000000000000000,
        )

        transaction.signature = self.carol.secret_key.sign(
            self.transaction_computer.compute_bytes_for_signing(transaction)
        )
        assert (
            transaction.signature.hex()
            == "6e217efb1106be3fbc37065b16491112cb7f1adc78b8860f6d587733776afdce0c9ce7f36f102c5b1fe14a2a4a7844812fa0edb98451deecc8b0225f5250340c"
        )

    def test_compute_transaction_hash(self):
        transaction = Transaction(
            sender=Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"),
            receiver=Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"),
            gas_limit=100000,
            chain_id="D",
            nonce=17243,
            value=1000000000000,
            data=b"testtx",
            version=2,
            signature=bytes.fromhex(
                "2dd7a28b2de2e85e2e07f1b5811bdffa3e1e5cbed6449fe13534fa42464a9101b31f37197545eb145f5b31b3d001b83a1dc1318b2ac3b3f9722f5ff154191e00"
            ),
        )
        tx_hash = self.transaction_computer.compute_transaction_hash(transaction)
        assert tx_hash.hex() == "f35793b8732c959bbce7185cfafaa4b39380ac94a98a74e3c74054598f7bca11"

    def test_compute_transaction_hash_with_usernames(self):
        transaction = Transaction(
            sender=Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"),
            receiver=Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"),
            gas_limit=100000,
            chain_id="D",
            nonce=17244,
            value=1000000000000,
            data=b"testtx",
            version=2,
            sender_username="alice",
            receiver_username="alice",
            signature=bytes.fromhex(
                "3a5c4ee64f1453cef3cebdd3718dd185b81b9343612453da424e31ffc5347cf7e2dd93ce14da887a0a5689d607f887368f665e5c1e70a591553cfab79bec4006"
            ),
        )
        tx_hash = self.transaction_computer.compute_transaction_hash(transaction)
        assert tx_hash.hex() == "bdf6b099a2bafdf05468807936513a2cba3979a4a10b6beab151f27cc3079bd1"

    def test_compute_transaction_fee_insufficient(self):
        transaction = Transaction(
            sender=Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"),
            receiver=Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"),
            gas_limit=50000,
            chain_id="D",
            data=b"toolittlegaslimit",
        )

        with pytest.raises(NotEnoughGasError):
            self.transaction_computer.compute_transaction_fee(transaction, NetworkConfig())

    def test_compute_transaction_fee(self):
        transaction = Transaction(
            sender=Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"),
            receiver=Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"),
            gas_price=500,
            gas_limit=20,
            chain_id="D",
        )

        computed_gas = self.transaction_computer.compute_transaction_fee(transaction, NetworkConfig(min_gas_limit=10))
        assert computed_gas == 5050

    def test_compute_transaction_fee_with_data_field(self):
        transaction = Transaction(
            sender=Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"),
            receiver=Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"),
            gas_price=500,
            gas_limit=12010,
            chain_id="D",
            data=b"testdata",
        )

        computed_gas = self.transaction_computer.compute_transaction_fee(transaction, NetworkConfig(min_gas_limit=10))
        assert computed_gas == 6005000

    def test_compute_transaction_with_guardian_fields(self):
        sender_secret_key_hex = "2bbcdae7e193924fa0d301e7a12c7defc92a93bc5e587cc968f04fcb86022e1c"
        sender_secret_key = UserSecretKey(bytes.fromhex(sender_secret_key_hex))

        transaction = Transaction(
            sender=Address.new_from_bech32("drt1fp4zaxvyc8jh99vauwns99kvs9tn0k6cwrr0zpyz2jvyurcepuhs57mu7a"),
            receiver=Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"),
            gas_limit=139000,
            gas_price=1000000000,
            chain_id="D",
            nonce=2,
            value=1000000000000000000,
            data=b"this is a test transaction",
            version=2,
            options=2,
            guardian=Address.new_from_bech32("drt1nn8apn09vmf72l7kzr3nd90rr5r2q74he7hseghs3v68c5p7ud2q2te2xy"),
            guardian_signature=bytes.fromhex(
                "487150c26d38a01fe19fbe26dac20ec2b42ec3abf5763a47a508e62bcd6ad3437c4d404684442e864a1dbad446dc0f852889a09f0650b5fdb55f4ee18147920d"
            ),
        )

        transaction.signature = sender_secret_key.sign(self.transaction_computer.compute_bytes_for_signing(transaction))
        assert (
            transaction.signature.hex()
            == "4511c3f0f7220932fdfcb4b68b94b5899d149648dd3d3a0051f3be745d95b911cc6845ae9752f722b624dad39f184c65c966ec00bc6cd49acfc28575984d2b00"
        )

        tx_hash = self.transaction_computer.compute_transaction_hash(transaction)
        assert tx_hash.hex() == "f9a56644a7e070fe60be59fea7419da6d83aef0dfea5b6f3a94005b80660f84a"

    # this test was done to mimic the one in drt-chain-go
    def test_compute_transaction_with_dummy_guardian(self):
        alice_private_key_hex = "2bbcdae7e193924fa0d301e7a12c7defc92a93bc5e587cc968f04fcb86022e1c"
        alice_secret_key = UserSecretKey(bytes.fromhex(alice_private_key_hex))

        transaction = Transaction(
            sender=Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"),
            receiver=Address.new_from_bech32("drt18h03w0y7qtqwtra3u4f0gu7e3kn2fslj83lqxny39m5c4rwaectswerhd2"),
            gas_limit=150000,
            chain_id="local-testnet",
            gas_price=1000000000,
            data=b"test data field",
            version=2,
            options=2,
            nonce=92,
            value=123456789000000000000000000000,
            guardian=Address.new_from_bech32("drt1x23lzn8483xs2su4fak0r0dqx6w38enpmmqf2yrkylwq7mfnvyhsmueha6"),
            guardian_signature=bytes([0] * 64),
        )

        transaction.signature = alice_secret_key.sign(self.transaction_computer.compute_bytes_for_signing(transaction))
        assert (
            transaction.signature.hex()
            == "14bbdaf3ece1533aefe874147266fd8f6d7281a571a12d133c7dfb3cda655a8618c1092bc22c4496eaf867c3af3686fc4ae7327485a13c12769fcd589dbc2a0d"
        )

        proto_serializer = ProtoSerializer()
        serialized = proto_serializer.serialize_transaction(transaction)
        assert (
            serialized.hex()
            == "085c120e00018ee90ff6181f3761632000001a203ddf173c9e02c0e58fb1e552f473d98da6a4c3f23c7e034c912ee98a8dddce172a20391f932707a9dfa86d3bcbb3d5d0cc9f25ad0e680fe499f107d844b7e6ea71d5388094ebdc0340f093094a0f746573742064617461206669656c64520d6c6f63616c2d746573746e65745802624014bbdaf3ece1533aefe874147266fd8f6d7281a571a12d133c7dfb3cda655a8618c1092bc22c4496eaf867c3af3686fc4ae7327485a13c12769fcd589dbc2a0d6802722032a3f14cf53c4d0543954f6cf1bda0369d13e661dec095107627dc0f6d33612f7a4000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
        )

        tx_hash = self.transaction_computer.compute_transaction_hash(transaction)
        assert tx_hash.hex() == "5b1a94420f59e687200044233abbddb3056e6921deb82cec706ecbd03003fb93"

    def test_tx_computer_has_options_set(self):
        tx = Transaction(
            sender=Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"),
            receiver=Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"),
            gas_limit=50000,
            chain_id="D",
            options=3,
        )

        assert self.transaction_computer.has_options_set_for_guarded_transaction(tx)
        assert self.transaction_computer.has_options_set_for_hash_signing(tx)

    def test_tx_computer_apply_guardian(self):
        tx = Transaction(
            sender=Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"),
            receiver=Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"),
            gas_limit=200000,
            chain_id="D",
            version=1,
            options=1,
        )

        self.transaction_computer.apply_guardian(
            transaction=tx,
            guardian=Address.new_from_bech32("drt18h03w0y7qtqwtra3u4f0gu7e3kn2fslj83lqxny39m5c4rwaectswerhd2"),
        )

        assert tx.version == 2
        assert tx.options == 3
        assert str(tx.guardian) == "drt18h03w0y7qtqwtra3u4f0gu7e3kn2fslj83lqxny39m5c4rwaectswerhd2"

    def test_sign_transaction_by_hash(self):
        parent = Path(__file__).parent.parent
        pem = UserPEM.from_file(parent / "testutils" / "testwallets" / "alice.pem")

        tx = Transaction(
            sender=Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"),
            receiver=Address.new_from_bech32("drt18h03w0y7qtqwtra3u4f0gu7e3kn2fslj83lqxny39m5c4rwaectswerhd2"),
            value=0,
            gas_limit=50000,
            version=2,
            options=0,
            chain_id="integration tests chain ID",
            nonce=89,
        )

        with pytest.raises(
            Exception,
            match=re.escape(
                "`options` property is not set for hash signing. Please set the least signinficant bit of the `options` property to `1`."
            ),
        ):
            self.transaction_computer.compute_hash_for_signing(tx)

        tx.options = 1
        serialized = self.transaction_computer.compute_hash_for_signing(tx)
        tx.signature = pem.secret_key.sign(serialized)

        assert (
            tx.signature.hex()
            == "17e608f5ae9897b500046cf896cc5ea3de5208e8b42781733a9ae5a0f1ef11a5a0710b30b9df2bcc550fd83a379ffbb5dab20a6d803c755ca969a294f563ac08"
        )

    def test_apply_guardian_with_hash_signing(self):
        tx = Transaction(
            sender=Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"),
            receiver=Address.new_from_bech32("drt18h03w0y7qtqwtra3u4f0gu7e3kn2fslj83lqxny39m5c4rwaectswerhd2"),
            value=0,
            gas_limit=50000,
            version=1,
            chain_id="localnet",
            nonce=89,
        )

        self.transaction_computer.apply_options_for_hash_signing(tx)
        assert tx.version == 2
        assert tx.options == 1

        self.transaction_computer.apply_guardian(transaction=tx, guardian=Address.new_from_bech32(self.carol.label))
        assert tx.version == 2
        assert tx.options == 3

    def test_ensure_transaction_is_valid(self):
        tx = Transaction(
            sender=Address.new_from_bech32(self.bob.label),
            receiver=Address.new_from_bech32(self.bob.label),
            gas_limit=50000,
            chain_id="",
        )

        with pytest.raises(BadUsageError, match="The `chainID` field is not set"):
            self.transaction_computer.compute_bytes_for_signing(tx)

        tx.chain_id = "localnet"
        tx.version = 1
        tx.options = 2
        with pytest.raises(
            BadUsageError,
            match=f"Non-empty transaction options requires transaction version >= {MIN_TRANSACTION_VERSION_THAT_SUPPORTS_OPTIONS}",
        ):
            self.transaction_computer.compute_bytes_for_signing(tx)

        self.transaction_computer.apply_options_for_hash_signing(tx)
        assert tx.version == 2
        assert tx.options == 3

    def test_compute_bytes_for_verifying_signature(self):
        tx = Transaction(
            sender=Address.new_from_bech32(self.alice.label),
            receiver=Address.new_from_bech32(self.bob.label),
            gas_limit=50000,
            chain_id="D",
            nonce=7,
        )

        tx.signature = self.alice.secret_key.sign(self.transaction_computer.compute_bytes_for_signing(tx))

        user_verifier = UserVerifier(self.alice.public_key)
        is_signed_by_alice = user_verifier.verify(
            data=self.transaction_computer.compute_bytes_for_verifying(tx),
            signature=tx.signature,
        )

        wrong_verifier = UserVerifier(self.bob.public_key)
        is_signed_by_bob = wrong_verifier.verify(
            data=self.transaction_computer.compute_bytes_for_verifying(tx),
            signature=tx.signature,
        )

        assert is_signed_by_alice
        assert is_signed_by_bob is False

    def test_compute_bytes_for_verifying_transaction_signed_by_hash(self):
        tx = Transaction(
            sender=Address.new_from_bech32(self.alice.label),
            receiver=Address.new_from_bech32(self.bob.label),
            gas_limit=50000,
            chain_id="D",
            nonce=7,
        )
        self.transaction_computer.apply_options_for_hash_signing(tx)
        tx.signature = self.alice.secret_key.sign(self.transaction_computer.compute_hash_for_signing(tx))

        user_verifier = UserVerifier(self.alice.public_key)
        is_signed_by_alice = user_verifier.verify(
            data=self.transaction_computer.compute_bytes_for_verifying(tx),
            signature=tx.signature,
        )

        wrong_verifier = UserVerifier(self.bob.public_key)
        is_signed_by_bob = wrong_verifier.verify(
            data=self.transaction_computer.compute_bytes_for_verifying(tx),
            signature=tx.signature,
        )

        assert is_signed_by_alice
        assert is_signed_by_bob is False

    def test_transaction_converter(self):
        transaction = Transaction(
            nonce=90,
            value=123456789000000000000000000000,
            sender=Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"),
            receiver=Address.new_from_bech32("drt18h03w0y7qtqwtra3u4f0gu7e3kn2fslj83lqxny39m5c4rwaectswerhd2"),
            sender_username="alice",
            receiver_username="bob",
            gas_price=1000000000,
            gas_limit=80000,
            data=b"hello",
            chain_id="localnet",
        )

        tx_as_dict = transaction.to_dictionary()
        restored_tx = Transaction.new_from_dictionary(tx_as_dict)

        assert transaction == restored_tx

    def test_serialize_tx_with_relayed_v3(self):
        sender = Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh")
        relayer = Address.new_from_bech32("drt18h03w0y7qtqwtra3u4f0gu7e3kn2fslj83lqxny39m5c4rwaectswerhd2")

        transaction = Transaction(
            nonce=89,
            sender=sender,
            receiver=sender,
            value=0,
            gas_limit=50000,
            gas_price=1000000000,
            chain_id="D",
            relayer=relayer,
        )
        serialized_tx = self.transaction_computer.compute_bytes_for_signing(transaction)
        assert (
            serialized_tx.decode()
            == r"""{"nonce":89,"value":"0","receiver":"drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh","sender":"drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh","gasPrice":1000000000,"gasLimit":50000,"chainID":"D","version":2,"relayer":"drt18h03w0y7qtqwtra3u4f0gu7e3kn2fslj83lqxny39m5c4rwaectswerhd2"}"""
        )

    def test_relayed_v3(self):
        alice = Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh")
        bob = Address.new_from_bech32("drt18h03w0y7qtqwtra3u4f0gu7e3kn2fslj83lqxny39m5c4rwaectswerhd2")
        carol = Address(self.carol.public_key.get_bytes())

        transaction = Transaction(
            nonce=90,
            value=123456789000000000000000000000,
            sender=alice,
            receiver=bob,
            sender_username="alice",
            receiver_username="bob",
            gas_price=1000000000,
            gas_limit=80000,
            data=b"hello",
            chain_id="localnet",
        )
        assert not self.transaction_computer.is_relayed_v3_transaction(transaction)

        transaction.relayer = carol
        assert self.transaction_computer.is_relayed_v3_transaction(transaction)


x = TestTransaction()
x.test_compute_bytes_for_verifying_signature()
