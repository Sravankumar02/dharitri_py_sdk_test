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
    reward_address = Address.new_from_bech32("drt1k2s324ww2g0yj38qn2ch2jwctdy8mnfxep94q9arncc6xecg3xaq889n6e")

    validator_pubkey = ValidatorPublicKey.from_string(
        "e7beaa95b3877f47348df4dd1cb578a4f7cabf7a20bfeefe5cdd263878ff132b765e04fef6f40c93512b666c47ed7719b8902f6c922c04247989b7137e837cc81a62e54712471c97a2ddab75aa9c2f58f813ed4c0fa722bde0ab718bff382208"
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

        assert transaction.sender.to_bech32() == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
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
            == "7629051f3e8ad2746eec1b4a95cc8ce5de69ee253125e209204b64e4cdb757e90e8034fc7fa3afd4b569c7f1f06db85076c9a63a8545e4d96d4e3c1aabd0df07"
        )
        assert (
            transaction.data.decode()
            == "stake@02@f8910e47cf9464777c912e6390758bb39715fffcb861b184017920e4a807b42553f2f21e7f3914b81bcf58b66a72ab16d97013ae1cff807cefc977ef8cbf116258534b9e46d19528042d16ef8374404a89b184e0a4ee18c77c49e454d04eae8d@1865870f7f69162a2dfefd33fe232a9ca984c6f22d1ee3f6a5b34a8eb8c9f7319001f29d5a2eed85c1500aca19fa4189@1b4e60e6d100cdf234d3427494dac55fbac49856cadc86bcb13a01b9bb05a0d9143e86c186c948e7ae9e52427c9523102efe9019a2a9c06db02993f2e3e6756576ae5a3ec7c235d548bc79de1a6990e1120ae435cb48f7fc436c9f9098b92a0d@12b309791213aac8ad9f34f0d912261e30f9ab060859e4d515e020a98b91d82a7cd334e4b504bb93d6b75347cccd6318@b2a11555ce521e4944e09ab17549d85b487dcd26c84b5017a39e31a3670889ba"
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

        assert transaction.sender.to_bech32() == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
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
            == "7629051f3e8ad2746eec1b4a95cc8ce5de69ee253125e209204b64e4cdb757e90e8034fc7fa3afd4b569c7f1f06db85076c9a63a8545e4d96d4e3c1aabd0df07"
        )
        assert (
            transaction.data.decode()
            == "stake@02@f8910e47cf9464777c912e6390758bb39715fffcb861b184017920e4a807b42553f2f21e7f3914b81bcf58b66a72ab16d97013ae1cff807cefc977ef8cbf116258534b9e46d19528042d16ef8374404a89b184e0a4ee18c77c49e454d04eae8d@1865870f7f69162a2dfefd33fe232a9ca984c6f22d1ee3f6a5b34a8eb8c9f7319001f29d5a2eed85c1500aca19fa4189@1b4e60e6d100cdf234d3427494dac55fbac49856cadc86bcb13a01b9bb05a0d9143e86c186c948e7ae9e52427c9523102efe9019a2a9c06db02993f2e3e6756576ae5a3ec7c235d548bc79de1a6990e1120ae435cb48f7fc436c9f9098b92a0d@12b309791213aac8ad9f34f0d912261e30f9ab060859e4d515e020a98b91d82a7cd334e4b504bb93d6b75347cccd6318@b2a11555ce521e4944e09ab17549d85b487dcd26c84b5017a39e31a3670889ba"
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

        assert transaction.sender.to_bech32() == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
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
            == "61e7beb550cc20667fe8d21bafe987496bb7aae147f242cde47270892b53bd31f3d076cfff6fd520763bf211f19b15b9df0d505b3da9b159c29a89937cb92f0e"
        )
        assert (
            transaction.data.decode()
            == "stake@02@f8910e47cf9464777c912e6390758bb39715fffcb861b184017920e4a807b42553f2f21e7f3914b81bcf58b66a72ab16d97013ae1cff807cefc977ef8cbf116258534b9e46d19528042d16ef8374404a89b184e0a4ee18c77c49e454d04eae8d@1865870f7f69162a2dfefd33fe232a9ca984c6f22d1ee3f6a5b34a8eb8c9f7319001f29d5a2eed85c1500aca19fa4189@1b4e60e6d100cdf234d3427494dac55fbac49856cadc86bcb13a01b9bb05a0d9143e86c186c948e7ae9e52427c9523102efe9019a2a9c06db02993f2e3e6756576ae5a3ec7c235d548bc79de1a6990e1120ae435cb48f7fc436c9f9098b92a0d@12b309791213aac8ad9f34f0d912261e30f9ab060859e4d515e020a98b91d82a7cd334e4b504bb93d6b75347cccd6318@b2a11555ce521e4944e09ab17549d85b487dcd26c84b5017a39e31a3670889ba"
        )

    def test_create_transaction_for_topping_up(self):
        transaction = self.controller.create_transaction_for_topping_up(
            sender=self.alice,
            nonce=self.alice.nonce,
            amount=2500000000000000000000,
        )

        assert transaction.sender.to_bech32() == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
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
            == "39064a3e23fbee980202024c98dfdaba272693cc1030f6cb3568c8ebe7a526d857b4099cf7784324b51c4ad8f0b92621cdb2c32e631040500e43a878bf989a0d"
        )

    def test_create_transaction_for_unstaking(self):
        transaction = self.controller.create_transaction_for_unstaking(
            sender=self.alice,
            nonce=7,
            public_keys=[self.validator_pubkey],
        )

        assert transaction.sender.to_bech32() == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
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
            == "38a6291f43d92554394ed926e7500524f7b2a29dede552dfd91b0ff0a3313168854e6aa0f7d767cb53c62c92f51f4f5ea727ceb308fd74340a900ea84f868d07"
        )
        assert (
            transaction.data.decode()
            == "unStake@e7beaa95b3877f47348df4dd1cb578a4f7cabf7a20bfeefe5cdd263878ff132b765e04fef6f40c93512b666c47ed7719b8902f6c922c04247989b7137e837cc81a62e54712471c97a2ddab75aa9c2f58f813ed4c0fa722bde0ab718bff382208"
        )

    def test_create_transaction_for_unbonding(self):
        transaction = self.controller.create_transaction_for_unbonding(
            sender=self.alice,
            nonce=7,
            public_keys=[self.validator_pubkey],
        )

        assert transaction.sender.to_bech32() == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
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
            == "431d6a532e5d2b2a91de662aad151db0f96fac5425a225f0393d3f409bd1e624ef5cf5e79fce844d9a93a3d836a66088a66d032e16380f18864b4fc19ef05503"
        )
        assert (
            transaction.data.decode()
            == "unBond@e7beaa95b3877f47348df4dd1cb578a4f7cabf7a20bfeefe5cdd263878ff132b765e04fef6f40c93512b666c47ed7719b8902f6c922c04247989b7137e837cc81a62e54712471c97a2ddab75aa9c2f58f813ed4c0fa722bde0ab718bff382208"
        )

    def test_create_transaction_for_unjailing(self):
        transaction = self.controller.create_transaction_for_unjailing(
            sender=self.alice,
            nonce=7,
            public_keys=[self.validator_pubkey],
            amount=2500000000000000000000,
        )

        assert transaction.sender.to_bech32() == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
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
            == "15458f5db3360251a966286fba7160ec17d88d7fc4f6fe0f9deda658e969f9ba49fef969526157e8750846aa2876b07d3b507ad6e9a0c9ab7655aa22fd413a0d"
        )
        assert (
            transaction.data.decode()
            == "unJail@e7beaa95b3877f47348df4dd1cb578a4f7cabf7a20bfeefe5cdd263878ff132b765e04fef6f40c93512b666c47ed7719b8902f6c922c04247989b7137e837cc81a62e54712471c97a2ddab75aa9c2f58f813ed4c0fa722bde0ab718bff382208"
        )

    def test_create_transaction_for_changing_rewards_address(self):
        transaction = self.controller.create_transaction_for_changing_rewards_address(
            sender=self.alice,
            nonce=7,
            rewards_address=self.reward_address,
        )

        assert transaction.sender.to_bech32() == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
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
            == "5d82d90873806855a965bd9b61e11854ef2e8323b17539f3f42a071a44ebdb7b2e34c57d261a02c9fa78feb5ba21bf90dd7bede91a72e0f7a7c8fd38e08f1603"
        )
        assert (
            transaction.data.decode()
            == "changeRewardAddress@b2a11555ce521e4944e09ab17549d85b487dcd26c84b5017a39e31a3670889ba"
        )

    def test_create_transaction_for_claiming(self):
        transaction = self.controller.create_transaction_for_claiming(
            sender=self.alice,
            nonce=7,
        )

        assert transaction.sender.to_bech32() == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
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
            == "7dbc547aab6fbdc4c0f7620c06cf44d2a00d6012e2a1db2e4edec1fa0f523679571d78eb957b4a9b68853af06c5121df26588a9046e11c00a846d0f1e93a2c07"
        )

    def test_create_transaction_for_unstaking_nodes(self):
        transaction = self.controller.create_transaction_for_unstaking_nodes(
            sender=self.alice,
            nonce=7,
            public_keys=[self.validator_pubkey],
        )

        assert transaction.sender.to_bech32() == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
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
            == "a27e60730ce7d1199fe7236a3db3c75d238f43d364ad4cd5de9fa1607004c7aa470637f85be1fd09bf43edd78d869ba4f2f121740509b8e93f329f7c0cb2cf07"
        )
        assert (
            transaction.data.decode()
            == "unStakeNodes@e7beaa95b3877f47348df4dd1cb578a4f7cabf7a20bfeefe5cdd263878ff132b765e04fef6f40c93512b666c47ed7719b8902f6c922c04247989b7137e837cc81a62e54712471c97a2ddab75aa9c2f58f813ed4c0fa722bde0ab718bff382208"
        )

    def test_create_transaction_for_unstaking_tokens(self):
        transaction = self.controller.create_transaction_for_unstaking_tokens(
            sender=self.alice,
            nonce=7,
            amount=11000000000000000000,
        )

        assert transaction.sender.to_bech32() == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
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
            == "d0aac76e130a235cfc78028c11ba81c71840d54028cdd6bfa44272e2bc3f8fe65e4404489a50cdf37bc4b04a150cc8586d096224a829ef15a97df04b67b33f09"
        )
        assert transaction.data.decode() == "unStakeTokens@98a7d9b8314c0000"

    def test_create_transaction_for_unbonding_nodes(self):
        transaction = self.controller.create_transaction_for_unbonding_nodes(
            sender=self.alice,
            nonce=7,
            public_keys=[self.validator_pubkey],
        )

        assert transaction.sender.to_bech32() == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
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
            == "d0bef0ca2e18ef2eb5333733be459f65c4b1726372c11f0ccfab18767d68fcf5af4a440d03641729c58ed4a69e17a8921ed38567fe81464f0c1f98f8587b1e00"
        )
        assert (
            transaction.data.decode()
            == "unBondNodes@e7beaa95b3877f47348df4dd1cb578a4f7cabf7a20bfeefe5cdd263878ff132b765e04fef6f40c93512b666c47ed7719b8902f6c922c04247989b7137e837cc81a62e54712471c97a2ddab75aa9c2f58f813ed4c0fa722bde0ab718bff382208"
        )

    def test_create_transaction_for_unbonding_tokens(self):
        transaction = self.controller.create_transaction_for_unbonding_tokens(
            sender=self.alice,
            nonce=7,
            amount=20000000000000000000,
        )

        assert transaction.sender.to_bech32() == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
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
            == "52b910c987349bda999573067563f43ac323de241e20a228a8dcc129d17f5604d87bbb30fb2ef4233dd64e2c54d76e22d1c209cad4af92e40b73c29d0b51f002"
        )
        assert transaction.data.decode() == "unBondTokens@01158e460913d00000"

    def test_create_transaction_for_cleaning_registered_data(self):
        transaction = self.controller.create_transaction_for_cleaning_registered_data(
            sender=self.alice,
            nonce=7,
        )

        assert transaction.sender.to_bech32() == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
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
            == "f2791ca4edb918807cacc08c05e7103fd936b2402b3d0c2cf7f219946b8067ebce5a685908a2cac466f1bccb73b4ec8470b421119826584d41684a4971b2eb01"
        )
        assert transaction.data.decode() == "cleanRegisteredData"

    def test_create_transaction_for_restaking_unstaked_nodes(self):
        transaction = self.controller.create_transaction_for_restaking_unstaked_nodes(
            sender=self.alice,
            nonce=7,
            public_keys=[self.validator_pubkey],
        )

        assert transaction.sender.to_bech32() == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
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
            == "e4420a51bf3ac6762943d15da9a6e14961d53ca96c61b1b1ab333d1298ea0f5eb0c7f50f832d3d34076f91030155d73f856bfd95c5ff3f35bd6962f31a4cc60b"
        )
        assert (
            transaction.data.decode()
            == "reStakeUnStakedNodes@e7beaa95b3877f47348df4dd1cb578a4f7cabf7a20bfeefe5cdd263878ff132b765e04fef6f40c93512b666c47ed7719b8902f6c922c04247989b7137e837cc81a62e54712471c97a2ddab75aa9c2f58f813ed4c0fa722bde0ab718bff382208"
        )

    def test_create_new_delegation_contract_from_validator(self):
        transaction = self.controller.create_transaction_for_new_delegation_contract_from_validator_data(
            sender=self.alice,
            nonce=7,
            max_cap=0,
            fee=3745,
        )

        assert transaction.sender.to_bech32() == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqylllsz8he8y"
        assert transaction.value == 0
        assert transaction.nonce == 7
        assert transaction.gas_limit == 51_107_000
        assert transaction.chain_id == "localnet"
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.data.decode() == "makeNewContractFromValidatorData@@0ea1"

    def test_create_transaction_for_merging_validator_to_delegation(self):
        delegation_contract = Address.new_from_bech32("drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx")

        transaction = self.controller.create_transaction_for_merging_validator_to_delegation_with_whitelist(
            sender=self.alice,
            nonce=7,
            delegation_contract=delegation_contract,
        )

        assert transaction.sender.to_bech32() == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqylllsz8he8y"
        assert transaction.value == 0
        assert transaction.nonce == 7
        assert transaction.gas_limit == 50_206_000
        assert transaction.chain_id == "localnet"
        assert transaction.version == 2
        assert transaction.options == 0
        assert (
            transaction.data.decode()
            == "mergeValidatorToDelegationWithWhitelist@000000000000000000010000000000000000000000000000000000002fffffff"
        )

    def test_create_transaction_for_merging_validator_to_delegation_same_owner(self):
        delegation_contract = Address.new_from_bech32("drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx")

        transaction = self.controller.create_transaction_for_merging_validator_to_delegation_same_owner(
            sender=self.alice,
            nonce=7,
            delegation_contract=delegation_contract,
        )

        assert transaction.sender.to_bech32() == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqylllsz8he8y"
        assert transaction.value == 0
        assert transaction.nonce == 7
        assert transaction.gas_limit == 50_200_000
        assert transaction.chain_id == "localnet"
        assert transaction.version == 2
        assert transaction.options == 0
        assert (
            transaction.data.decode()
            == "mergeValidatorToDelegationSameOwner@000000000000000000010000000000000000000000000000000000002fffffff"
        )
