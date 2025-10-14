import os
from pathlib import Path

from dharitri_py_sdk.wallet.validator_keys import ValidatorSecretKey
from dharitri_py_sdk.wallet.validator_pem import ValidatorPEM
from dharitri_py_sdk.wallet.validator_signer import ValidatorSigner
from dharitri_py_sdk.wallet.validator_verifier import ValidatorVerifier

testwallets = Path(__file__).parent.parent / "testutils" / "testwallets"


def test_validator_secret_key_generate_public_key():
    assert (
        ValidatorSecretKey.from_string("132e9b47291fcc62c64b334fd434ab2db74bf64b42d4cc1b4cedd10df77c1936")
        .generate_public_key()
        .hex()
        == "d3e0427c22ff9cc80ef4156f976644cfa25c54e5a69ed199132053f8cbbfddd4eb15a2f732a3c9b392169c8b1d060e0b5ab0d88b4dd7b4010fa051a17ef81bdbace5e68025965b00bf48e14a9ec8d8e2a8bcc9e62f97ddac3268f6b805f7b80e"
    )


def test_sign_message():
    signer = ValidatorSigner.from_pem_file(testwallets / "validatorKey00.pem")
    message = b"hello"
    signature = signer.sign(message)
    assert (
        signature.hex()
        == "d2f4300352053141dd7128d58af93a2bbe73c3ddf24e685ddcd5b2b03d2d5dcf52b4ed491f1ad4f1a5e7eed458789414"
    )


def test_verify_message():
    verifier = ValidatorVerifier.from_string(
        "d3e0427c22ff9cc80ef4156f976644cfa25c54e5a69ed199132053f8cbbfddd4eb15a2f732a3c9b392169c8b1d060e0b5ab0d88b4dd7b4010fa051a17ef81bdbace5e68025965b00bf48e14a9ec8d8e2a8bcc9e62f97ddac3268f6b805f7b80e"
    )

    message = b"hello"
    signature = bytes.fromhex(
        "d2f4300352053141dd7128d58af93a2bbe73c3ddf24e685ddcd5b2b03d2d5dcf52b4ed491f1ad4f1a5e7eed458789414"
    )

    assert verifier.verify(message, signature)

    invalid_signature = bytes.fromhex(
        "94fd0a3a9d4f1ea2d4b40c6da67f9b786284a1c3895b7253fec7311597cda3f757862bb0690a92a13ce612c33889fd86"
    )
    assert verifier.verify(message, invalid_signature) is False


def test_pem_save():
    path = testwallets / "validatorKey00.pem"
    path_saved = path.with_suffix(".saved")

    with open(path) as f:
        content_expected = f.read().strip()

    pem = ValidatorPEM.from_file(path)
    pem.save(path_saved)

    with open(path_saved) as f:
        content_actual = f.read().strip()

    assert content_actual == content_expected
    os.remove(path_saved)
