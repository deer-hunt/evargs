from evargs.validator import Validator
from evargs.exception import EvValidateException
import pytest
import re


# Document: https://github.com/deer-hunt/evargs/
class TestValidator:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.validator = Validator()

    def test_validate_alphabet(self):
        self.validator.validate_alphabet('test1', 'abc')

        with pytest.raises(EvValidateException):
            self.validator.validate_alphabet('test2', '123')

    def test_validate_alphanumeric(self):
        self.validator.validate_alphanumeric('test1', 'abc123')

        with pytest.raises(EvValidateException):
            self.validator.validate_alphanumeric('test2', 'abc#123')

    def test_validate_ascii(self):
        self.validator.validate_ascii('test1', 'abc123')

        with pytest.raises(EvValidateException):
            self.validator.validate_ascii('test2', 'abc123ñ')

    def test_validate_printable_ascii(self):
        self.validator.validate_printable_ascii('test1', 'abc123')

        with pytest.raises(EvValidateException):
            self.validator.validate_printable_ascii('test2', 'abc123ñ')

    def test_validate_standard_ascii(self):
        self.validator.validate_standard_ascii('test1', 'abc123\t')

        with pytest.raises(EvValidateException):
            self.validator.validate_standard_ascii('test2', 'abc123ñ')

    def test_validate_char_numeric(self):
        self.validator.validate_char_numeric('test1', '123')

        with pytest.raises(EvValidateException):
            self.validator.validate_char_numeric('test2', 'abc123')

    def test_validate_regex(self):
        self.validator.validate_regex('test1', 'abc123', r'^[a-z0-9]+$')

        self.validator.validate_regex('dna', 'ATGCGTACGTAGCTAGCTAGCTAGCATCGTAGCTAGCTAGC', r'^[ATGC]+$')

        self.validator.validate_regex('base64', 'SGVsbG8gd29ybGQhMTIzNDU2', r'^[A-Za-z0-9+/=]+$')

        with pytest.raises(EvValidateException):
            self.validator.validate_regex('error1', 'abc#123', r'^[a-z0-9]+$')

        with pytest.raises(EvValidateException):
            self.validator.validate_regex('error2', 'ABC', r'^XYZ.+$')

    def test_validate_unsigned(self):
        self.validator.validate_unsigned('test1', 123)

        with pytest.raises(EvValidateException):
            self.validator.validate_unsigned('test2', -123)

    def test_validate_even(self):
        self.validator.validate_even('test1', 2)

        with pytest.raises(EvValidateException):
            self.validator.validate_even('test2', 3)

    def test_validate_odd(self):
        self.validator.validate_odd('test1', 3)

        with pytest.raises(EvValidateException):
            self.validator.validate_odd('test2', 2)

    def test_validate_range(self):
        self.validator.validate_range('test1', 5, 1, 10)

        with pytest.raises(EvValidateException):
            self.validator.validate_range('test2', 11, 1, 10)
