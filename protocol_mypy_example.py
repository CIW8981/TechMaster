"""
Protocol + mypy — complete worked example (CORRECT version).

A NotificationService depends only on the Notifier Protocol (the abstraction),
never on a concrete class. Concrete notifiers match STRUCTURALLY — none of
them inherit from Notifier. mypy verifies the match at check-time.

Check types:  mypy protocol_mypy_example.py
Run program:  python protocol_mypy_example.py
"""

from typing import Protocol


# --- THE CONTRACT (pure interface: shape only, no inheritance needed) ---
class Notifier(Protocol):
    def send(self, recipient: str, message: str) -> bool: ...


# --- IMPLEMENTATIONS (note: NONE inherit from Notifier) ---
class EmailNotifier:
    def send(self, recipient: str, message: str) -> bool:
        print(f"[EMAIL] to {recipient}: {message}")
        return True


class SMSNotifier:
    def send(self, recipient: str, message: str) -> bool:
        print(f"[SMS] to {recipient}: {message}")
        return True


# --- HIGH-LEVEL CODE depends on the abstraction, not a concrete class ---
class NotificationService:
    def __init__(self, notifier: Notifier):
        self._notifier = notifier

    def alert(self, recipient: str, message: str) -> None:
        if self._notifier.send(recipient, message):
            print("  -> delivered")
        else:
            print("  -> FAILED")


def main() -> None:
    for notifier in (EmailNotifier(), SMSNotifier()):
        NotificationService(notifier).alert("alice@example.com", "Build passed")


if __name__ == "__main__":
    main()
