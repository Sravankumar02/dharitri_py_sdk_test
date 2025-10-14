import pytest

from dharitri_py_sdk.wallet.errors import InvalidAddressIndexError, InvalidMnemonicError
from dharitri_py_sdk.wallet.mnemonic import Mnemonic


def test_assert_text_is_valid():
    with pytest.raises(InvalidMnemonicError):
        Mnemonic.assert_text_is_valid("bad mnemonic")
        Mnemonic.assert_text_is_valid("moral volcano peasant pass circle pen over picture")


def test_generate():
    mnemonic = Mnemonic.generate()
    words = mnemonic.get_words()
    assert len(words) == 24

    with pytest.raises(InvalidAddressIndexError):
        mnemonic.derive_key(-1)


def test_derive_keys():
    mnemonic = Mnemonic(
        "bread type ride autumn corn maid benefit pole that normal orchard confirm napkin degree arrow guitar offer you enjoy bronze more onion push decorate"
    )
    assert mnemonic.derive_key(0).hex() == "2bbcdae7e193924fa0d301e7a12c7defc92a93bc5e587cc968f04fcb86022e1c"
    assert mnemonic.derive_key(1).hex() == "1f4d9984ff57a9bcc7b8aea32069e41d36366e4dd9e08f55c6691168de06f2c3"
    assert mnemonic.derive_key(2).hex() == "6c030765ecd8dce0e8aa8e15ab10823d5ae5dc682d3cb6c260640f01def7a587"

    # change the text to an invalid mnemonic
    mnemonic.text = "this is an invalid mnemonic"
    with pytest.raises(InvalidMnemonicError):
        mnemonic.derive_key()


def test_convert_entropy_to_mnemonic_and_back():
    def test_conversion(text: str, entropy_hex: str) -> None:
        entropy_from_mnemonic = Mnemonic(text).get_entropy()
        mnemonic_from_entropy = Mnemonic.from_entropy(bytes.fromhex(entropy_hex))

        assert entropy_from_mnemonic.hex() == entropy_hex
        assert mnemonic_from_entropy.get_text() == text

    test_conversion(
        text="abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about",
        entropy_hex="00000000000000000000000000000000",
    )

    test_conversion(
        text="moral volcano peasant pass circle pen over picture flat shop clap goat never lyrics gather prepare woman film husband gravity behind test tiger improve",
        entropy_hex="8fbeb688d0529344e77d225898d4a73209510ad81d4ffceac9bfb30149bf387b",
    )

    with pytest.raises(ValueError):
        Mnemonic.from_entropy(bytes.fromhex("abba"))
