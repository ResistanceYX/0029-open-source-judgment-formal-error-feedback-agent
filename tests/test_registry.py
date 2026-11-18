from judgment_formal_lint.input_registry import register_input, sha256_text


def test_fingerprint_stable():
    a = sha256_text("hello")
    b = sha256_text("hello")
    assert a == b and len(a) == 64


def test_register_records_governance_fields():
    info = register_input("demo.txt", "some text")
    assert info["document_id"] == info["sha256"][:16]
    assert info["authorization"]
    assert info["allowed_use"]
    assert info["formal_text_verified"] is False
    assert info["source_type"] == "user_provided_file"
