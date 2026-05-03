"""test to verify pytest is working correctly."""


def test_math():
    """If 1 + 1 stops being 2, we have problems."""
    assert 1 + 1 == 2


def test_string_operations():
    """Verify Python strings behave normally."""
    assert "Meddiff".lower() == "meddiff"
    assert len("hello") == 5