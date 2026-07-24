"""Basic automated test for the Streamlit dashboard."""

from streamlit.testing.v1 import AppTest


def test_dashboard_loads() -> None:
    """Confirm the dashboard loads without an exception."""

    app = AppTest.from_file("dashboard.py")
    app.run(timeout=30)

    assert not app.exception
    assert app.title[0].value == "🛡️ AI SOC Analyst Assistant"
    assert len(app.text_area) == 1
    assert len(app.file_uploader) == 1
    assert len(app.button) >= 1