"""UI tests for source/Meddiff.py using streamlit's AppTest.

These are integration style tests that simulate user interaction with the
Streamlit app. External dependencies (JSONBin API, login flow, secrets)
are mocked so tests run offline and don't touch real services.
"""

import sys
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

# Add source/ to Python's import path so AppTest can find utils/
SOURCE_DIR = Path(__file__).parent.parent / "source"
sys.path.insert(0, str(SOURCE_DIR))

# Absolute path to the app file we're testing
APP_FILE = str(SOURCE_DIR / "Meddiff.py")


@pytest.fixture
def app_test(mocker):
    """
    Build a ready-to-run AppTest with all external dependencies mocked.

    Mocks:
    - st.secrets — provides fake JSONBin credentials
    - login() — short-circuits the auth flow
    - JSONBin save_key / load_data — no real HTTP calls
    - st.session_state["username"] — fake user
    """
    # Fake secrets so st.secrets["jsonbin"]["api_key"] doesn't crash
    fake_secrets = {"jsonbin": {"api_key": "fake-key", "bin_id": "fake-bin"}}
    mocker.patch("streamlit.secrets", fake_secrets)

    # Skip login — pretend the user is already logged in
    mocker.patch("utils.authentication.login", return_value=None)

    # Mock JSONBin calls so no real HTTP happens
    mocker.patch("utils.jsonbin_client.load_data", return_value={})
    mocker.patch("utils.jsonbin_client.save_key", return_value={})

    # Build the AppTest instance
    at = AppTest.from_file(APP_FILE)

    # Pre-set session state so login-related state isn't missing
    at.session_state["username"] = "test_user"

    return at


# ---------- Tests ----------

def test_app_loads_without_crashing(app_test):
    """The main app should load and run without raising an exception."""
    at = app_test.run(timeout=10)
    assert not at.exception, f"App crashed during load: {at.exception}"


def test_app_displays_main_title(app_test):
    """The main page should display the expected title."""
    at = app_test.run(timeout=10)
    titles = [t.value for t in at.title]
    assert any("Differenzierung" in title for title in titles), (
        f"Expected title containing 'Differenzierung', got: {titles}"
    )


def test_app_renders_three_tabs(app_test):
    """The app should render three tabs: Tastatur, Beurteilung, Resultat."""
    at = app_test.run(timeout=10)
    # Tabs in Streamlit's AppTest are exposed as a flat list
    # We check that there's at least one set of tabs with 3 entries
    assert len(at.tabs) >= 1, "Expected at least one tab group"
    tab_labels = [tab.label for tab in at.tabs]
    assert "Tastatur" in tab_labels
    assert "Beurteilung" in tab_labels
    assert "Resultat" in tab_labels


def test_clicking_finish_count_with_zero_cells_shows_error(app_test):
    """Clicking 'Zählung beenden' when no cells counted should show an error."""
    at = app_test.run(timeout=10)

    # Find the "Zählung beenden" button and click it
    finish_buttons = [b for b in at.button if b.label == "Zählung beenden"]
    assert len(finish_buttons) > 0, "Could not find 'Zählung beenden' button"

    finish_buttons[0].click().run(timeout=10)

    # An error message should now be visible
    error_messages = [e.value for e in at.error]
    assert any("100 Zellen" in msg for msg in error_messages), (
        f"Expected error about counting 100 cells, got: {error_messages}"
    )