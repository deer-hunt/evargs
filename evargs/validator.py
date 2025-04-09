from evargs.exception import EvArgsException, EvValidateException
import re


class Validator:
    # str
    def validate_size(self, name: str, v: str, size: int):
        if not (len(v) == size):
            self.raise_error('Character length must be {}.({})'.format(size, name))

    def validate_between(self, name: str, v: str, min_size: int, max_size: int):
        vl = len(v)

        if not ((min_size is None or min_size <= vl) and (max_size is None or vl <= max_size)):
            self.raise_error('Character length must be "{} - {}".({}; {})'.format(min_size, max_size, name, vl))

    def validate_alphabet(self, name: str, v: str):
        if not (re.search(r'^[a-z]+$', v, flags=re.I)):
            self.raise_error('Require alphabet chars.({})'.format(name))

    def validate_alphanumeric(self, name: str, v: str):
        if not (re.search(r'^[a-z0-9]+$', v, flags=re.I)):
            self.raise_error('Require alphanumeric chars.({})'.format(name))

    def validate_ascii(self, name: str, v: str):
        if not (re.search(r'^[\x00-\x7F]+$', v, flags=re.I)):
            self.raise_error('Require ASCII chars.({})'.format(name))

    def validate_printable_ascii(self, name: str, v: str):
        if not (re.search(r'^[\x20-\x7E]+$', v, flags=re.I)):
            self.raise_error('Require printable ASCII chars.({})'.format(name))

    def validate_standard_ascii(self, name: str, v: str):
        if not (re.search(r'^[\x20-\x7E\x09\x0A\x0D]+$', v, flags=re.I)):
            self.raise_error('Require standard ASCII chars.({})'.format(name))

    def validate_char_numeric(self, name: str, v: str):
        if not (re.search(r'^[0-9]+$', v, flags=re.I)):
            self.raise_error('Require numeric chars.({})'.format(name))

    def validate_regex(self, name: str, v: any, regex: str, *args):
        flags = args[0] if len(args) == 1 else 0

        if not (re.search(regex, str(v), flags=flags)):
            self.raise_error('Require regex matched chars.({}; "{}")'.format(name, regex))

    # int, float
    def validate_range(self, name: str, v: any, min_v, max_v):
        if not ((min_v is None or min_v <= v) and (max_v is None or v <= max_v)):
            self.raise_error('Require number in range.({}; "{} - {}")'.format(name, min_v, max_v))

    def validate_unsigned(self, name: str, v: any):
        if not (isinstance(v, (int, float, complex)) and v >= 0):
            self.raise_error('Require unsigned value.({})'.format(name))

    def validate_even(self, name: str, v: any):
        if not (isinstance(v, int) and v % 2 == 0):
            self.raise_error('Require even number.({})'.format(name))

    def validate_odd(self, name: str, v: any):
        if not (isinstance(v, int) and v % 2 == 1):
            self.raise_error('Require odd number.({})'.format(name))

    def raise_error(self, msg, code=EvValidateException.ERROR_GENERAL):
        raise EvValidateException(msg, code)
