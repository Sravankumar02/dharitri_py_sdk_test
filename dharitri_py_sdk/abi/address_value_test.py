import re
from types import SimpleNamespace

import pytest

from dharitri_py_sdk.abi.address_value import AddressValue
from dharitri_py_sdk.core.address import Address


def test_set_payload_and_get_payload():
    # Simple
    pubkey = bytes.fromhex("2e77c9b1ae7fdc0d9a13e53687b93d24f87e1adcfc3c6abc9314c1365a37b849")
    value = AddressValue()
    value.set_payload(pubkey)
    assert value.get_payload() == pubkey

    # Simple (from Address)
    address = Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh")
    value = AddressValue()
    value.set_payload(address)
    assert value.get_payload() == address.get_public_key()

    # Simple (from bech32)
    address = Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh")
    value = AddressValue()
    value.set_payload(address.to_bech32())
    assert value.get_payload() == address.get_public_key()

    # From dict using a bech32 address
    address = Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh")
    value = AddressValue()
    value.set_payload({"bech32": address.to_bech32()})
    assert value.get_payload() == address.get_public_key()

    # From dict using a hex address
    address = Address.new_from_bech32("drt18y0exfc84806smfmeweat5xvnuj66rngpljfnug8mpzt0eh2w82sc0eqzh")
    value = AddressValue()
    value.set_payload({"hex": address.to_hex()})
    assert value.get_payload() == address.get_public_key()

    value = AddressValue.new_from_address(address)
    assert value.get_payload() == address.get_public_key()

    # With errors
    with pytest.raises(ValueError, match=re.escape("public key (address) has invalid length: 3")):
        AddressValue().set_payload(bytes([1, 2, 3]))

    # With errors
    with pytest.raises(TypeError, match="cannot convert 'types.SimpleNamespace' object to bytes"):
        AddressValue().set_payload(SimpleNamespace(a=1, b=2, c=3))

    # With errors
    with pytest.raises(
        ValueError,
        match="cannot extract pubkey from dictionary: missing 'bech32' or 'hex' keys",
    ):
        AddressValue().set_payload({})
