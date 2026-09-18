---
title: "Observer Pattern (Python)"
description: "Learn the Observer design pattern from first principles with Python examples, plus how it maps to AWS SNS/SQS for distributed pub/sub"
tags:
  - python
  - programming
  - design-patterns
  - observer
  - clean-code
difficulty: intermediate
last_updated: "2026-09-18"
---

# Observer Pattern

!!! info "The pattern"
    Define a one-to-many dependency so that when one object (the **subject**)
    changes state or emits an event, all its registered dependents
    (**observers**) are notified automatically — **without the subject knowing
    their concrete types**.

## Introduction

Where Strategy answers "which algorithm?" and Factory answers "who creates it?",
Observer answers: *"when something happens, notify everyone who cares — without the
source knowing who they are."*

---

## The Problem

Follow-up actions after placing an order are hardcoded into the service:

```python
class OrderService:
    def place_order(self, order):
        # ...save the order...
        EmailService().send_confirmation(order)
        InventorySystem().reduce_stock(order)
        AnalyticsService().track_purchase(order)
        WarehouseSystem().notify(order)
```

Problems:

- **Violates Open/Closed** — every new action (SMS, loyalty points, fraud check)
  forces editing `place_order`.
- **Tightly coupled** — `OrderService` directly depends on four concrete systems.
- **Fragile** — if one system throws, it can break the whole flow.
- **Hard to test** — you can't test order placement without all four systems.

---

## The Fix: Observer (subscribe / notify)

The subject keeps a list of subscribers and just **announces** the event; each
observer decides how to react.

```python
from typing import Protocol


# The observer contract
class OrderObserver(Protocol):
    def on_order_placed(self, order) -> None: ...


# The subject — maintains subscribers and announces events
class OrderService:
    def __init__(self):
        self._observers: list[OrderObserver] = []

    def subscribe(self, observer: OrderObserver) -> None:      # register
        self._observers.append(observer)

    def place_order(self, order):
        # ...save the order...
        self._notify(order)                     # announce — don't know who listens

    def _notify(self, order):
        for observer in self._observers:
            try:
                observer.on_order_placed(order)
            except Exception as e:               # one failure doesn't kill the rest
                print(f"observer failed: {e}")


# Each subscriber owns its own reaction, in one place
class EmailObserver:
    def on_order_placed(self, order):
        print(f"Sending confirmation email for {order}")

class InventoryObserver:
    def on_order_placed(self, order):
        print(f"Reducing stock for {order}")

class AnalyticsObserver:
    def on_order_placed(self, order):
        print(f"Tracking purchase {order}")
```

**Usage** — wire up subscribers *outside* the subject:

```python
service = OrderService()
service.subscribe(EmailObserver())
service.subscribe(InventoryObserver())
service.subscribe(AnalyticsObserver())

service.place_order("Book x2")
# all three react; OrderService never named any of them
```

Adding SMS? Write `SmsObserver` and `service.subscribe(SmsObserver())` —
`place_order` is never touched.

---

## The Fundamental Shift: Dependency Direction

- **Naive:** `OrderService` → depends on → `EmailService`, `InventorySystem`, ...
  (the subject knows every subscriber; adding one changes the subject).
- **Observer:** observers depend on the `OrderObserver` interface and register
  themselves; `OrderService` depends on **nothing concrete** — only an abstract
  list of observers.

The dependency **inverts**: subscribers know the publisher, not the other way
around. This is Dependency Inversion at the event level, and it's why new reactions
never require editing the subject.

---

## Observer at Cloud Scale: AWS SNS/SQS

Observer is the **in-process** version of pub/sub. The same pattern implemented as
**distributed infrastructure** is AWS SNS/SQS (or Kafka, EventBridge):

| Observer (in-process) | Distributed (AWS) |
|-----------------------|-------------------|
| Subject / Publisher | SNS topic |
| Observers / Subscribers | SQS queues, Lambdas, email endpoints |
| `subscribe()` | topic subscription |
| `notify()` | `sns.publish()` |

In both, the publisher broadcasts an event and does **not** know who consumes it —
the exact decoupling Observer provides.

---

## When to Use It

- One event must trigger **multiple, independent reactions**, **and**
- You want to add/remove reactions **without modifying** the event source, **and**
- The source **shouldn't be coupled** to what happens next.

Classic uses: event systems, UI model→view updates, pub/sub, notifications, and
distributed messaging (SNS/SQS, Kafka, EventBridge).

## How It Connects

- **Open/Closed** — add observers without editing the subject.
- **Dependency Inversion** — the subject depends on the observer abstraction.
- **Separation of Concerns** — each reaction is isolated in its own observer.
- **Cloud architecture** — SNS/SQS/Kafka are Observer as distributed infrastructure.

## Summary Checklist

- [ ] Does one event need to trigger several independent reactions?
- [ ] Are follow-up actions hardcoded into the event source?
- [ ] Can I add a reaction by subscribing a new observer (no edit to the subject)?
- [ ] Should one failing observer be isolated from the others?

## Related Topics

- [SOLID Principles (Python)](../solid-principles.md)
- [Strategy Pattern (Python)](strategy.md)
- [Separation of Concerns (Python)](../separation-of-concerns.md)

---

**Tags**: #python #programming #design-patterns #observer #clean-code

**Difficulty**: <span class="difficulty-intermediate">Intermediate</span>
