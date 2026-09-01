"""Sample first-party domain logic."""

API_KEY = "fixture-secret-value"


def build_message(name: str) -> str:
    cleaned = name.strip() or "guest"
    return f"Hello, {cleaned}!"
