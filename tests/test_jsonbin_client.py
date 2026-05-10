"""Tests for source/utils/jsonbin_client.py — JSONBin API helpers."""

import sys
from pathlib import Path
from unittest.mock import MagicMock

# Add source/utils/ to Python's import path
UTILS_DIR = Path(__file__).parent.parent / "source" / "utils"
sys.path.insert(0, str(UTILS_DIR))

import jsonbin_client


# ---------- Tests for load_key ----------

def test_load_key_returns_existing_value(mocker):
    """load_key should return the value when the key exists in the bin."""
    fake_response = MagicMock()
    fake_response.json.return_value = {
        "record": {"alice": [1, 2, 3], "bob": [4, 5, 6]}
    }
    mocker.patch("jsonbin_client.requests.get", return_value=fake_response)

    result = jsonbin_client.load_key("key", "bin", "alice")

    assert result == [1, 2, 3]


def test_load_key_returns_default_when_missing(mocker):
    """load_key should return the empty_value when the key is not in the bin."""
    fake_response = MagicMock()
    fake_response.json.return_value = {"record": {"alice": [1, 2, 3]}}
    mocker.patch("jsonbin_client.requests.get", return_value=fake_response)

    result = jsonbin_client.load_key("key", "bin", "charlie", empty_value=[])

    assert result == []


def test_load_key_custom_empty_value(mocker):
    """load_key should respect a custom empty_value when key is missing."""
    fake_response = MagicMock()
    fake_response.json.return_value = {"record": {}}
    mocker.patch("jsonbin_client.requests.get", return_value=fake_response)

    result = jsonbin_client.load_key("key", "bin", "missing", empty_value="not found")

    assert result == "not found"


def test_load_key_uses_correct_url_and_headers(mocker):
    """load_key should hit the /latest endpoint with the master key in headers."""
    fake_response = MagicMock()
    fake_response.json.return_value = {"record": {"alice": [1]}}
    mock_get = mocker.patch("jsonbin_client.requests.get", return_value=fake_response)

    jsonbin_client.load_key("my-key", "my-bin", "alice")

    mock_get.assert_called_once_with(
        "https://api.jsonbin.io/v3/b/my-bin/latest",
        headers={"X-Master-Key": "my-key"},
    )


# ---------- Tests for save_key ----------

def test_save_key_adds_new_key_to_existing_dict(mocker):
    """save_key should add a new key to the existing record dict."""
    fake_get_response = MagicMock()
    fake_get_response.json.return_value = {"record": {"alice": [1]}}
    fake_put_response = MagicMock()
    fake_put_response.json.return_value = {"record": {"alice": [1], "bob": [2]}}

    mocker.patch("jsonbin_client.requests.get", return_value=fake_get_response)
    mock_put = mocker.patch("jsonbin_client.requests.put", return_value=fake_put_response)

    jsonbin_client.save_key("key", "bin", "bob", [2])

    sent_data = mock_put.call_args.kwargs["json"]
    assert sent_data == {"alice": [1], "bob": [2]}


def test_save_key_updates_existing_key(mocker):
    """save_key should overwrite an existing key's value."""
    fake_get_response = MagicMock()
    fake_get_response.json.return_value = {"record": {"alice": [1, 2, 3]}}
    fake_put_response = MagicMock()
    fake_put_response.json.return_value = {"record": {"alice": [99]}}

    mocker.patch("jsonbin_client.requests.get", return_value=fake_get_response)
    mock_put = mocker.patch("jsonbin_client.requests.put", return_value=fake_put_response)

    jsonbin_client.save_key("key", "bin", "alice", [99])

    sent_data = mock_put.call_args.kwargs["json"]
    assert sent_data == {"alice": [99]}


# ---------- Tests for load_data ----------

def test_load_data_returns_user_data(mocker):
    """load_data should return the user's stored data."""
    fake_response = MagicMock()
    fake_response.json.return_value = {
        "record": {"alice": [{"cells": 5}, {"cells": 10}]}
    }
    mocker.patch("jsonbin_client.requests.get", return_value=fake_response)

    result = jsonbin_client.load_data("key", "bin", "alice")

    assert result == [{"cells": 5}, {"cells": 10}]


def test_load_data_returns_empty_list_for_missing_user(mocker):
    """load_data should return an empty list when the user has no data."""
    fake_response = MagicMock()
    fake_response.json.return_value = {"record": {"alice": [1, 2]}}
    mocker.patch("jsonbin_client.requests.get", return_value=fake_response)

    result = jsonbin_client.load_data("key", "bin", "newuser")

    assert result == []


def test_load_data_returns_empty_list_when_value_is_none(mocker):
    """load_data should convert None to an empty list."""
    fake_response = MagicMock()
    fake_response.json.return_value = {"record": {"alice": None}}
    mocker.patch("jsonbin_client.requests.get", return_value=fake_response)

    result = jsonbin_client.load_data("key", "bin", "alice")

    assert result == []