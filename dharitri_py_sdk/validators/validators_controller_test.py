from pathlib import Path

from dharitri_py_sdk.accounts.account import Account
from dharitri_py_sdk.core.address import Address
from dharitri_py_sdk.validators.validators_controller import ValidatorsController
from dharitri_py_sdk.validators.validators_signers import ValidatorsSigners
from dharitri_py_sdk.wallet.validator_keys import ValidatorPublicKey


class TestValidatorsController:
    testdata = Path(__file__).parent.parent / "testutils" / "testdata"
    testwallets = Path(__file__).parent.parent / "testutils" / "testwallets"
    validators_file = testwallets / "validators.pem"

    alice = Account.new_from_pem(testwallets / "alice.pem")
    reward_address = Address.new_from_bech32("drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q")

    validator_pubkey = ValidatorPublicKey.from_string(
        "d3e0427c22ff9cc80ef4156f976644cfa25c54e5a69ed199132053f8cbbfddd4eb15a2f732a3c9b392169c8b1d060e0b5ab0d88b4dd7b4010fa051a17ef81bdbace5e68025965b00bf48e14a9ec8d8e2a8bcc9e62f97ddac3268f6b805f7b80e"
    )

    controller = ValidatorsController(chain_id="localnet")

    def test_create_transaction_for_staking_using_path_to_validators_file(self):
        transaction = self.controller.create_transaction_for_staking(
            sender=self.alice,
            nonce=self.alice.nonce,
            validators_file=self.validators_file,
            amount=2500000000000000000000,
            rewards_address=self.reward_address,
        )

        assert transaction.sender.to_bech32() == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
        assert transaction.value == 2500000000000000000000
        assert transaction.nonce == 0
        assert transaction.gas_limit == 11029500
        assert transaction.chain_id == "localnet"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.guardian is None
        assert transaction.relayer is None
        assert (
            transaction.signature.hex()
            == "b4b6ee45f8a1d882ebef9cb2044f2833280f96bea4dec6632db69020e4927764d49ecdb47fc3abc9e9d96f3f61490d5dcdde4ea768d0475f52fac2b8eb02d705"
        )
        assert (
            transaction.data.decode()
            == "stake@02@d3e0427c22ff9cc80ef4156f976644cfa25c54e5a69ed199132053f8cbbfddd4eb15a2f732a3c9b392169c8b1d060e0b5ab0d88b4dd7b4010fa051a17ef81bdbace5e68025965b00bf48e14a9ec8d8e2a8bcc9e62f97ddac3268f6b805f7b80e@900befe131dfdb8b40bfbf048ebb7f12b57d2d45bedd141bca848f343c7ac8c431af9faacbaaac1cf5eca9827aef9d06@b0b6349b3f693e08c433970d10efb2fe943eac4057a945146bee5fd163687f4e1800d541aa0f11bf9e4cb6552f512e126068e68eb471d18fcc477ddfe0b9b3334f34e30d8b7b2c08f914f4ae54454f75fb28922ba9fd28785bcadc627031fa8a@f1fdb60bab285322ffaff8ee27b2b90f03a71d1f172e077941f2212e7a27588ed873faf3bd7f37a8205fda788e1f3d88@b05fe535c27f46911f74f8b7f2051c54f792fca08c7ab23c53e77ececd2cd928"
        )

    def test_create_transaction_for_staking_using_validators_file(self):
        validators_file = ValidatorsSigners.new_from_pem(self.validators_file)

        transaction = self.controller.create_transaction_for_staking(
            sender=self.alice,
            nonce=self.alice.nonce,
            validators_file=validators_file,
            amount=2500000000000000000000,
            rewards_address=self.reward_address,
        )

        assert transaction.sender.to_bech32() == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
        assert transaction.value == 2500000000000000000000
        assert transaction.nonce == 0
        assert transaction.gas_limit == 11029500
        assert transaction.chain_id == "localnet"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.guardian is None
        assert transaction.relayer is None
        assert (
            transaction.signature.hex()
            == "b4b6ee45f8a1d882ebef9cb2044f2833280f96bea4dec6632db69020e4927764d49ecdb47fc3abc9e9d96f3f61490d5dcdde4ea768d0475f52fac2b8eb02d705"
        )
        assert (
            transaction.data.decode()
            == "stake@02@d3e0427c22ff9cc80ef4156f976644cfa25c54e5a69ed199132053f8cbbfddd4eb15a2f732a3c9b392169c8b1d060e0b5ab0d88b4dd7b4010fa051a17ef81bdbace5e68025965b00bf48e14a9ec8d8e2a8bcc9e62f97ddac3268f6b805f7b80e@900befe131dfdb8b40bfbf048ebb7f12b57d2d45bedd141bca848f343c7ac8c431af9faacbaaac1cf5eca9827aef9d06@b0b6349b3f693e08c433970d10efb2fe943eac4057a945146bee5fd163687f4e1800d541aa0f11bf9e4cb6552f512e126068e68eb471d18fcc477ddfe0b9b3334f34e30d8b7b2c08f914f4ae54454f75fb28922ba9fd28785bcadc627031fa8a@f1fdb60bab285322ffaff8ee27b2b90f03a71d1f172e077941f2212e7a27588ed873faf3bd7f37a8205fda788e1f3d88@b05fe535c27f46911f74f8b7f2051c54f792fca08c7ab23c53e77ececd2cd928"
        )

    def test_create_transaction_for_staking_with_relayer_and_guardian(self):
        validators_file = ValidatorsSigners.new_from_pem(self.validators_file)

        transaction = self.controller.create_transaction_for_staking(
            sender=self.alice,
            nonce=self.alice.nonce,
            validators_file=validators_file,
            amount=2500000000000000000000,
            rewards_address=self.reward_address,
            guardian=Address.new_from_bech32("drt1cqqxak4wun7508e0yj9ng843r6hv4mzd0hhpjpsejkpn9wa9yq8s0ztfl2"),
            relayer=Address.new_from_bech32("drt1ssmsc9022udc8pdw7wk3hxw74jr900xg28vwpz3z60gep66fasaszky4ct"),
        )

        assert transaction.sender.to_bech32() == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
        assert transaction.value == 2500000000000000000000
        assert transaction.nonce == 0
        assert transaction.gas_limit == 11129500
        assert transaction.chain_id == "localnet"
        assert transaction.version == 2
        assert transaction.options == 2
        assert transaction.guardian == Address.new_from_bech32(
            "drt1cqqxak4wun7508e0yj9ng843r6hv4mzd0hhpjpsejkpn9wa9yq8s0ztfl2"
        )
        assert transaction.relayer == Address.new_from_bech32(
            "drt1ssmsc9022udc8pdw7wk3hxw74jr900xg28vwpz3z60gep66fasaszky4ct"
        )
        assert (
            transaction.signature.hex()
            == "bf11fbba0b1d835a42358b4585ab58ed363ea8e1b7e641519ef18ca65c76ab510388df8404ba8d262c250900aea189e78770f27bd0f37fc7a3c981e1c378eb0d"
        )
        assert (
            transaction.data.decode()
            == "stake@02@d3e0427c22ff9cc80ef4156f976644cfa25c54e5a69ed199132053f8cbbfddd4eb15a2f732a3c9b392169c8b1d060e0b5ab0d88b4dd7b4010fa051a17ef81bdbace5e68025965b00bf48e14a9ec8d8e2a8bcc9e62f97ddac3268f6b805f7b80e@900befe131dfdb8b40bfbf048ebb7f12b57d2d45bedd141bca848f343c7ac8c431af9faacbaaac1cf5eca9827aef9d06@b0b6349b3f693e08c433970d10efb2fe943eac4057a945146bee5fd163687f4e1800d541aa0f11bf9e4cb6552f512e126068e68eb471d18fcc477ddfe0b9b3334f34e30d8b7b2c08f914f4ae54454f75fb28922ba9fd28785bcadc627031fa8a@f1fdb60bab285322ffaff8ee27b2b90f03a71d1f172e077941f2212e7a27588ed873faf3bd7f37a8205fda788e1f3d88@b05fe535c27f46911f74f8b7f2051c54f792fca08c7ab23c53e77ececd2cd928"
        )

    def test_create_transaction_for_topping_up(self):
        transaction = self.controller.create_transaction_for_topping_up(
            sender=self.alice,
            nonce=self.alice.nonce,
            amount=2500000000000000000000,
        )

        assert transaction.sender.to_bech32() == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
        assert transaction.value == 2500000000000000000000
        assert transaction.nonce == 0
        assert transaction.gas_limit == 5057500
        assert transaction.chain_id == "localnet"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.guardian is None
        assert transaction.relayer is None
        assert transaction.data.decode() == "stake"
        assert (
            transaction.signature.hex()
            == "889baf984fca3c5325c4fa3a6b7b0d550b49bb6ae34f4f81fea6ccf71373b51aeeb0c7449b89479ed2f69a50a859668017469944fbf19125ec24671bf7114800"
        )

    def test_create_transaction_for_unstaking(self):
        transaction = self.controller.create_transaction_for_unstaking(
            sender=self.alice,
            nonce=7,
            public_keys=[self.validator_pubkey],
        )

        assert transaction.sender.to_bech32() == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
        assert transaction.value == 0
        assert transaction.nonce == 7
        assert transaction.gas_limit == 5350000
        assert transaction.chain_id == "localnet"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.guardian is None
        assert transaction.relayer is None
        assert (
            transaction.signature.hex()
            == "9588ef705a8794edb40ced8a70098cbc6c95cc652d1a61acbdc45bb7f56c1650e686ba307dfdd65efa3bb2be413701abcc65343ba0e95be2a5f996945d7cfe07"
        )
        assert (
            transaction.data.decode()
            == "unStake@d3e0427c22ff9cc80ef4156f976644cfa25c54e5a69ed199132053f8cbbfddd4eb15a2f732a3c9b392169c8b1d060e0b5ab0d88b4dd7b4010fa051a17ef81bdbace5e68025965b00bf48e14a9ec8d8e2a8bcc9e62f97ddac3268f6b805f7b80e"
        )

    def test_create_transaction_for_unbonding(self):
        transaction = self.controller.create_transaction_for_unbonding(
            sender=self.alice,
            nonce=7,
            public_keys=[self.validator_pubkey],
        )

        assert transaction.sender.to_bech32() == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
        assert transaction.value == 0
        assert transaction.nonce == 7
        assert transaction.gas_limit == 5348500
        assert transaction.chain_id == "localnet"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.guardian is None
        assert transaction.relayer is None
        assert (
            transaction.signature.hex()
            == "3db8f4fe12e49376c2fd57df0460d92ee7cf97a375fba6b94093f3d8663a412e0131750b8fd4af10ae28806929f8f2fbf7210448fab7388e49a1cdf3a361660e"
        )
        assert (
            transaction.data.decode()
            == "unBond@d3e0427c22ff9cc80ef4156f976644cfa25c54e5a69ed199132053f8cbbfddd4eb15a2f732a3c9b392169c8b1d060e0b5ab0d88b4dd7b4010fa051a17ef81bdbace5e68025965b00bf48e14a9ec8d8e2a8bcc9e62f97ddac3268f6b805f7b80e"
        )

    def test_create_transaction_for_unjailing(self):
        transaction = self.controller.create_transaction_for_unjailing(
            sender=self.alice,
            nonce=7,
            public_keys=[self.validator_pubkey],
            amount=2500000000000000000000,
        )

        assert transaction.sender.to_bech32() == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
        assert transaction.value == 2500000000000000000000
        assert transaction.nonce == 7
        assert transaction.gas_limit == 5348500
        assert transaction.chain_id == "localnet"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.guardian is None
        assert transaction.relayer is None
        assert (
            transaction.signature.hex()
            == "d786e022eb8c219f3653898f6a397b84223a534b7128cc0b40b2ea89737ffec824f2a09e12e6ad6f229e721c3badd18247dea36800d8b209a1663a4629acae08"
        )
        assert (
            transaction.data.decode()
            == "unJail@d3e0427c22ff9cc80ef4156f976644cfa25c54e5a69ed199132053f8cbbfddd4eb15a2f732a3c9b392169c8b1d060e0b5ab0d88b4dd7b4010fa051a17ef81bdbace5e68025965b00bf48e14a9ec8d8e2a8bcc9e62f97ddac3268f6b805f7b80e"
        )

    def test_create_transaction_for_changing_rewards_address(self):
        transaction = self.controller.create_transaction_for_changing_rewards_address(
            sender=self.alice,
            nonce=7,
            rewards_address=self.reward_address,
        )

        assert transaction.sender.to_bech32() == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
        assert transaction.value == 0
        assert transaction.nonce == 7
        assert transaction.gas_limit == 5176000
        assert transaction.chain_id == "localnet"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.guardian is None
        assert transaction.relayer is None
        assert (
            transaction.signature.hex()
            == "8fc9186263dd411c6e2d7096dbef027cfd40246590bc1e78c8a12f896a32b28554857138cc67673ee8812f86b345bef270bb69605fb4470aeb3aa7d997561301"
        )
        assert (
            transaction.data.decode()
            == "changeRewardAddress@b05fe535c27f46911f74f8b7f2051c54f792fca08c7ab23c53e77ececd2cd928"
        )

    def test_create_transaction_for_claiming(self):
        transaction = self.controller.create_transaction_for_claiming(
            sender=self.alice,
            nonce=7,
        )

        assert transaction.sender.to_bech32() == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
        assert transaction.value == 0
        assert transaction.nonce == 7
        assert transaction.gas_limit == 5057500
        assert transaction.chain_id == "localnet"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.guardian is None
        assert transaction.relayer is None
        assert transaction.data.decode() == "claim"
        assert (
            transaction.signature.hex()
            == "c45746452968a46323753ae083a7f5d3bba40baeedfe3e765ea7976681dc87f0588fe382418f2d946dcbde9d09727e5f2fe6120dd07edfa9dd579eeba574760b"
        )

    def test_create_transaction_for_unstaking_nodes(self):
        transaction = self.controller.create_transaction_for_unstaking_nodes(
            sender=self.alice,
            nonce=7,
            public_keys=[self.validator_pubkey],
        )

        assert transaction.sender.to_bech32() == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
        assert transaction.value == 0
        assert transaction.nonce == 7
        assert transaction.gas_limit == 5357500
        assert transaction.chain_id == "localnet"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.guardian is None
        assert transaction.relayer is None
        assert (
            transaction.signature.hex()
            == "7d766ac56974eb46b1dc6b74acac90e14f728e4a200c6311a4d795c7386f58fc81f242ff4a2fe9f2d30cd6785f66166fea359fbb7f17e237f655f76471598c09"
        )
        assert (
            transaction.data.decode()
            == "unStakeNodes@d3e0427c22ff9cc80ef4156f976644cfa25c54e5a69ed199132053f8cbbfddd4eb15a2f732a3c9b392169c8b1d060e0b5ab0d88b4dd7b4010fa051a17ef81bdbace5e68025965b00bf48e14a9ec8d8e2a8bcc9e62f97ddac3268f6b805f7b80e"
        )

    def test_create_transaction_for_unstaking_tokens(self):
        transaction = self.controller.create_transaction_for_unstaking_tokens(
            sender=self.alice,
            nonce=7,
            amount=11000000000000000000,
        )

        assert transaction.sender.to_bech32() == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
        assert transaction.value == 0
        assert transaction.nonce == 7
        assert transaction.gas_limit == 5095000
        assert transaction.chain_id == "localnet"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.guardian is None
        assert transaction.relayer is None
        assert (
            transaction.signature.hex()
            == "319d4088e12f18b181374c32aa8a4dcd21d6d7e3ee74316943af252787fa9c25f29336a83093398dec2af040655e6deb2b87851ff1fede3cfe7b7ca5089a6707"
        )
        assert transaction.data.decode() == "unStakeTokens@98a7d9b8314c0000"

    def test_create_transaction_for_unbonding_nodes(self):
        transaction = self.controller.create_transaction_for_unbonding_nodes(
            sender=self.alice,
            nonce=7,
            public_keys=[self.validator_pubkey],
        )

        assert transaction.sender.to_bech32() == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
        assert transaction.value == 0
        assert transaction.nonce == 7
        assert transaction.gas_limit == 5356000
        assert transaction.chain_id == "localnet"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.guardian is None
        assert transaction.relayer is None
        assert (
            transaction.signature.hex()
            == "c8844152d1dc97799eca138fe00c41b2228dd6e6f3826b768843d2b3ba12e982c8311ccffc0860cd256efe7ce1f69b701fa1f744fb7f078fa1ff642014ea620a"
        )
        assert (
            transaction.data.decode()
            == "unBondNodes@d3e0427c22ff9cc80ef4156f976644cfa25c54e5a69ed199132053f8cbbfddd4eb15a2f732a3c9b392169c8b1d060e0b5ab0d88b4dd7b4010fa051a17ef81bdbace5e68025965b00bf48e14a9ec8d8e2a8bcc9e62f97ddac3268f6b805f7b80e"
        )

    def test_create_transaction_for_unbonding_tokens(self):
        transaction = self.controller.create_transaction_for_unbonding_tokens(
            sender=self.alice,
            nonce=7,
            amount=20000000000000000000,
        )

        assert transaction.sender.to_bech32() == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
        assert transaction.value == 0
        assert transaction.nonce == 7
        assert transaction.gas_limit == 5096500
        assert transaction.chain_id == "localnet"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.guardian is None
        assert transaction.relayer is None
        assert (
            transaction.signature.hex()
            == "801694418b144d99aad6e27bcb387ecbc5858d38a44807d3b26329c6341bfdb34f43edda47038e69f61f5a3a9a956cdf8aedd6c3e8424b552124215809d19403"
        )
        assert transaction.data.decode() == "unBondTokens@01158e460913d00000"

    def test_create_transaction_for_cleaning_registered_data(self):
        transaction = self.controller.create_transaction_for_cleaning_registered_data(
            sender=self.alice,
            nonce=7,
        )

        assert transaction.sender.to_bech32() == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
        assert transaction.value == 0
        assert transaction.nonce == 7
        assert transaction.gas_limit == 5078500
        assert transaction.chain_id == "localnet"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.guardian is None
        assert transaction.relayer is None
        assert (
            transaction.signature.hex()
            == "ceac96dad6b9cd2ebb873a092b896e1568943ea4e26a1d1efed9ce9909713ff291e9b041d7e9a3274cf1c22a8dae85e2010d9a3b62de003995e982587ad68d0e"
        )
        assert transaction.data.decode() == "cleanRegisteredData"

    def test_create_transaction_for_restaking_unstaked_nodes(self):
        transaction = self.controller.create_transaction_for_restaking_unstaked_nodes(
            sender=self.alice,
            nonce=7,
            public_keys=[self.validator_pubkey],
        )

        assert transaction.sender.to_bech32() == "drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
        assert transaction.value == 0
        assert transaction.nonce == 7
        assert transaction.gas_limit == 5369500
        assert transaction.chain_id == "localnet"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.guardian is None
        assert transaction.relayer is None
        assert (
            transaction.signature.hex()
            == "749b567ee93fabbfc667c057152df18e4157fd9bd2baac861d0da0032ce77dee55b9c14cfd144596542dec5ce5343aeede2c3ee51d8ff933001646bcbcb3390b"
        )
        assert (
            transaction.data.decode()
            == "reStakeUnStakedNodes@d3e0427c22ff9cc80ef4156f976644cfa25c54e5a69ed199132053f8cbbfddd4eb15a2f732a3c9b392169c8b1d060e0b5ab0d88b4dd7b4010fa051a17ef81bdbace5e68025965b00bf48e14a9ec8d8e2a8bcc9e62f97ddac3268f6b805f7b80e"
        )
