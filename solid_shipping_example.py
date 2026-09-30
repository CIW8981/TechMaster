"""
SOLID by first principles — worked example (Principles 1 & 2 so far).

Demonstrates:
  - Single Responsibility (SRP):  each class has ONE reason to change
  - Open/Closed (OCP):            add new shipping types WITHOUT editing tested code
  - Duck typing + Protocol:       behavior-based contracts, verified by mypy
  - Pydantic validation:          validate DATA, separate from BEHAVIOR

Run:  python solid_shipping_example.py
"""

from typing import Protocol
from pydantic import BaseModel, field_validator


# ---------------------------------------------------------------------------
# 1. THE CONTRACT  (an abstraction — "what does a shipping strategy look like?")
#
#    A Protocol describes a SHAPE: "anything with cost(weight) -> float".
#    Strategies below do NOT inherit from it — thanks to DUCK TYPING, Python
#    only cares that they HAVE a .cost() method, not what class they are.
#    The Protocol exists for documentation + static checking (mypy).
# ---------------------------------------------------------------------------
class ShippingStrategy(Protocol):
    def cost(self, weight: float) -> float: ...


# ---------------------------------------------------------------------------
# 2. THE CONCRETE STRATEGIES  (BEHAVIOR)
#
#    SRP: each strategy has exactly one reason to change — its own pricing rule.
#    A change to Express pricing never touches Standard or Overnight.
# ---------------------------------------------------------------------------
class Standard:
    def cost(self, weight: float) -> float:
        return weight * 1.0


class Express:
    def cost(self, weight: float) -> float:
        return weight * 2.5


class Overnight:
    def cost(self, weight: float) -> float:
        return weight * 5.0


# ---------------------------------------------------------------------------
# 3. THE DATA  (validated by Pydantic)
#
#    SRP again: Package's only job is to hold valid data.
#    Pydantic answers "is this DATA valid?" (weight > 0) — NOT "what's the
#    behavior?". Behavior lives in the strategy. Keep the two responsibilities
#    separate.
# ---------------------------------------------------------------------------
class Package(BaseModel):
    weight: float
    strategy: ShippingStrategy

    # A strategy is a duck-typed behavioral object, not a standard Pydantic
    # type, so we must allow arbitrary types here.
    model_config = {"arbitrary_types_allowed": True}

    @field_validator("weight")
    @classmethod
    def weight_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("weight must be positive")
        return v


# ---------------------------------------------------------------------------
# 4. THE CALCULATOR  (OPEN/CLOSED)
#
#    Closed to modification: cost() is frozen — it never needs editing again.
#    Open to extension:      support new shipping types by ADDING new strategy
#                            classes, not by editing this method.
# ---------------------------------------------------------------------------
class ShippingCalculator:
    def cost(self, package: Package) -> float:
        return package.strategy.cost(package.weight)


# ---------------------------------------------------------------------------
# 5. USAGE
# ---------------------------------------------------------------------------
def main() -> None:
    calc = ShippingCalculator()

    p1 = Package(weight=10, strategy=Standard())
    p2 = Package(weight=10, strategy=Express())
    p3 = Package(weight=10, strategy=Overnight())

    print("Standard :", calc.cost(p1))   # 10.0
    print("Express  :", calc.cost(p2))   # 25.0
    print("Overnight:", calc.cost(p3))   # 50.0

    # --- OPEN/CLOSED IN ACTION -------------------------------------------
    # Business wants Drone shipping. We ADD a class. We do NOT touch
    # ShippingCalculator.cost() or any existing, tested strategy.
    class Drone:
        def cost(self, weight: float) -> float:
            return weight * 8.0

    p4 = Package(weight=10, strategy=Drone())
    print("Drone    :", calc.cost(p4))   # 80.0

    # --- PYDANTIC VALIDATION IN ACTION -----------------------------------
    # Invalid DATA is rejected at construction time, before any cost is
    # computed. The old plain class would have silently returned -12.5.
    try:
        Package(weight=-5, strategy=Express())
    except Exception as e:
        print("\nRejected invalid package (weight=-5):")
        print(e)


if __name__ == "__main__":
    main()
