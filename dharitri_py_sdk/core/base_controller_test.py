from pathlib import Path

from dharitri_py_sdk.accounts.account import Account
from dharitri_py_sdk.core.address import Address
from dharitri_py_sdk.core.base_controller import BaseController
from dharitri_py_sdk.core.transaction import Transaction


class TestBaseController:
    controller = BaseController()

    def test_version_and_options_for_hash_signing(self):
        testwallets = Path(__file__).parent.parent / "testutils" / "testwallets"
        alice = Account.new_from_pem(testwallets / "alice.pem")
        alice.use_hash_signing = True

        transaction = Transaction(
            sender=alice.address,
            receiver=Address.new_from_bech32("drt18h03w0y7qtqwtra3u4f0gu7e3kn2fslj83lqxny39m5c4rwaectswerhd2"),
            gas_limit=50_000,
            chain_id="D",
            version=1,
            options=0,
        )

        self.controller._set_version_and_options_for_hash_signing(sender=alice, transaction=transaction)  # type: ignore
        assert transaction.version == 2
        assert transaction.options == 1

    def test_add_extra_gas_limit(self):
        transaction = Transaction(
            sender=Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"),
            receiver=Address.new_from_bech32("drt18h03w0y7qtqwtra3u4f0gu7e3kn2fslj83lqxny39m5c4rwaectswerhd2"),
            gas_limit=50_000,
            chain_id="D",
            guardian=Address.new_from_bech32("drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q"),
            relayer=Address.new_from_bech32("drt10xpcr2cqud9vm6q4axfv64ek63k7xywfcy8zyjp7pvx3kr4cnqlqv3scy7"),
        )

        self.controller._add_extra_gas_limit_if_required(transaction=transaction)  # type: ignore
        assert transaction.gas_limit == 150_000

    def test_set_version_and_options_for_guardian(self):
        transaction = Transaction(
            sender=Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh"),
            receiver=Address.new_from_bech32("drt18h03w0y7qtqwtra3u4f0gu7e3kn2fslj83lqxny39m5c4rwaectswerhd2"),
            gas_limit=50_000,
            chain_id="D",
            guardian=Address.new_from_bech32("drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q"),
            version=1,
            options=0,
        )

        self.controller._set_version_and_options_for_guardian(transaction=transaction)  # type: ignore
        assert transaction.version == 2
        assert transaction.options == 2
