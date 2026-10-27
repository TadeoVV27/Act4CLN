from decimal import Decimal

class Specification:
    def is_satisfied_by(self, order):
        raise NotImplementedError

    def __and__(self, other):
        return AndSpec(self, other)

    def __or__(self, other):
        return OrSpec(self, other)

    def __invert__(self):
        return NotSpec(self)

class AndSpec(Specification):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def is_satisfied_by(self, order):
        return self.left.is_satisfied_by(order) and self.right.is_satisfied_by(order)

class OrSpec(Specification):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def is_satisfied_by(self, order):
        return self.left.is_satisfied_by(order) or self.right.is_satisfied_by(order)

class NotSpec(Specification):
    def __init__(self, spec):
        self.spec = spec

    def is_satisfied_by(self, order):
        return not self.spec.is_satisfied_by(order)

class MinimumAmountSpec(Specification):
    def __init__(self, minimum_amount: Decimal):
        self.minimum_amount = minimum_amount

    def is_satisfied_by(self, order):
        # Utiliza estrictamente mayor que (>) como indica la guía
        return order.total.amount > self.minimum_amount

class VIPCustomerSpec(Specification):
    def is_satisfied_by(self, order):
        return order.customer.is_vip

class MinimumUnitsSpec(Specification):
    def __init__(self, minimum_units: int):
        self.minimum_units = minimum_units

    def is_satisfied_by(self, order):
        return order.units >= self.minimum_units

class ActivePromotionSpec(Specification):
    def is_satisfied_by(self, order):
        return order.has_promotion

# Regla de descuento de 10 %
ten_percent = (
    MinimumAmountSpec(Decimal("500"))
    & VIPCustomerSpec()
    & MinimumUnitsSpec(4)
    & ~ActivePromotionSpec()
)

# Regla de 5 %: total > 5000 y SIN promoción
five_percent = (
    MinimumAmountSpec(Decimal("5000"))
    & ~ActivePromotionSpec()
)

# Combinación con OR
any_discount = ten_percent | five_percent