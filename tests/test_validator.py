from evargs.validator import Validator
from evargs.exception import ValidateException
import pytest
import re


# Document: https://github.com/deer-hunt/evargs/
class TestValidator:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.validator = Validator()

    def test_validate_exist(self):
        self.validator.validate_exist([1, 2])

        with pytest.raises(ValidateException):
            self.validator.validate_exist([])

    def test_validate_size(self):
        self.validator.validate_size('abc', 3)

        with pytest.raises(ValidateException):
            self.validator.validate_size('abc', 5)

        self.validator.validate_size([1, 2], 2)

    def test_validate_sizes(self):
        self.validator.validate_sizes('abc', 1, 10)

        with pytest.raises(ValidateException):
            self.validator.validate_sizes('abc', 10, 20)

        self.validator.validate_sizes([1, 2], 1, 2)
        self.validator.validate_sizes([1, 2], None, 2)
        self.validator.validate_sizes([1, 2], 1, None)

    def test_validate_alphabet(self):
        self.validator.validate_alphabet('abc')

        with pytest.raises(ValidateException):
            self.validator.validate_alphabet('123')

    def test_validate_alphanumeric(self):
        self.validator.validate_alphanumeric('abc123')

        with pytest.raises(ValidateException):
            self.validator.validate_alphanumeric('abc#123')

    def test_validate_ascii(self):
        self.validator.validate_ascii('abc123')

        with pytest.raises(ValidateException):
            self.validator.validate_ascii('abc123ñ')

    def test_validate_printable_ascii(self):
        self.validator.validate_printable_ascii('abc123')

        with pytest.raises(ValidateException):
            self.validator.validate_printable_ascii('abc123ñ')

    def test_validate_standard_ascii(self):
        self.validator.validate_standard_ascii('abc123\t')

        with pytest.raises(ValidateException):
            self.validator.validate_standard_ascii('abc123ñ')

    def test_validate_char_numeric(self):
        self.validator.validate_char_numeric('123')

        with pytest.raises(ValidateException):
            self.validator.validate_char_numeric('abc123')

    def test_validate_regex(self):
        self.validator.validate_regex('abc123', r'^[a-z0-9]+$')

        # dna
        self.validator.validate_regex('ATGCGTACGTAGCTAGCTAGCTAGCATCGTAGCTAGCTAGC', r'^[ATGC]+$')

        # base64
        self.validator.validate_regex('SGVsbG8gd29ybGQhMTIzNDU2', r'^[A-Za-z0-9+/=]+$')

        with pytest.raises(ValidateException):
            self.validator.validate_regex('abc#123', r'^[a-z0-9]+$')

        with pytest.raises(ValidateException):
            self.validator.validate_regex('ABC', r'^XYZ.+$')

    def test_validate_unsigned(self):
        self.validator.validate_unsigned(123)

        with pytest.raises(ValidateException):
            self.validator.validate_unsigned(-123)

    def test_validate_positive(self):
        self.validator.validate_positive(1)

        with pytest.raises(ValidateException):
            self.validator.validate_positive(0)

        with pytest.raises(ValidateException):
            self.validator.validate_positive(-1)

    def test_validate_negative(self):
        self.validator.validate_negative(-1)

        with pytest.raises(ValidateException):
            self.validator.validate_negative(0)

        with pytest.raises(ValidateException):
            self.validator.validate_negative(1)

    def test_validate_even(self):
        self.validator.validate_even(2)

        with pytest.raises(ValidateException):
            self.validator.validate_even(3)

    def test_validate_odd(self):
        self.validator.validate_odd(3)

        with pytest.raises(ValidateException):
            self.validator.validate_odd(2)

    def test_validate_range(self):
        self.validator.validate_range(5, 1, 10)

        with pytest.raises(ValidateException):
            self.validator.validate_range(11, 1, 10)
