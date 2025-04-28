import re
from enum import Enum
from typing import Type

from evargs.exception import ValidateException

"""
Validator

This class provides comprehensive validation functionality for parameter values.
"""


class Validator:
    # any
    def validate_exist(self, v: any):
        """Validate value exist."""
        if self.get_length(v) == 0:
            self.raise_error('Require value.', v)

    def validate_size(self, v: any, size: int):
        """Validate object's length."""
        if not (self.get_length(v) == size):
            self.raise_error(f'Size must be {size}.', append_value=False)

    def validate_sizes(self, v: any, min_size: int = None, max_size: int = None):
        """Validate object's length by range."""
        size = self.get_length(v)

        if not ((min_size is None or min_size <= size) and (max_size is None or size <= max_size)):
            self.raise_error(f'Size must be "{min_size} - {max_size}".({size})', append_value=False)

    def get_length(self, v: any) -> int:
        try:
            if not isinstance(v, (int, float, complex)):
                size = len(v)
            else:
                size = 1
        except Exception:
            size = 0

        return size

    def validate_enum(self, v: any, enum_class: Type[Enum]):
        """Validate enum value."""
        values = [item.value for item in enum_class]

        if not (v in values):
            self.raise_error('Out of permitted values.', v)

    # str
    def validate_alphabet(self, v: str):
        """Validate alphabet chars."""
        if not (re.search(r'^[a-z]+$', v, flags=re.I)):
            self.raise_error('Require alphabet chars.', v)

    def validate_alphanumeric(self, v: str):
        """Validate alphanumeric chars."""
        if not (re.search(r'^[a-z0-9]+$', v, flags=re.I)):
            self.raise_error('Require alphanumeric chars.', v)

    def validate_ascii(self, v: str):
        """Validate ASCII chars."""
        if not (re.search(r'^[\x00-\x7F]+$', v, flags=re.I)):
            self.raise_error('Require ASCII chars.', v)

    def validate_printable_ascii(self, v: str):
        """Validate printable ASCII chars."""
        if not (re.search(r'^[\x20-\x7E]+$', v, flags=re.I)):
            self.raise_error('Require printable ASCII chars.', v)

    def validate_standard_ascii(self, v: str):
        """Validate standard ASCII chars."""
        if not (re.search(r'^[\x20-\x7E\x09\x0A\x0D]+$', v, flags=re.I)):
            self.raise_error('Require standard ASCII chars.', v)

    def validate_char_numeric(self, v: str):
        """Validate numeric chars."""
        if not (re.search(r'^[0-9]+$', v, flags=re.I)):
            self.raise_error('Require numeric chars.', v)

    def validate_regex(self, v: any, regex: str, *args):
        """Validate regex chars."""
        flags = args[0] if len(args) == 1 else 0

        if not (re.search(regex, str(v), flags=flags)):
            self.raise_error('Require regex matched chars.', v)

    # int, float
    def validate_range(self, v: any, min_v=None, max_v=None):
        """Validate numeric value b y range."""
        if not ((min_v is None or min_v <= v) and (max_v is None or v <= max_v)):
            self.raise_error(f'Require number in range.("{min_v} - {max_v}")', append_value=False)

    def validate_unsigned(self, v: any):
        """Validate unsigned value."""
        if not (isinstance(v, (int, float, complex)) and v >= 0):
            self.raise_error('Require unsigned value.', v)

    def validate_positive(self, v: any):
        """Validate positive value."""
        if not (isinstance(v, (int, float, complex)) and v > 0):
            self.raise_error('Require positive value.', v)

    def validate_negative(self, v: any):
        """Validate negative value."""
        if not (isinstance(v, (int, float, complex)) and v < 0):
            self.raise_error('Require negative value.', v)

    def validate_even(self, v: int):
        """Validate even value."""
        if not (isinstance(v, int) and v % 2 == 0):
            self.raise_error('Require even number.', v)

    def validate_odd(self, v: int):
        """Validate odd value."""
        if not (isinstance(v, int) and v % 2 == 1):
            self.raise_error('Require odd number.', v)

    def raise_error(self, msg: str, v: any = None, code=ValidateException.ERROR_GENERAL, append_value=True):
        if append_value:
            if isinstance(v, str):
                msg += f'(\'{v}\')'
            else:
                msg += f'({v})'

        raise ValidateException(msg, code)
