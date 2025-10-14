from dharitri_py_sdk.core.address import Address
from dharitri_py_sdk.core.proto.transaction_serializer import ProtoSerializer
from dharitri_py_sdk.core.transaction import Transaction
from dharitri_py_sdk.core.transaction_computer import TransactionComputer
from dharitri_py_sdk.testutils.wallets import load_wallets


class TestProtoSerializer:
    wallets = load_wallets()
    alice = wallets["alice"]
    bob = wallets["bob"]
    carol = wallets["carol"]
    proto_serializer = ProtoSerializer()
    transaction_computer = TransactionComputer()

    def test_serialize_tx_no_data_no_value(self):
        transaction = Transaction(
            sender=Address.new_from_bech32(self.alice.label),
            receiver=Address.new_from_bech32(self.bob.label),
            gas_limit=50000,
            chain_id="local-testnet",
            nonce=89,
            value=0,
        )
        transaction.signature = self.alice.secret_key.sign(
            self.transaction_computer.compute_bytes_for_signing(transaction)
        )

        serialized_transaction = self.proto_serializer.serialize_transaction(transaction)
        assert (
            serialized_transaction.hex()
            == "0859120200001a203ddf173c9e02c0e58fb1e552f473d98da6a4c3f23c7e034c912ee98a8dddce172a20391f932707a9dfa86d3bcbb3d5d0cc9f25ad0e680fe499f107d844b7e6ea71d5388094ebdc0340d08603520d6c6f63616c2d746573746e657458026240129faad6b4222905addd10a2b49941f0a0f559de52e78af98752916cd470980527f4822a8503ded124f6a54f2801c2617c1922a6d0d2c35c33daa437311a4903"
        )

    def test_serialize_tx_with_data_no_value(self):
        transaction = Transaction(
            sender=Address.new_from_bech32(self.alice.label),
            receiver=Address.new_from_bech32(self.bob.label),
            gas_limit=80000,
            chain_id="local-testnet",
            data=b"hello",
            nonce=90,
        )
        transaction.signature = self.alice.secret_key.sign(
            self.transaction_computer.compute_bytes_for_signing(transaction)
        )

        serialized_transaction = self.proto_serializer.serialize_transaction(transaction)
        assert (
            serialized_transaction.hex()
            == "085a120200001a203ddf173c9e02c0e58fb1e552f473d98da6a4c3f23c7e034c912ee98a8dddce172a20391f932707a9dfa86d3bcbb3d5d0cc9f25ad0e680fe499f107d844b7e6ea71d5388094ebdc034080f1044a0568656c6c6f520d6c6f63616c2d746573746e65745802624032290b79b021945a6650c5f38bcc8bf70f025323598396eaae68447912a84b5bc07897cf5261c48de1b0ab588148811cc394a9462c65372c8dfed1e245951807"
        )

    def test_serialize_tx_with_data_and_value(self):
        transaction = Transaction(
            sender=Address.new_from_bech32(self.alice.label),
            receiver=Address.new_from_bech32(self.bob.label),
            gas_limit=100000,
            chain_id="local-testnet",
            nonce=92,
            data=b"for the spaceship",
            value=123456789000000000000000000000,
        )
        transaction.signature = self.alice.secret_key.sign(
            self.transaction_computer.compute_bytes_for_signing(transaction)
        )

        serialized_transaction = self.proto_serializer.serialize_transaction(transaction)
        assert (
            serialized_transaction.hex()
            == "085c120e00018ee90ff6181f3761632000001a203ddf173c9e02c0e58fb1e552f473d98da6a4c3f23c7e034c912ee98a8dddce172a20391f932707a9dfa86d3bcbb3d5d0cc9f25ad0e680fe499f107d844b7e6ea71d5388094ebdc0340a08d064a11666f722074686520737061636573686970520d6c6f63616c2d746573746e65745802624061deaf3566fc651e5d50ae8f8989771c149077b8f721e02e886be66f013be4e4ae1eadc6d36d54ce0d3899b34db6e6198d01f7b155243305fb49199f21937609"
        )

    def test_serialize_tx_with_nonce_zero(self):
        transaction = Transaction(
            sender=Address.new_from_bech32(self.alice.label),
            receiver=Address.new_from_bech32(self.bob.label),
            chain_id="local-testnet",
            gas_limit=80000,
            nonce=0,
            value=0,
            data=b"hello",
            version=1,
        )
        transaction.signature = self.alice.secret_key.sign(
            self.transaction_computer.compute_bytes_for_signing(transaction)
        )

        serialized_transaction = self.proto_serializer.serialize_transaction(transaction)
        assert (
            serialized_transaction.hex()
            == "120200001a203ddf173c9e02c0e58fb1e552f473d98da6a4c3f23c7e034c912ee98a8dddce172a20391f932707a9dfa86d3bcbb3d5d0cc9f25ad0e680fe499f107d844b7e6ea71d5388094ebdc034080f1044a0568656c6c6f520d6c6f63616c2d746573746e65745801624024b30a91becdbba0dddc74886d52253a221ed2c381da0c6d7ea4c6482075b577c1b105c588ba8ec9442182b345e3cda975ecfc3785481ad44eb2dfd0464aee00"
        )

    def test_serialized_tx_with_usernames(self):
        transaction = Transaction(
            sender=Address.new_from_bech32(self.carol.label),
            receiver=Address.new_from_bech32(self.alice.label),
            gas_limit=50000,
            chain_id="T",
            nonce=204,
            value=1000000000000000000,
            sender_username="carol",
            receiver_username="alice",
        )
        transaction.signature = self.carol.secret_key.sign(
            self.transaction_computer.compute_bytes_for_signing(transaction)
        )

        serialized_transaction = self.proto_serializer.serialize_transaction(transaction)
        assert (
            serialized_transaction.hex()
            == "08cc011209000de0b6b3a76400001a20391f932707a9dfa86d3bcbb3d5d0cc9f25ad0e680fe499f107d844b7e6ea71d52205616c6963652a20b05fe535c27f46911f74f8b7f2051c54f792fca08c7ab23c53e77ececd2cd92832056361726f6c388094ebdc0340d08603520154580262406e217efb1106be3fbc37065b16491112cb7f1adc78b8860f6d587733776afdce0c9ce7f36f102c5b1fe14a2a4a7844812fa0edb98451deecc8b0225f5250340c"
        )
