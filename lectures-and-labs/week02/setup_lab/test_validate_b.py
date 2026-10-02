from validate_b import is_valid_email


def test_valid_email_returns_true_for_normal_address() -> None:
    assert is_valid_email("user@example.com") is True


def test_valid_email_returns_false_when_dot_is_missing() -> None:
    assert is_valid_email("user@example") is False


def test_valid_email_returns_false_when_at_sign_is_missing() -> None:
    assert is_valid_email("user.example.com") is False


def test_valid_email_returns_false_for_300_character_address() -> None:
    address = ("a" * 288) + "@example.com"
    assert len(address) == 300
    assert is_valid_email(address) is False
