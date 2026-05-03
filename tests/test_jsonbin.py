"""Tests for source/jsonbin.py"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

# Tell Python where to find source/ so we can import jsonbin.py
sys.path.insert(0, str(Path(__file__).parent.parent / "source"))

import jsonbin

# ---------- Tests for load_data_ ----------

def test_load_data_returns_record(mocker):
    """load_data_ should return the 'record' field from the JSON response."""
    fake_response = MagicMock()
    fake_response.json.return_value = {"record": {"users": ["alice", "bob"]}}
    mocker.patch("jsonbin.requests.get", return_value=fake_response)

    result = jsonbin.load_data_("fake-key", "fake-bin-id")

    assert result == {"users": ["alice", "bob"]}


def test_load_data_uses_correct_url_and_headers(mocker):
    """load_data_ should hit the /latest endpoint with the master key in headers."""
    fake_response = MagicMock()
    fake_response.json.return_value = {"record": {}}
    mock_get = mocker.patch("jsonbin.requests.get", return_value=fake_response)

    jsonbin.load_data_("my-key", "my-bin")

    mock_get.assert_called_once_with(
        "https://api.jsonbin.io/v3/b/my-bin/latest",
        headers={"X-Master-Key": "my-key"},
    )


# ---------- Tests for save_data_ ----------

def test_save_data_sends_put_with_data(mocker):
    """save_data_ should send a PUT request with the data as JSON body."""
    fake_response = MagicMock()
    fake_response.json.return_value = {"record": {"saved": True}}
    mock_put = mocker.patch("jsonbin.requests.put", return_value=fake_response)

    payload = {"hello": "world"}
    result = jsonbin.save_data_("my-key", "my-bin", payload)

    mock_put.assert_called_once_with(
        "https://api.jsonbin.io/v3/b/my-bin",
        headers={"X-Master-Key": "my-key", "Content-Type": "application/json"},
        json=payload,
    )
    assert result == {"record": {"saved": True}}


# ---------- Tests for load_key ----------

def test_load_key_returns_existing_value(mocker):
    """load_key should return the value when the key exists in the bin."""
    fake_response = MagicMock()
    fake_response.json.return_value = {
        "record": {"alice": [1, 2, 3], "bob": [4, 5, 6]}
    }
    mocker.patch("jsonbin.requests.get", return_value=fake_response)

    result = jsonbin.load_key("key", "bin", "alice")

    assert result == [1, 2, 3]


def test_load_key_returns_default_when_missing(mocker):
    """load_key should return the empty_value when the key is not in the bin."""
    fake_response = MagicMock()
    fake_response.json.return_value = {"record": {"alice": [1, 2, 3]}}
    mocker.patch("jsonbin.requests.get", return_value=fake_response)

    result = jsonbin.load_key("key", "bin", "charlie", empty_value=[])

    assert result == []


def test_load_key_custom_empty_value(mocker):
    """load_key should respect a custom empty_value when key is missing."""
    fake_response = MagicMock()
    fake_response.json.return_value = {"record": {}}
    mocker.patch("jsonbin.requests.get", return_value=fake_response)

    result = jsonbin.load_key("key", "bin", "missing", empty_value="not found")

    assert result == "not found"


# ---------- Tests for save_key ----------

def test_save_key_adds_new_key_to_existing_dict(mocker):
    """save_key should add a new key to the existing record dict."""
    fake_get_response = MagicMock()
    fake_get_response.json.return_value = {"record": {"alice": [1]}}
    fake_put_response = MagicMock()
    fake_put_response.json.return_value = {"record": {"alice": [1], "bob": [2]}}

    mocker.patch("jsonbin.requests.get", return_value=fake_get_response)
    mock_put = mocker.patch("jsonbin.requests.put", return_value=fake_put_response)

    jsonbin.save_key("key", "bin", "bob", [2])

    # The PUT call should include both alice (existing) and bob (new)
    sent_data = mock_put.call_args.kwargs["json"]
    assert sent_data == {"alice": [1], "bob": [2]}


def test_save_key_updates_existing_key(mocker):
    """save_key should overwrite an existing key's value."""
    fake_get_response = MagicMock()
    fake_get_response.json.return_value = {"record": {"alice": [1, 2, 3]}}
    fake_put_response = MagicMock()
    fake_put_response.json.return_value = {"record": {"alice": [99]}}

    mocker.patch("jsonbin.requests.get", return_value=fake_get_response)
    mock_put = mocker.patch("jsonbin.requests.put", return_value=fake_put_response)

    jsonbin.save_key("key", "bin", "alice", [99])

    sent_data = mock_put.call_args.kwargs["json"]
    assert sent_data == {"alice": [99]}