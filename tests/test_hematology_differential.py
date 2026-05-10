"""Tests for source/utils/hematology_differential.py — counter logic."""

import sys
from pathlib import Path

import pytest

# Add source/utils/ to Python's import path
UTILS_DIR = Path(__file__).parent.parent / "source" / "utils"
sys.path.insert(0, str(UTILS_DIR))


# We need to mock streamlit BEFORE importing hematology_differential
# because the module does `import streamlit as st` at module level
@pytest.fixture(autouse=True)
def fake_session_state(mocker):
    """Replace st.session_state with a plain dict for every test."""
    fake_state = {}
    mocker.patch("streamlit.session_state", new=fake_state)
    return fake_state


from hematology_differential import HematologyDifferential


# ---------- Tests for get_increment_value (pure logic) ----------

def test_get_increment_value_returns_plus_one_for_addieren():
    """get_increment_value('addieren') should return +1."""
    counter = HematologyDifferential(count_times="run1")
    assert counter.get_increment_value("addieren") == 1


def test_get_increment_value_returns_minus_one_for_subtrahieren():
    """get_increment_value('subtrahieren') should return -1."""
    counter = HematologyDifferential(count_times="run1")
    assert counter.get_increment_value("subtrahieren") == -1


def test_get_increment_value_raises_on_invalid_input():
    """get_increment_value should raise ValueError for unknown actions."""
    counter = HematologyDifferential(count_times="run1")
    with pytest.raises(ValueError):
        counter.get_increment_value("invalid_action")


# ---------- Tests for initialize_session_state ----------

def test_initialize_session_state_creates_keys(fake_session_state):
    """initialize_session_state should populate session_state with default counts."""
    counter = HematologyDifferential(count_times="run1")
    counter.initialize_session_state()

    assert "run1" in fake_session_state
    assert "leukocyte_count" in fake_session_state["run1"]
    assert "diverse_count" in fake_session_state["run1"]


def test_initialize_session_state_does_not_overwrite_existing(fake_session_state):
    """Calling initialize_session_state twice should not reset existing data."""
    counter = HematologyDifferential(count_times="run1")
    counter.initialize_session_state()
    fake_session_state["run1"]["leukocyte_count"]["Basophil"] = 5

    counter.initialize_session_state()
    assert fake_session_state["run1"]["leukocyte_count"]["Basophil"] == 5


# ---------- Tests for get_total_leukocytes ----------

def test_get_total_leukocytes_sums_all_values(fake_session_state):
    """get_total_leukocytes should sum all leukocyte counts."""
    counter = HematologyDifferential(count_times="run1")
    counter.initialize_session_state()
    fake_session_state["run1"]["leukocyte_count"]["Basophil"] = 3
    fake_session_state["run1"]["leukocyte_count"]["Lymphozyt"] = 7

    assert counter.get_total_leukocytes() == 10


def test_get_total_leukocytes_zero_when_empty(fake_session_state):
    """get_total_leukocytes should return 0 if nothing has been counted."""
    counter = HematologyDifferential(count_times="run1")
    counter.initialize_session_state()
    assert counter.get_total_leukocytes() == 0


# ---------- Tests for get_combined_counts ----------

def test_get_combined_counts_merges_both_dicts(fake_session_state):
    """get_combined_counts should return a single dict with all cell types."""
    counter = HematologyDifferential(count_times="run1")
    counter.initialize_session_state()
    fake_session_state["run1"]["leukocyte_count"]["Basophil"] = 4
    fake_session_state["run1"]["diverse_count"]["Normoblast"] = 2

    combined = counter.get_combined_counts()
    assert combined["Basophil"] == 4
    assert combined["Normoblast"] == 2


# ---------- Tests for reset_category and reset_all_counts ----------

def test_reset_category_zeroes_one_category(fake_session_state):
    """reset_category should zero out only the specified category."""
    counter = HematologyDifferential(count_times="run1")
    counter.initialize_session_state()
    fake_session_state["run1"]["leukocyte_count"]["Basophil"] = 5
    fake_session_state["run1"]["diverse_count"]["Normoblast"] = 3

    counter.reset_category("leukocyte_count")
    assert fake_session_state["run1"]["leukocyte_count"]["Basophil"] == 0
    # diverse_count should NOT be reset
    assert fake_session_state["run1"]["diverse_count"]["Normoblast"] == 3


def test_reset_all_counts_zeroes_everything(fake_session_state):
    """reset_all_counts should zero out both categories."""
    counter = HematologyDifferential(count_times="run1")
    counter.initialize_session_state()
    fake_session_state["run1"]["leukocyte_count"]["Basophil"] = 5
    fake_session_state["run1"]["diverse_count"]["Normoblast"] = 3

    counter.reset_all_counts()
    assert fake_session_state["run1"]["leukocyte_count"]["Basophil"] == 0
    assert fake_session_state["run1"]["diverse_count"]["Normoblast"] == 0