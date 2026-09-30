---
title: "Adapter Pattern (Python)"
description: "Learn the Adapter design pattern from first principles with Python examples: wrap an incompatible third-party interface so it fits the interface your code expects"
tags:
  - python
  - programming
  - design-patterns
  - adapter
  - clean-code
difficulty: intermediate
last_updated: "2026-09-18"
---

# Adapter Pattern

!!! info "The pattern"
    Wrap an object with an incompatible interface in a new class that exposes the
    interface *your* code expects, translating calls between the two — like a
    power-plug adapter that makes a US plug fit a European socket.

## Introduction

You often need to use a third-party or legacy class whose API **doesn't match**
your code's expectations — and you can't change either side. The Adapter is a small
translator that sits between them.

---

## The Problem

Your app expects one clean interface everywhere:

```python
from typing import Protocol

class Notifier(Protocol):
    def send(self, recipient: str, message: str) -> bool: ...
```

But a third-party SMS library (Twilio) has a different shape you **cannot modify**:

```python
class TwilioClient:                      # third-party — cannot be changed
    def send_text_message(self, from_number, to_number, body):
        print(f"Twilio: {body} -> {to_number}")
        return {"status": "queued"}
```

Mismatch: your app wants `send(recipient, message) -> bool`; Twilio offers
`send_text_message(from_number, to_number, body) -> dict`. Different method name,
parameters, and return type.

---

## The Fix: An Adapter

A small class that **implements your interface** and **wraps** the third-party
object, translating between the two.

```python
class TwilioAdapter:                          # implements YOUR Notifier interface
    def __init__(self, twilio_client: TwilioClient, from_number: str):
        self._twilio = twilio_client          # wraps the third-party object
        self._from = from_number

    def send(self, recipient: str, message: str) -> bool:   # YOUR interface shape
        # translate YOUR call -> TWILIO's call
        result = self._twilio.send_text_message(
            from_number=self._from,
            to_number=recipient,              # recipient -> to_number
            body=message,                     # message   -> body
        )
        # translate TWILIO's dict return -> YOUR bool
        return result["status"] == "queued"
```

**Usage** — Twilio now works anywhere a `Notifier` is expected, no special-casing:

```python
def alert_user(notifier: Notifier, user, msg):    # generic app code, unchanged
    notifier.send(user, msg)

twilio = TwilioClient()
sms_notifier = TwilioAdapter(twilio, from_number="+1555000000")

alert_user(sms_notifier, "+1555123456", "Your order shipped!")
```

`alert_user` has no idea Twilio exists — it only sees a `Notifier`.

---

## Why This Beats Scattering `isinstance` Checks

The alternative — special-casing Twilio at every call site — is much worse:

```python
# the BAD way, repeated everywhere
if isinstance(x, TwilioClient):
    x.send_text_message(from_number=..., to_number=user, body=msg)
else:
    x.send(user, msg)
```

The Adapter protects you by:

1. **Containing the quirks in one place** — Twilio's odd API lives only in the
   adapter, never leaking into call sites (DRY + Separation of Concerns).
2. **Keeping the app decoupled** — switch SMS providers by writing a new adapter;
   no app code changes (Open/Closed + Dependency Inversion).
3. **Removing conditional soup** — the app calls `notifier.send(...)` uniformly; no
   `isinstance` branches to maintain (and the adapter is a valid Liskov substitute).

> The Adapter **quarantines the mismatch** into one wrapper, so the incompatible
> third-party API never leaks into your codebase.

---

## When to Use It

- You have a class (usually **third-party** or **legacy**) whose interface you
  **can't or shouldn't change**, **and**
- It doesn't match the interface your code expects, **and**
- You want to use it without polluting your app with its quirks.

Real uses: wrapping third-party SDKs (payment gateways, SMS, cloud clients),
adapting legacy code to a new interface, making mismatched libraries
interchangeable.

## Adapter vs. Decorator

Both **wrap** an object, but for different reasons:

- **Adapter** — changes the *interface* (makes an incompatible thing fit).
- **Decorator** — keeps the *same* interface but *adds behavior*.

## How It Connects

- **Dependency Inversion** — the app depends on your abstraction; the adapter
  bridges to the concrete third-party class.
- **Open/Closed** — support a new provider by adding an adapter, not editing app code.
- **Liskov** — the adapter is a valid substitute for your interface.
- **Separation of Concerns** — translation is isolated from business logic.

## Summary Checklist

- [ ] Am I using a class whose interface I can't change?
- [ ] Does its API mismatch what my code expects?
- [ ] Did I wrap it in an adapter implementing *my* interface?
- [ ] Are the third-party quirks confined to the adapter only?

## Related Topics

- [SOLID Principles (Python)](../solid-principles.md)
- [Strategy Pattern (Python)](strategy.md)

---

**Tags**: #python #programming #design-patterns #adapter #clean-code

**Difficulty**: <span class="difficulty-intermediate">Intermediate</span>
