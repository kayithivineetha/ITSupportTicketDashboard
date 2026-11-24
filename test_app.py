from streamlit.testing.v1 import AppTest


def test_app_loads_without_errors():
    at = AppTest.from_file("app.py").run()
    assert not at.exception


def test_default_ticket_count():
    at = AppTest.from_file("app.py").run()
    assert at.metric[0].value == "6"
