from typing import TYPE_CHECKING, Union
from decimal import Decimal, ROUND_HALF_EVEN, localcontext


class DecimalFormat:
    def __init__(self, pattern="#.###", *, grouping_used=None, grouping_size=3, rounding = ROUND_HALF_EVEN):
        """
        Initialize DecimalFormat with pattern similar to Java
        Args:
            pattern: Format pattern (default "#.###")
        """
        split = pattern.split(".")
        self.min_fraction_digits = 0
        if "." in pattern and split[1].startswith("0"):
            self.min_fraction_digits = len(split[1]) - len(split[1].lstrip("0"))
        self.max_fraction_digits = len(split[1]) if "." in pattern else 0
        if grouping_used is not None:
            self.grouping_used = grouping_used
        else:
            self.grouping_used = "," in split[0]
        self.grouping_size = grouping_size if grouping_size else 3
        self.rounding_mode = rounding

    def set_minimum_fraction_digits(self, digits):
        """Set the minimum number of digits allowed in the fraction portion"""
        self.min_fraction_digits = max(0, int(digits))
        if self.min_fraction_digits > self.max_fraction_digits:
            self.max_fraction_digits = self.min_fraction_digits
        return self

    def set_maximum_fraction_digits(self, digits):
        """Set the maximum number of digits allowed in the fraction portion"""
        self.max_fraction_digits = max(0, int(digits))
        if self.max_fraction_digits < self.min_fraction_digits:
            self.min_fraction_digits = self.max_fraction_digits
        return self

    def format(self, number: Union[int, float, Decimal, str]) -> str:
        """
        Format number according to the pattern
        Args:
            number: Number to format
        Returns:
            Formatted string
        """
        if number is None:
            return "0"

        # Round to maximum fraction digits
        with localcontext(prec=56) as ctx:
            rounded = Decimal(number).quantize(
                Decimal("1." + "0" * self.max_fraction_digits),
                rounding=self.rounding_mode,
            )

        # Format with maximum digits
        formatted = f"{rounded:.{self.max_fraction_digits}f}"

        if self.min_fraction_digits == 0:
            # Remove trailing zeros and decimal point if allowed
            formatted = formatted.rstrip("0").rstrip(".")
        else:
            # Ensure minimum number of fraction digits
            parts = formatted.split(".")
            if len(parts) == 1:
                formatted += "." + "0" * self.min_fraction_digits
            else:
                decimal_part = parts[1].ljust(self.min_fraction_digits, "0")
                formatted = f"{parts[0]}.{decimal_part}"

        # Apply grouping if enabled
        if self.grouping_used:
            parts = formatted.split(".")
            integer_part = parts[0]
            # Handle negative numbers
            sign = ""
            if integer_part.startswith("-"):
                sign = "-"
                integer_part = integer_part[1:]
            # Add group separators
            groups = []
            while integer_part:
                groups.insert(0, integer_part[-self.grouping_size :])
                integer_part = integer_part[: -self.grouping_size]
            integer_part = sign + ",".join(groups)
            formatted = integer_part + ("." + parts[1] if len(parts) > 1 else "")

        return formatted
