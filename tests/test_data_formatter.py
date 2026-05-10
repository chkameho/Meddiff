"""Tests for source/utils/data_formatter.py — storage and display formatters."""

import sys
from pathlib import Path

import pandas as pd

# Add source/utils/ to Python's import path
UTILS_DIR = Path(__file__).parent.parent / "source" / "utils"
sys.path.insert(0, str(UTILS_DIR))

from data_formatter import StorageFormatter, DisplayFormatter


# ---------- Tests for StorageFormatter ----------

def _make_sample_df():
    """Helper: create a simple DataFrame for testing."""
    return pd.DataFrame(
        {"Mittelwert": [50, 30, 20]},
        index=["Lymphozyt", "Segmentierte", "Monozyt"],
    )


def test_storage_formatter_to_dict_has_correct_top_level_id():
    """to_dict() should be keyed by the id passed to the constructor."""
    formatter = StorageFormatter(
        id=42, df_count=_make_sample_df(),
        ec_morph="normal", lc_morph="normal", tc_morph="normal",
        legend="test legend",
    )
    result = formatter.to_dict()
    assert 42 in result


def test_storage_formatter_to_dict_contains_raw_data_and_meta_info():
    """to_dict() should produce both raw_data and meta_info sections."""
    formatter = StorageFormatter(
        id=1, df_count=_make_sample_df(),
        ec_morph="x", lc_morph="y", tc_morph="z",
        legend="some legend",
    )
    result = formatter.to_dict()
    assert "raw_data" in result[1]
    assert "meta_info" in result[1]


def test_storage_formatter_meta_info_contains_legend():
    """The legend passed in should appear in meta_info."""
    formatter = StorageFormatter(
        id=1, df_count=_make_sample_df(),
        ec_morph="x", lc_morph="y", tc_morph="z",
        legend="my custom legend",
    )
    meta = formatter._build_meta_info()
    assert meta["legend"] == "my custom legend"


def test_storage_formatter_meta_info_has_save_time():
    """meta_info should include a save_time key with a non-empty value."""
    formatter = StorageFormatter(
        id=1, df_count=_make_sample_df(),
        ec_morph="x", lc_morph="y", tc_morph="z",
        legend="",
    )
    meta = formatter._build_meta_info()
    assert "save_time" in meta
    assert len(meta["save_time"]) > 0  # ISO format string


def test_storage_formatter_data_contains_morph_descriptions():
    """_build_data should include all three morphology descriptions."""
    formatter = StorageFormatter(
        id=1, df_count=_make_sample_df(),
        ec_morph="ec_value", lc_morph="lc_value", tc_morph="tc_value",
        legend="",
    )
    data = formatter._build_data()
    assert data["morph"]["Erythrozyten Beurteilung"] == "ec_value"
    assert data["morph"]["Leukozyten Beurteilung"] == "lc_value"
    assert data["morph"]["Thrombozyten Beurteilung"] == "tc_value"


# ---------- Tests for DisplayFormatter ----------

def _make_sample_user_data():
    """Helper: build a sample user_data dict that DisplayFormatter expects."""
    return {
        "raw_data": {
            "count": {
                "index": ["Lymphozyt", "Monozyt"],
                "columns": ["Mittelwert"],
                "data": [[50], [20]],
            },
            "morph": {
                "Erythrozyten Beurteilung": "normal EC",
                "Leukozyten Beurteilung": "normal LC",
                "Thrombozyten Beurteilung": "normal TC",
            },
        },
        "meta_info": {
            "legend": "test legend",
            "save_time": "2026-05-03T12:00:00+00:00",
        },
    }


def test_display_formatter_get_count_data():
    """get_count_data should return (index, columns, data) tuple."""
    formatter = DisplayFormatter(_make_sample_user_data())
    index, columns, data = formatter.get_count_data()
    assert index == ["Lymphozyt", "Monozyt"]
    assert columns == ["Mittelwert"]
    assert data == [[50], [20]]


def test_display_formatter_get_morph_data():
    """get_morph_data should return the three morphology descriptions."""
    formatter = DisplayFormatter(_make_sample_user_data())
    morph = formatter.get_morph_data()
    assert morph["Erythrozyten Beurteilung"] == "normal EC"


def test_display_formatter_get_meta_info_with_legend():
    """get_meta_info should return (legend, save_time) tuple when legend exists."""
    formatter = DisplayFormatter(_make_sample_user_data())
    legend, save_time = formatter.get_meta_info()
    assert legend == "test legend"
    assert save_time == "2026-05-03T12:00:00+00:00"


def test_display_formatter_get_meta_info_with_empty_legend():
    """If legend is empty, get_meta_info should return 'Keine Angaben'."""
    user_data = _make_sample_user_data()
    user_data["meta_info"]["legend"] = ""

    formatter = DisplayFormatter(user_data)
    legend, _ = formatter.get_meta_info()
    assert legend == "Keine Angaben"


def test_display_formatter_to_dataframe_returns_correct_shape():
    """to_dataframe should produce a DataFrame matching the stored data."""
    formatter = DisplayFormatter(_make_sample_user_data())
    df = formatter.to_dataframe()
    assert isinstance(df, pd.DataFrame)
    assert list(df.index) == ["Lymphozyt", "Monozyt"]
    assert list(df.columns) == ["Mittelwert"]
    assert df.loc["Lymphozyt", "Mittelwert"] == 50