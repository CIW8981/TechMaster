"""
Protocol + mypy — BROKEN version to demonstrate mypy catching a violation.

BadNotifier does NOT satisfy the Notifier Protocol:
  - its method is named notify(), not send()
So passing it to NotificationService should be a type error that mypy detects
BEFORE the program runs.

Check types:  mypy protocol_mypy_broken.py
"""

from typing import Protocol


class Notifier(Protocol):
    def send(self, recipient: str, message: str) -> bool: ...


class BadNotifier:
    # Wrong method name — this does NOT match the Notifier shape.
    def notify(self, recipient: str, message: str) -> bool:
        print(f"notifying {recipient}: {message}")
        return True


class NotificationService:
    def __init__(self, notifier: Notifier):
        self._notifier = notifier

    def alert(self, recipient: str, message: str) -> None:
        self._notifier.send(recipient, message)


def main() -> None:
    # BadNotifier has no send() method, so it is NOT a valid Notifier.
    NotificationService(BadNotifier()).alert("bob@example.com", "hi")


if __name__ == "__main__":
    main()
