from dharitri_py_sdk.core import Address, TransactionsFactoryConfig
from dharitri_py_sdk.core.constants import DELEGATION_MANAGER_SC_ADDRESS_HEX
from dharitri_py_sdk.delegation import DelegationTransactionsFactory
from dharitri_py_sdk.wallet import ValidatorSecretKey, ValidatorSigner
from dharitri_py_sdk.wallet.validator_keys import ValidatorPublicKey


class TestDelegationTransactionsFactory:
    config = TransactionsFactoryConfig("D")
    factory = DelegationTransactionsFactory(config)

    def test_create_transaction_for_new_delegation_contract(self):
        transaction = self.factory.create_transaction_for_new_delegation_contract(
            sender=Address.new_from_bech32("drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5"),
            total_delegation_cap=5000000000000000000000,
            service_fee=10,
            amount=1250000000000000000000,
        )

        assert transaction.sender.to_bech32() == "drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5"
        assert transaction.receiver.to_bech32() == Address.new_from_hex(DELEGATION_MANAGER_SC_ADDRESS_HEX).to_bech32()
        assert transaction.data
        assert transaction.data.decode() == "createNewDelegationContract@010f0cf064dd59200000@0a"
        assert transaction.gas_limit == 60126500
        assert transaction.value == 1250000000000000000000

    def test_create_transaction_for_adding_nodes(self):
        sender = Address.new_from_bech32("drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5")
        delegation_contract = Address.new_from_bech32("drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx")

        validator_secret_key = ValidatorSecretKey.from_string(
            "132e9b47291fcc62c64b334fd434ab2db74bf64b42d4cc1b4cedd10df77c1936"
        )
        validator_signer = ValidatorSigner(validator_secret_key)

        signed_message = validator_signer.sign(bytes.fromhex(delegation_contract.to_hex()))
        public_key = validator_secret_key.generate_public_key()

        public_keys = [public_key]
        signed_messages = [signed_message]

        transaction = self.factory.create_transaction_for_adding_nodes(
            sender=sender,
            delegation_contract=delegation_contract,
            public_keys=public_keys,
            signed_messages=signed_messages,
        )

        assert transaction.sender.to_bech32() == "drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx"
        assert transaction.data
        assert (
            transaction.data.decode()
            == "addNodes@d3e0427c22ff9cc80ef4156f976644cfa25c54e5a69ed199132053f8cbbfddd4eb15a2f732a3c9b392169c8b1d060e0b5ab0d88b4dd7b4010fa051a17ef81bdbace5e68025965b00bf48e14a9ec8d8e2a8bcc9e62f97ddac3268f6b805f7b80e@b368bdf8d3afbce33cae45b31f70608e38699db578b6a9423c9bd094b5071468f85ea21241aa090065dd44c181d53a83"
        )
        assert transaction.value == 0

    def test_create_transaction_for_removing_nodes(self):
        sender = Address.new_from_bech32("drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5")
        delegation_contract = Address.new_from_bech32("drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx")

        public_keys = [ValidatorPublicKey(bytes([0] * 96))]

        transaction = self.factory.create_transaction_for_removing_nodes(
            sender=sender,
            delegation_contract=delegation_contract,
            public_keys=public_keys,
        )

        assert transaction.sender.to_bech32() == "drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx"
        assert transaction.data
        assert (
            transaction.data.decode()
            == "removeNodes@000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
        )
        assert transaction.value == 0

    def test_create_transaction_for_staking_nodes(self):
        sender = Address.new_from_bech32("drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5")
        delegation_contract = Address.new_from_bech32("drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx")

        public_keys = [ValidatorPublicKey(bytes([0] * 96))]

        transaction = self.factory.create_transaction_for_staking_nodes(
            sender=sender,
            delegation_contract=delegation_contract,
            public_keys=public_keys,
        )

        assert transaction.sender.to_bech32() == "drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx"
        assert transaction.data
        assert (
            transaction.data.decode()
            == "stakeNodes@000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
        )
        assert transaction.value == 0

    def test_create_transaction_for_unbonding_nodes(self):
        sender = Address.new_from_bech32("drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5")
        delegation_contract = Address.new_from_bech32("drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx")

        public_keys = [ValidatorPublicKey(bytes([0] * 96))]

        transaction = self.factory.create_transaction_for_unbonding_nodes(
            sender=sender,
            delegation_contract=delegation_contract,
            public_keys=public_keys,
        )

        assert transaction.sender.to_bech32() == "drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx"
        assert transaction.data
        assert (
            transaction.data.decode()
            == "unBondNodes@000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
        )
        assert transaction.value == 0

    def test_create_transaction_for_unstaking_nodes(self):
        sender = Address.new_from_bech32("drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5")
        delegation_contract = Address.new_from_bech32("drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx")

        public_keys = [ValidatorPublicKey(bytes([0] * 96))]

        transaction = self.factory.create_transaction_for_unstaking_nodes(
            sender=sender,
            delegation_contract=delegation_contract,
            public_keys=public_keys,
        )

        assert transaction.sender.to_bech32() == "drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx"
        assert transaction.data
        assert (
            transaction.data.decode()
            == "unStakeNodes@000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
        )
        assert transaction.value == 0

    def test_create_transaction_for_unjailing_nodes(self):
        sender = Address.new_from_bech32("drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5")
        delegation_contract = Address.new_from_bech32("drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx")

        public_keys = [ValidatorPublicKey(bytes([0] * 96))]

        transaction = self.factory.create_transaction_for_unjailing_nodes(
            sender=sender,
            delegation_contract=delegation_contract,
            public_keys=public_keys,
            amount=25000000000000000000,  # 2.5 rewa
        )

        assert transaction.sender.to_bech32() == "drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx"
        assert transaction.data
        assert (
            transaction.data.decode()
            == "unJailNodes@000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
        )
        assert transaction.value == 25000000000000000000

    def test_create_transaction_for_changing_service_fee(self):
        sender = Address.new_from_bech32("drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5")
        delegation_contract = Address.new_from_bech32("drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx")

        transaction = self.factory.create_transaction_for_changing_service_fee(
            sender=sender, delegation_contract=delegation_contract, service_fee=10
        )

        assert transaction.sender.to_bech32() == "drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx"
        assert transaction.data
        assert transaction.data.decode() == "changeServiceFee@0a"
        assert transaction.value == 0

    def test_create_transaction_for_modifying_delegation_cap(self):
        sender = Address.new_from_bech32("drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5")
        delegation_contract = Address.new_from_bech32("drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx")

        transaction = self.factory.create_transaction_for_modifying_delegation_cap(
            sender=sender,
            delegation_contract=delegation_contract,
            delegation_cap=5000000000000000000000,
        )

        assert transaction.sender.to_bech32() == "drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx"
        assert transaction.data
        assert transaction.data.decode() == "modifyTotalDelegationCap@010f0cf064dd59200000"
        assert transaction.value == 0

    def test_create_transaction_for_setting_automatic_activation(self):
        sender = Address.new_from_bech32("drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5")
        delegation_contract = Address.new_from_bech32("drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx")

        transaction = self.factory.create_transaction_for_setting_automatic_activation(
            sender=sender, delegation_contract=delegation_contract
        )

        assert transaction.sender.to_bech32() == "drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx"
        assert transaction.data
        assert transaction.data.decode() == "setAutomaticActivation@74727565"
        assert transaction.value == 0

    def test_create_transaction_for_unsetting_automatic_activation(self):
        sender = Address.new_from_bech32("drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5")
        delegation_contract = Address.new_from_bech32("drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx")

        transaction = self.factory.create_transaction_for_unsetting_automatic_activation(
            sender=sender, delegation_contract=delegation_contract
        )

        assert transaction.sender.to_bech32() == "drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx"
        assert transaction.data
        assert transaction.data.decode() == "setAutomaticActivation@66616c7365"
        assert transaction.value == 0

    def test_create_transaction_for_setting_cap_check_on_redelegate_rewards(self):
        sender = Address.new_from_bech32("drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5")
        delegation_contract = Address.new_from_bech32("drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx")

        transaction = self.factory.create_transaction_for_setting_cap_check_on_redelegate_rewards(
            sender=sender, delegation_contract=delegation_contract
        )

        assert transaction.sender.to_bech32() == "drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx"
        assert transaction.data
        assert transaction.data.decode() == "setCheckCapOnReDelegateRewards@74727565"
        assert transaction.value == 0

    def test_create_transaction_for_unsetting_cap_check_on_redelegate_rewards(self):
        sender = Address.new_from_bech32("drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5")
        delegation_contract = Address.new_from_bech32("drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx")

        transaction = self.factory.create_transaction_for_unsetting_cap_check_on_redelegate_rewards(
            sender=sender, delegation_contract=delegation_contract
        )

        assert transaction.sender.to_bech32() == "drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx"
        assert transaction.data
        assert transaction.data.decode() == "setCheckCapOnReDelegateRewards@66616c7365"
        assert transaction.value == 0

    def test_create_transaction_for_setting_metadata(self):
        sender = Address.new_from_bech32("drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5")
        delegation_contract = Address.new_from_bech32("drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx")

        transaction = self.factory.create_transaction_for_setting_metadata(
            sender=sender,
            delegation_contract=delegation_contract,
            name="name",
            website="website",
            identifier="identifier",
        )

        assert transaction.sender.to_bech32() == "drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx"
        assert transaction.data
        assert transaction.data.decode() == "setMetaData@6e616d65@77656273697465@6964656e746966696572"
        assert transaction.value == 0

    def test_create_transaction_for_delegating(self):
        sender = Address.new_from_bech32("drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5")
        delegation_contract = Address.new_from_bech32("drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx")

        transaction = self.factory.create_transaction_for_delegating(
            sender=sender,
            delegation_contract=delegation_contract,
            amount=1000000000000000000,
        )

        assert transaction.sender.to_bech32() == "drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx"
        assert transaction.data
        assert transaction.data.decode() == "delegate"
        assert transaction.value == 1000000000000000000
        assert transaction.gas_limit == 11062000

    def test_create_transaction_for_claiming_rewards(self):
        sender = Address.new_from_bech32("drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5")
        delegation_contract = Address.new_from_bech32("drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx")

        transaction = self.factory.create_transaction_for_claiming_rewards(
            sender=sender, delegation_contract=delegation_contract
        )

        assert transaction.sender.to_bech32() == "drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx"
        assert transaction.data
        assert transaction.data.decode() == "claimRewards"
        assert transaction.value == 0
        assert transaction.gas_limit == 11068000

    def test_create_transaction_for_redelegating_rewards(self):
        sender = Address.new_from_bech32("drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5")
        delegation_contract = Address.new_from_bech32("drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx")

        transaction = self.factory.create_transaction_for_redelegating_rewards(
            sender=sender, delegation_contract=delegation_contract
        )

        assert transaction.sender.to_bech32() == "drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx"
        assert transaction.data
        assert transaction.data.decode() == "reDelegateRewards"
        assert transaction.value == 0
        assert transaction.gas_limit == 11075500

    def test_create_transaction_for_undelegating(self):
        sender = Address.new_from_bech32("drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5")
        delegation_contract = Address.new_from_bech32("drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx")

        transaction = self.factory.create_transaction_for_undelegating(
            sender=sender,
            delegation_contract=delegation_contract,
            amount=1000000000000000000,
        )

        assert transaction.sender.to_bech32() == "drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx"
        assert transaction.data
        assert transaction.data.decode() == "unDelegate@0de0b6b3a7640000"
        assert transaction.value == 0
        assert transaction.gas_limit == 11090500

    def test_create_transaction_for_withdrawing(self):
        sender = Address.new_from_bech32("drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5")
        delegation_contract = Address.new_from_bech32("drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx")

        transaction = self.factory.create_transaction_for_withdrawing(
            sender=sender, delegation_contract=delegation_contract
        )

        assert transaction.sender.to_bech32() == "drt18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqfgxqg5"
        assert transaction.receiver.to_bech32() == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtlllllsjnaptx"
        assert transaction.data
        assert transaction.data.decode() == "withdraw"
        assert transaction.value == 0
        assert transaction.gas_limit == 11062000
