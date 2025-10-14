from dharitri_py_sdk.wallet.libraries.bls_facade import BLSFacade


def test_generate_public_key():
    facade = BLSFacade()

    # With good input
    public_key = facade.generate_public_key(
        bytes.fromhex("132e9b47291fcc62c64b334fd434ab2db74bf64b42d4cc1b4cedd10df77c1936")
    )
    assert (
        public_key.hex()
        == "d3e0427c22ff9cc80ef4156f976644cfa25c54e5a69ed199132053f8cbbfddd4eb15a2f732a3c9b392169c8b1d060e0b5ab0d88b4dd7b4010fa051a17ef81bdbace5e68025965b00bf48e14a9ec8d8e2a8bcc9e62f97ddac3268f6b805f7b80e"
    )

    # With bad input
    public_key = facade.generate_public_key(
        bytes.fromhex("7cff99bd671502db7d15bc8abc0c9a804fb925406fbdd50f1e4c17a4cd7742")
    )
    assert public_key.hex() == ""


def test_compute_message_signature():
    facade = BLSFacade()

    # With good input
    signature = facade.compute_message_signature(
        message=b"hello",
        private_key=bytes.fromhex("132e9b47291fcc62c64b334fd434ab2db74bf64b42d4cc1b4cedd10df77c1936"),
    )

    assert (
        signature.hex()
        == "d2f4300352053141dd7128d58af93a2bbe73c3ddf24e685ddcd5b2b03d2d5dcf52b4ed491f1ad4f1a5e7eed458789414"
    )

    # With bad input (bad key)
    signature = facade.compute_message_signature(
        message=b"hello",
        private_key=bytes.fromhex("7cff99bd671502db7d15bc8abc0c9a804fb925406fbdd50f1e4c17a4cd7742"),
    )

    assert signature.hex() == ""


def test_verify_message_signature():
    facade = BLSFacade()

    # With good input
    ok = facade.verify_message_signature(
        public_key=bytes.fromhex(
            "d3e0427c22ff9cc80ef4156f976644cfa25c54e5a69ed199132053f8cbbfddd4eb15a2f732a3c9b392169c8b1d060e0b5ab0d88b4dd7b4010fa051a17ef81bdbace5e68025965b00bf48e14a9ec8d8e2a8bcc9e62f97ddac3268f6b805f7b80e"
        ),
        message=b"hello",
        signature=bytes.fromhex(
            "d2f4300352053141dd7128d58af93a2bbe73c3ddf24e685ddcd5b2b03d2d5dcf52b4ed491f1ad4f1a5e7eed458789414"
        ),
    )

    assert ok

    # With altered signature
    ok = facade.verify_message_signature(
        public_key=bytes.fromhex(
            "d3e0427c22ff9cc80ef4156f976644cfa25c54e5a69ed199132053f8cbbfddd4eb15a2f732a3c9b392169c8b1d060e0b5ab0d88b4dd7b4010fa051a17ef81bdbace5e68025965b00bf48e14a9ec8d8e2a8bcc9e62f97ddac3268f6b805f7b80e"
        ),
        message=b"hello",
        signature=bytes.fromhex(
            "94fd0a3a9d4f1ea2d4b40c6da67f9b786284a1c3895b7253fec7311597cda3f757862bb0690a92a13ce612c33889fd86"
        ),
    )

    # With altered message
    ok = facade.verify_message_signature(
        public_key=bytes.fromhex(
            "d3e0427c22ff9cc80ef4156f976644cfa25c54e5a69ed199132053f8cbbfddd4eb15a2f732a3c9b392169c8b1d060e0b5ab0d88b4dd7b4010fa051a17ef81bdbace5e68025965b00bf48e14a9ec8d8e2a8bcc9e62f97ddac3268f6b805f7b80e"
        ),
        message=b"helloWorld",
        signature=bytes.fromhex(
            "84fd0a3a9d4f1ea2d4b40c6da67f9b786284a1c3895b7253fec7311597cda3f757862bb0690a92a13ce612c33889fd86"
        ),
    )

    assert not ok

    # With bad public key
    ok = facade.verify_message_signature(
        public_key=bytes.fromhex(
            "badbad95b3877f47348df4dd1cb578a4f7cabf7a20bfeefe5cdd263878ff132b765e04fef6f40c93512b666c47ed7719b8902f6c922c04247989b7137e837cc81a62e54712471c97a2ddab75aa9c2f58f813ed4c0fa722bde0ab718bff382208"
        ),
        message=b"hello",
        signature=bytes.fromhex(
            "84fd0a3a9d4f1ea2d4b40c6da67f9b786284a1c3895b7253fec7311597cda3f757862bb0690a92a13ce612c33889fd86"
        ),
    )

    assert not ok


def test_generate_sign_and_verify():
    facade = BLSFacade()
    message = b"hello"

    private_key = facade.generate_private_key()
    public_key = facade.generate_public_key(private_key)
    signature = facade.compute_message_signature(message, private_key)
    ok = facade.verify_message_signature(public_key, message, signature)

    assert ok
