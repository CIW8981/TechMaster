---
title: "Composition over Inheritance (Python)"
description: "Learn why to favor composition over inheritance from first principles, with Python examples covering the class explosion and diamond problems"
tags:
  - python
  - programming
  - design-principles
  - composition
  - clean-code
difficulty: intermediate
last_updated: "2026-09-17"
---

# Composition over Inheritance

!!! info "The principle"
    Build behavior by **combining** small, focused objects (has-a) rather than
    inheriting from a rigid parent chain (is-a). This is the practical fix for the
    inheritance pain that [SOLID's Liskov principle](solid-principles.md) warns
    about.

## Introduction

Inheritance models **"is-a"** — a rigid, single-parent chain. The real world is
often about **"can-do" capabilities** that mix freely across roles. When
capabilities combine in arbitrary ways, a single inheritance tree cannot express
them without duplication or ambiguity.

!!! note "Read as: *favor*, not *forbid*"
    "Favor composition over inheritance" means **prefer composition as the
    default** — not "never use inheritance." Inheritance is still the right tool
    for a stable, genuine *is-a* relationship.

---

## The Problem

Modeling employees with inheritance looks reasonable at first:

```python
class Employee:
    def work(self):
        print("working...")


class Manager(Employee):
    def manage(self):
        print("managing team...")


class Engineer(Employee):
    def code(self):
        print("writing code...")
```

Then reality arrives:

1. Some engineers become **team leads** — they `code()` **and** `manage()`.
2. **Contractors** `code()` but are **not** employees.
3. A **CTO** `manage()`s, `code()`s, **and** does executive work.

### Where does `TeamLead` go?

A `TeamLead` needs both `code()` and `manage()`. Every inheritance option is bad:

=== "Option A: copy manage()"

    ```python
    class TeamLead(Engineer):
        def manage(self):            # duplicated from Manager — DRY violation
            print("managing team...")
    ```

=== "Option B: multiple inheritance"

    ```python
    class TeamLead(Engineer, Manager):   # diamond problem:
        pass                             # Employee inherited via two paths
    ```

=== "Option C: new branch"

    ```python
    # Duplicate everything into a fresh class — worst of all
    ```

Add the CTO and contractors, and **every new combination of capabilities forces a
new awkward class or more multiple inheritance**. This is the **class explosion
problem**, and Option B invites the **diamond problem** (ambiguous method
resolution through a shared grandparent).

---

## The Fix: Composition

Stop asking *"what is this employee?"* and ask *"what can it do?"* — then **plug in**
capabilities as objects.

```python
# --- Behavior/component classes: one capability each ---
class CodingSkill:
    def code(self):
        print("writing code...")


class ManagementSkill:
    def manage(self):
        print("managing team...")


class ExecutiveSkill:
    def set_strategy(self):
        print("setting company strategy...")


# --- Roles COMPOSE the capabilities they need (no inheritance tree) ---
class Engineer:
    def __init__(self):
        self.coding = CodingSkill()

    def code(self):
        self.coding.code()


class TeamLead:
    def __init__(self):
        self.coding = CodingSkill()          # has coding
        self.management = ManagementSkill()  # AND management

    def code(self):
        self.coding.code()

    def manage(self):
        self.management.manage()


class CTO:
    def __init__(self):
        self.coding = CodingSkill()
        self.management = ManagementSkill()
        self.executive = ExecutiveSkill()    # any combination, freely

    def code(self):       self.coding.code()
    def manage(self):     self.management.manage()
    def strategize(self): self.executive.set_strategy()
```

**Usage:**

```python
lead = TeamLead()
lead.code()      # writing code...
lead.manage()    # managing team...
```

### What composition fixed

- **No class explosion** — a new role just picks the capabilities it needs.
- **No duplication** — `manage()` logic lives in one place (`ManagementSkill`),
  reused by `TeamLead` and `CTO` (DRY preserved).
- **No diamond problem** — there is no shared parent to inherit twice.
- **Contractors are trivial** — compose `CodingSkill` without any `Employee` baggage.

!!! tip "What kind of classes are these?"
    `CodingSkill`, `ManagementSkill`, `ExecutiveSkill` are **component / behavior
    classes** — small, focused units of *behavior* meant to be plugged into other
    objects. They are neither *data classes* nor *interfaces*. If they were made
    swappable at runtime, they would be **strategies**; if delivered via
    inheritance, **mixins**.

---

## When to Use Which

Composition is **flexible and reversible**; inheritance is **rigid and
committing**. When unsure, **default to composition** — it preserves your options
(aligns with YAGNI and KISS).

| Question | Lean toward |
|---|---|
| Not sure about the future? | **Composition** (keeps options open) |
| Capabilities that combine in different ways? | **Composition** |
| Might a subclass *not* be fully substitutable? | **Composition** |
| Stable, permanent "is-a" with no mixing? | Inheritance is fine |
| Need to share concrete implementation from a parent? | Inheritance is reasonable |
| Extending a framework's designed base class? | Inheritance (it's built for it) |

!!! success "The habit"
    **Start with composition; only "promote" to inheritance once a true, stable
    is-a relationship has clearly proven itself.** It is far easier to move from
    composition to inheritance later than to untangle a wrong inheritance tree.

### Use inheritance only when ALL hold

1. A true, **stable "is-a"** (e.g., `SavingsAccount` *is a* `BankAccount`).
2. **No capability mixing** — one clean lineage, not arbitrary skill combos.
3. You want to **share real implementation code** from the parent.
4. **Substitutability holds** — every subclass passes the Liskov test.

---

## How It Connects

- **Liskov (SOLID)** — composition sidesteps fragile parent-child behavioral
  promises entirely; there is no substitutability contract to break.
- **DRY** — each capability is defined exactly once and reused.
- **YAGNI / KISS** — composition avoids committing to a rigid hierarchy for an
  unknown future.

## Summary Checklist

- [ ] Am I modeling a stable *is-a*, or combinable *can-do* capabilities?
- [ ] Would new requirements cause a class explosion under inheritance?
- [ ] When unsure, did I default to composition?
- [ ] Did I reserve inheritance for stable is-a relationships that pass Liskov?

## Related Topics

- [SOLID Principles (Python)](solid-principles.md)
- [DRY, KISS & YAGNI (Python)](dry-kiss-yagni.md)

---

**Tags**: #python #programming #composition #inheritance #clean-code

**Difficulty**: <span class="difficulty-intermediate">Intermediate</span>
