from evargs import EvArgs, EvArgsException, EvValidateException
from evargs.validator import Validator
import pytest
import re


# Document: https://github.com/deer-hunt/evargs/
class TestRuleValidate:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_choices(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': int, 'choices': [1, 2, 3]},
            'b': {'type': str, 'choices': ['A', 'B', 'C']}
        }).parse('a=3;b=A')

        assert evargs.get('a') == 3
        assert evargs.get('b') == 'A'

        # Exception
        with pytest.raises(EvValidateException):
            evargs.parse('a=5;')

        with pytest.raises(EvValidateException):
            evargs.parse('b=Z;')

    def test_validate_number(self):
        evargs = EvArgs()

        # unsigned
        evargs.initialize({
            'a': {'type': int, 'validation': 'unsigned'},
        }).parse('a=1;')

        assert evargs.get('a') == 1

        # range
        evargs.initialize({
            'a': {'type': int, 'validation': ('range', None, 200)},
            'b': {'type': int, 'validation': ['range', 100, None]},
            'c': {'type': float, 'validation': [('unsigned',), ('range', 1, 200)]},
        }).parse('a=123;b=200;c=199.9')

        assert evargs.get('a') == 123
        assert evargs.get('c') == 199.9

    def test_validate_size(self):
        evargs = EvArgs()

        # size
        evargs.initialize({
            'a': {'type': str, 'validation': ['size', 3]},
        }).parse('a=ABC;')

        # between
        evargs.initialize({
            'a': {'type': str, 'validation': ['between', 4, None]},
            'b': {'type': str, 'validation': ['between', None, 10]},
        }).parse('a=ABCD;b=ABCDEFGHI')

        assert evargs.get('a') == 'ABCD'
        assert evargs.get('b') == 'ABCDEFGHI'

    def test_validate_str(self):
        evargs = EvArgs()

        # alphabet
        evargs.initialize({
            'a': {'type': str, 'validation': 'alphabet'},
            'b': {'type': str, 'validation': [tuple(['alphabet']), ('between', 4, None)]},
        }).parse('a=AbcD;')

        assert evargs.get('a') == 'AbcD'

        evargs.initialize({
            'a': {'type': str, 'validation': 'alphanumeric'},
        }).parse('a=Abc123;')

        assert evargs.get('a') == 'Abc123'

        # printable_ascii
        evargs.initialize({
            'a': {'type': str, 'validation': 'printable_ascii'},
        }).parse('a="Abc 123";')

        assert evargs.get('a') == 'Abc 123'

    def test_validate_regex(self):
        evargs = EvArgs()

        # regex
        evargs.initialize({
            'a': {'type': int, 'validation': ['regex', r'^\d{3}$']},
            'b': {'type': str, 'validation': ['regex', r'^ABC\d{5,10}XYZ$', re.I]},
        }).parse('a=123;b=AbC12345XyZ')

        assert evargs.get('a') == 123
        assert evargs.get('b') == 'AbC12345XyZ'

        evargs.initialize({
            'dna': {'type': str, 'validation': ['regex', r'^[ATGC]+$']},
        }).parse('dna=ATGCGTACGTAGCTAGCTAGCTAGCATCGTAGCTAGCTAGC')

        assert evargs.get('dna') == 'ATGCGTACGTAGCTAGCTAGCTAGCATCGTAGCTAGCTAGC'

        # Exception
        with pytest.raises(EvValidateException):
            evargs.initialize({
                'a': {'type': str, 'validation': ['regex', r'^XYZ.+$']},
            }).parse('a=123XYZ')

    def test_multiple_validation(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': str, 'validation': [('size', 4), ('alphabet',)]},
            'b': {'type': int, 'validation': [('range', 1, 50), ('odd',)]},
            'c': {'type': str, 'validation': [('between', 5, 10), tuple(['regex', '^[a-z]+$'])]},
        }).parse('a=ABCD;b=3;c=acdefg')

        assert evargs.get('a') == 'ABCD'
        assert evargs.get('b') == 3
        assert evargs.get('c') == 'acdefg'

        # Exception
        with pytest.raises(EvValidateException):
            evargs.parse('a=ABC;')

    def test_validate_method(self):
        evargs = EvArgs()

        # method
        evargs.initialize({
            'a': {'type': int, 'validation': lambda n, v: True if v >= 0 else False},
        }).parse('a=1;')

        assert evargs.get('a') == 1

        # Exception
        with pytest.raises(EvValidateException):
            evargs.initialize({
                'a': {'type': int, 'validation': lambda n, v: True if v >= 0 else False},
                'b': {'type': int, 'validation': lambda n, v: True if v >= 0 else False},
            }).parse('a=1;b = - 8;')


class MyValidator(Validator):
    def validate_length_limit(self, name: str, v):
        if not (len(v) == 8 or len(v) == 24):
            self.raise_error('Length is not 128,256.')


class TestExtendValidator():
    def test1(self):
        validator = MyValidator()

        evargs = EvArgs()

        evargs.set_validator(validator)

        # length_limit = MyValidator::validate_length_limit
        evargs.initialize({
            'a': {'type': str, 'validation': 'length_limit'},
        })

        evargs.parse('a=12345678;')

        assert evargs.get('a') == '12345678'
