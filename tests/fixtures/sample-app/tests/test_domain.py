from src.domain import build_message


def test_message():
    assert build_message("Codex") == "Hello, Codex!"
