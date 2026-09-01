"""Sample application entry point."""

from domain import build_message


def run(name: str) -> str:
    """Build the user-visible greeting."""
    message = build_message(name)
    return message


if __name__ == "__main__":
    print(run("world"))
