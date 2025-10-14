from pathlib import Path

from dharitri_py_sdk.core.address import Address
from dharitri_py_sdk.core.transactions_factory_config import TransactionsFactoryConfig
from dharitri_py_sdk.validators.validators_signers import ValidatorsSigners
from dharitri_py_sdk.validators.validators_transactions_factory import (
    ValidatorsTransactionsFactory,
)
from dharitri_py_sdk.wallet.validator_keys import ValidatorPublicKey


class TestValidatorsTransactionsFactory:
    testdata = Path(__file__).parent.parent / "testutils" / "testdata"
    testwallets = Path(__file__).parent.parent / "testutils" / "testwallets"
    validators_file = testwallets / "validators.pem"

    alice = Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh")
    reward_address = Address.new_from_bech32("drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q")

    validator_pubkey = ValidatorPublicKey.from_string(
        "d3e0427c22ff9cc80ef4156f976644cfa25c54e5a69ed199132053f8cbbfddd4eb15a2f732a3c9b392169c8b1d060e0b5ab0d88b4dd7b4010fa051a17ef81bdbace5e68025965b00bf48e14a9ec8d8e2a8bcc9e62f97ddac3268f6b805f7b80e"
    )

    factory = ValidatorsTransactionsFactory(TransactionsFactoryConfig("D"))

    def test_create_transaction_for_staking_using_path_to_validators_file(self):
        transaction = self.factory.create_transaction_for_staking(
            sender=self.alice,
            validators_file=self.validators_file,
            amount=2500000000000000000000,
            rewards_address=self.reward_address,
        )

        assert transaction.sender.to_bech32() == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
        assert transaction.value == 2500000000000000000000
        assert transaction.nonce == 0
        assert transaction.gas_limit == 11029500
        assert transaction.chain_id == "D"
        assert transaction.version == 2
        assert transaction.options == 0
        assert (
            transaction.data.decode()
            == "stake@02@d3e0427c22ff9cc80ef4156f976644cfa25c54e5a69ed199132053f8cbbfddd4eb15a2f732a3c9b392169c8b1d060e0b5ab0d88b4dd7b4010fa051a17ef81bdbace5e68025965b00bf48e14a9ec8d8e2a8bcc9e62f97ddac3268f6b805f7b80e@900befe131dfdb8b40bfbf048ebb7f12b57d2d45bedd141bca848f343c7ac8c431af9faacbaaac1cf5eca9827aef9d06@b0b6349b3f693e08c433970d10efb2fe943eac4057a945146bee5fd163687f4e1800d541aa0f11bf9e4cb6552f512e126068e68eb471d18fcc477ddfe0b9b3334f34e30d8b7b2c08f914f4ae54454f75fb28922ba9fd28785bcadc627031fa8a@f1fdb60bab285322ffaff8ee27b2b90f03a71d1f172e077941f2212e7a27588ed873faf3bd7f37a8205fda788e1f3d88@b05fe535c27f46911f74f8b7f2051c54f792fca08c7ab23c53e77ececd2cd928"
        )

    def test_create_transaction_for_staking_using_validators_file(self):
        validators_file = ValidatorsSigners.new_from_pem(self.validators_file)

        transaction = self.factory.create_transaction_for_staking(
            sender=self.alice,
            validators_file=validators_file,
            amount=2500000000000000000000,
            rewards_address=self.reward_address,
        )

        assert transaction.sender.to_bech32() == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
        assert transaction.value == 2500000000000000000000
        assert transaction.nonce == 0
        assert transaction.gas_limit == 11029500
        assert transaction.chain_id == "D"
        assert transaction.version == 2
        assert transaction.options == 0
        assert (
            transaction.data.decode()
            == "stake@02@d3e0427c22ff9cc80ef4156f976644cfa25c54e5a69ed199132053f8cbbfddd4eb15a2f732a3c9b392169c8b1d060e0b5ab0d88b4dd7b4010fa051a17ef81bdbace5e68025965b00bf48e14a9ec8d8e2a8bcc9e62f97ddac3268f6b805f7b80e@900befe131dfdb8b40bfbf048ebb7f12b57d2d45bedd141bca848f343c7ac8c431af9faacbaaac1cf5eca9827aef9d06@b0b6349b3f693e08c433970d10efb2fe943eac4057a945146bee5fd163687f4e1800d541aa0f11bf9e4cb6552f512e126068e68eb471d18fcc477ddfe0b9b3334f34e30d8b7b2c08f914f4ae54454f75fb28922ba9fd28785bcadc627031fa8a@f1fdb60bab285322ffaff8ee27b2b90f03a71d1f172e077941f2212e7a27588ed873faf3bd7f37a8205fda788e1f3d88@b05fe535c27f46911f74f8b7f2051c54f792fca08c7ab23c53e77ececd2cd928"
        )

    def test_create_transaction_for_topping_up(self):
        transaction = self.factory.create_transaction_for_topping_up(
            sender=self.alice,
            amount=2500000000000000000000,
        )

        assert transaction.sender.to_bech32() == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
        assert transaction.value == 2500000000000000000000
        assert transaction.nonce == 0
        assert transaction.gas_limit == 5057500
        assert transaction.chain_id == "D"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.data.decode() == "stake"

    def test_create_transaction_for_unstaking(self):
        transaction = self.factory.create_transaction_for_unstaking(
            sender=self.alice,
            public_keys=[self.validator_pubkey],
        )

        assert transaction.sender.to_bech32() == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
        assert transaction.value == 0
        assert transaction.nonce == 0
        assert transaction.gas_limit == 5350000
        assert transaction.chain_id == "D"
        assert transaction.version == 2
        assert transaction.options == 0
        assert (
            transaction.data.decode()
            == "unStake@d3e0427c22ff9cc80ef4156f976644cfa25c54e5a69ed199132053f8cbbfddd4eb15a2f732a3c9b392169c8b1d060e0b5ab0d88b4dd7b4010fa051a17ef81bdbace5e68025965b00bf48e14a9ec8d8e2a8bcc9e62f97ddac3268f6b805f7b80e"
        )

    def test_create_transaction_for_unbonding(self):
        transaction = self.factory.create_transaction_for_unbonding(
            sender=self.alice,
            public_keys=[self.validator_pubkey],
        )

        assert transaction.sender.to_bech32() == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
        assert transaction.value == 0
        assert transaction.nonce == 0
        assert transaction.gas_limit == 5348500
        assert transaction.chain_id == "D"
        assert transaction.version == 2
        assert transaction.options == 0
        assert (
            transaction.data.decode()
            == "unBond@d3e0427c22ff9cc80ef4156f976644cfa25c54e5a69ed199132053f8cbbfddd4eb15a2f732a3c9b392169c8b1d060e0b5ab0d88b4dd7b4010fa051a17ef81bdbace5e68025965b00bf48e14a9ec8d8e2a8bcc9e62f97ddac3268f6b805f7b80e"
        )

    def test_create_transaction_for_unjailing(self):
        transaction = self.factory.create_transaction_for_unjailing(
            sender=self.alice,
            public_keys=[self.validator_pubkey],
            amount=2500000000000000000000,
        )

        assert transaction.sender.to_bech32() == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
        assert transaction.value == 2500000000000000000000
        assert transaction.nonce == 0
        assert transaction.gas_limit == 5348500
        assert transaction.chain_id == "D"
        assert transaction.version == 2
        assert transaction.options == 0
        assert (
            transaction.data.decode()
            == "unJail@d3e0427c22ff9cc80ef4156f976644cfa25c54e5a69ed199132053f8cbbfddd4eb15a2f732a3c9b392169c8b1d060e0b5ab0d88b4dd7b4010fa051a17ef81bdbace5e68025965b00bf48e14a9ec8d8e2a8bcc9e62f97ddac3268f6b805f7b80e"
        )

    def test_create_transaction_for_changing_rewards_address(self):
        transaction = self.factory.create_transaction_for_changing_rewards_address(
            sender=self.alice,
            rewards_address=self.reward_address,
        )

        assert transaction.sender.to_bech32() == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
        assert transaction.value == 0
        assert transaction.nonce == 0
        assert transaction.gas_limit == 5176000
        assert transaction.chain_id == "D"
        assert transaction.version == 2
        assert transaction.options == 0
        assert (
            transaction.data.decode()
            == "changeRewardAddress@b05fe535c27f46911f74f8b7f2051c54f792fca08c7ab23c53e77ececd2cd928"
        )

    def test_create_transaction_for_claiming(self):
        transaction = self.factory.create_transaction_for_claiming(sender=self.alice)

        assert transaction.sender.to_bech32() == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
        assert transaction.value == 0
        assert transaction.nonce == 0
        assert transaction.gas_limit == 5057500
        assert transaction.chain_id == "D"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.data.decode() == "claim"

    def test_create_transaction_for_unstaking_nodes(self):
        transaction = self.factory.create_transaction_for_unstaking_nodes(
            sender=self.alice,
            public_keys=[self.validator_pubkey],
        )

        assert transaction.sender.to_bech32() == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
        assert transaction.value == 0
        assert transaction.nonce == 0
        assert transaction.gas_limit == 5357500
        assert transaction.chain_id == "D"
        assert transaction.version == 2
        assert transaction.options == 0
        assert (
            transaction.data.decode()
            == "unStakeNodes@d3e0427c22ff9cc80ef4156f976644cfa25c54e5a69ed199132053f8cbbfddd4eb15a2f732a3c9b392169c8b1d060e0b5ab0d88b4dd7b4010fa051a17ef81bdbace5e68025965b00bf48e14a9ec8d8e2a8bcc9e62f97ddac3268f6b805f7b80e"
        )

    def test_create_transaction_for_unstaking_tokens(self):
        transaction = self.factory.create_transaction_for_unstaking_tokens(
            sender=self.alice,
            amount=11000000000000000000,
        )

        assert transaction.sender.to_bech32() == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
        assert transaction.value == 0
        assert transaction.nonce == 0
        assert transaction.gas_limit == 5095000
        assert transaction.chain_id == "D"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.data.decode() == "unStakeTokens@98a7d9b8314c0000"

    def test_create_transaction_for_unbonding_nodes(self):
        transaction = self.factory.create_transaction_for_unbonding_nodes(
            sender=self.alice,
            public_keys=[self.validator_pubkey],
        )

        assert transaction.sender.to_bech32() == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
        assert transaction.value == 0
        assert transaction.nonce == 0
        assert transaction.gas_limit == 5356000
        assert transaction.chain_id == "D"
        assert transaction.version == 2
        assert transaction.options == 0
        assert (
            transaction.data.decode()
            == "unBondNodes@d3e0427c22ff9cc80ef4156f976644cfa25c54e5a69ed199132053f8cbbfddd4eb15a2f732a3c9b392169c8b1d060e0b5ab0d88b4dd7b4010fa051a17ef81bdbace5e68025965b00bf48e14a9ec8d8e2a8bcc9e62f97ddac3268f6b805f7b80e"
        )

    def test_create_transaction_for_unbonding_tokens(self):
        transaction = self.factory.create_transaction_for_unbonding_tokens(
            sender=self.alice,
            amount=20000000000000000000,
        )

        assert transaction.sender.to_bech32() == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
        assert transaction.value == 0
        assert transaction.nonce == 0
        assert transaction.gas_limit == 5096500
        assert transaction.chain_id == "D"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.data.decode() == "unBondTokens@01158e460913d00000"

    def test_create_transaction_for_cleaning_registered_data(self):
        transaction = self.factory.create_transaction_for_cleaning_registered_data(sender=self.alice)

        assert transaction.sender.to_bech32() == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
        assert transaction.value == 0
        assert transaction.nonce == 0
        assert transaction.gas_limit == 5078500
        assert transaction.chain_id == "D"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.data.decode() == "cleanRegisteredData"

    def test_create_transaction_for_restaking_unstaked_nodes(self):
        transaction = self.factory.create_transaction_for_restaking_unstaked_nodes(
            sender=self.alice,
            public_keys=[self.validator_pubkey],
        )

        assert transaction.sender.to_bech32() == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
        assert transaction.value == 0
        assert transaction.nonce == 0
        assert transaction.gas_limit == 5369500
        assert transaction.chain_id == "D"
        assert transaction.version == 2
        assert transaction.options == 0
        assert (
            transaction.data.decode()
            == "reStakeUnStakedNodes@d3e0427c22ff9cc80ef4156f976644cfa25c54e5a69ed199132053f8cbbfddd4eb15a2f732a3c9b392169c8b1d060e0b5ab0d88b4dd7b4010fa051a17ef81bdbace5e68025965b00bf48e14a9ec8d8e2a8bcc9e62f97ddac3268f6b805f7b80e"
        )
