"""Reusable, schema-driven row validation for research datasets."""

import math
from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType


def _is_missing(value):
    return value is None or str(value).strip() == ""


@dataclass(frozen=True)
class NumericRule:
    """Inclusive numeric bounds and optional integer-only validation."""

    minimum: float | None = None
    maximum: float | None = None
    integer: bool = False

    def __post_init__(self):
        for name in ("minimum", "maximum"):
            value = getattr(self, name)
            if value is None:
                continue
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise TypeError(f"{name} must be a finite number or None")
            if not math.isfinite(value):
                raise ValueError(f"{name} must be finite")
            object.__setattr__(self, name, float(value))
        if (
            self.minimum is not None
            and self.maximum is not None
            and self.minimum > self.maximum
        ):
            raise ValueError("minimum cannot be greater than maximum")
        if not isinstance(self.integer, bool):
            raise TypeError("integer must be a boolean")


@dataclass(frozen=True)
class ValidationSchema:
    """Describe required fields, numeric constraints, and an identifier column.

    Numeric fields are optional unless they are also listed in required_fields.
    Minimum and maximum values are inclusive.
    """

    required_fields: tuple[str, ...] = ()
    numeric_rules: Mapping[str, NumericRule] = field(default_factory=dict)
    identifier_column: str | None = None

    def __post_init__(self):
        if isinstance(self.required_fields, str):
            raise TypeError("required_fields must be a sequence of field names")
        required_fields = tuple(self.required_fields)
        if any(not isinstance(name, str) or not name.strip() for name in required_fields):
            raise ValueError("required field names must be non-empty strings")
        if len(set(required_fields)) != len(required_fields):
            raise ValueError("required_fields cannot contain duplicates")
        if not isinstance(self.numeric_rules, Mapping):
            raise TypeError("numeric_rules must be a mapping")
        numeric_rules = dict(self.numeric_rules)
        for name, rule in numeric_rules.items():
            if not isinstance(name, str) or not name.strip():
                raise ValueError("numeric rule field names must be non-empty strings")
            if not isinstance(rule, NumericRule):
                raise TypeError(f"numeric rule for {name!r} must be a NumericRule")
        if self.identifier_column is not None and (
            not isinstance(self.identifier_column, str)
            or not self.identifier_column.strip()
        ):
            raise ValueError("identifier_column must be a non-empty string or None")
        object.__setattr__(self, "required_fields", required_fields)
        object.__setattr__(self, "numeric_rules", MappingProxyType(numeric_rules))

    def validate(self, row):
        """Return True for a valid row, otherwise a list of validation errors."""
        if not isinstance(row, Mapping):
            raise TypeError("row must be a mapping of column names to values")

        errors = []
        missing_fields = set()
        for name in self.required_fields:
            if name not in row:
                missing_fields.add(name)
                errors.append(f"The {name} key is missing")
            elif _is_missing(row[name]):
                missing_fields.add(name)
                errors.append(f"Value of {name} is missing")

        for name, rule in self.numeric_rules.items():
            if name not in row or _is_missing(row[name]):
                continue
            value = row[name]
            if isinstance(value, bool):
                errors.append(f"The value {value} in {name} must be a number")
                continue
            try:
                number = float(value)
            except (ValueError, TypeError, OverflowError):
                errors.append(f"The value {value} in {name} must be a number")
                continue
            if not math.isfinite(number):
                errors.append(f"{name} must be a finite number")
                continue
            if rule.integer and not number.is_integer():
                errors.append(f"{name} must be an integer")
                continue
            if rule.minimum is not None and number < rule.minimum:
                errors.append(f"{name} must be at least {rule.minimum:g}")
            if rule.maximum is not None and number > rule.maximum:
                errors.append(f"{name} must be at most {rule.maximum:g}")

        return errors if errors else True
