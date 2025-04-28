from evargs import EvArgs, EvArgsException, ValidateException
from evargs.validator import Validator
from enum import Enum
import pytest
import re


# Document: https://github.com/deer-hunt/evargs/
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
    EMERALD_GREEN = 2.5


class TestRuleValidation:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_required(self):
        evargs = EvArgs()

        assert evargs.assign('1', cast=int, required=True) == 1

        with pytest.raises(ValidateException):
            assert evargs.assign('', cast=int, required=True)

    def test_exist(self):
        evargs = EvArgs()

        assert evargs.assign('1', cast=str, validation='exist') == '1'
        assert evargs.assign(0, cast=int, validation='exist') == 0

        with pytest.raises(ValidateException):
            assert evargs.assign('', cast=str, validation='exist')

        assert evargs.assign(['1', '2', '3'], cast=int, list=True, post_apply='exist') == [1, 2, 3]

        with pytest.raises(ValidateException):
            assert evargs.assign([], cast=int, validation='exist')

    def test_size(self):
        evargs = EvArgs()

        evargs.assign('abc', cast=str, validation=('size', 3))
        evargs.assign([1, 2, 3], validation=('size', 3))
        evargs.assign(b'abc', validation=('size', 3))

        with pytest.raises(ValidateException):
            evargs.assign('abc', cast=str, validation=('size', 2))

        with pytest.raises(ValidateException):
            evargs.assign([1, 2, 3], validation=('size', 2))

    def test_sizes(self):
        evargs = EvArgs()

        evargs.assign('abc', cast=str, validation=('sizes', 1, 3))
        evargs.assign([1, 2, 3], validation=('sizes', 1, 3))
        evargs.assign('XYZ', validation=('sizes', None, 3))
        evargs.assign('XYZ', validation=('sizes', 2, None))

        with pytest.raises(ValidateException):
            evargs.assign('abc', cast=str, validation=('sizes', 0, 2))

        with pytest.raises(ValidateException):
            evargs.assign([1, 2, 3], validation=('sizes', 0, 2))

    def test_enum(self):
        evargs = EvArgs()

        assert evargs.assign(2, cast=int, validation=('enum', Color)) == 2

        with pytest.raises(ValidateException):
            assert evargs.assign(9, cast=int, validation=('enum', Color)) == 2

    def test_validate_str(self):
        evargs = EvArgs()

        # alphabet
        assert evargs.assign('AbcD', cast=str, validation='alphabet') == 'AbcD'
        assert evargs.assign('AbcDef', cast=str, validation=[tuple(['alphabet']), ('sizes', 4, None)]) == 'AbcDef'
        assert evargs.assign('Abc123', cast=str, validation='alphanumeric') == 'Abc123'

        # ascii
        assert evargs.assign('"Abc123"', cast=str, validation='ascii') == '"Abc123"'
        assert evargs.assign('"Abc 123"', cast=str, validation='printable_ascii') == '"Abc 123"'
        assert evargs.assign('"Abc-123"', cast=str, validation='standard_ascii') == '"Abc-123"'

        # char_numeric
        assert evargs.assign('1234', cast=str, validation='char_numeric') == '1234'

        with pytest.raises(ValidateException):
            assert evargs.assign('a1234', cast=str, validation='char_numeric') == 'a1234'

    def test_validate_regex(self):
        evargs = EvArgs()

        # regex
        assert evargs.assign('123', cast=int, validation=['regex', r'^\d{3}$']) == 123
        assert evargs.assign('AbC12345XyZ', cast=str, validation=['regex', r'^ABC\d{5,10}XYZ$', re.I]) == 'AbC12345XyZ'
        assert evargs.assign('ATGCGTACGTAGCTAGCTAGCTAGCATCGTAGCTAGCTAGC', cast=str, validation=['regex', r'^[ATGC]+$']) == 'ATGCGTACGTAGCTAGCTAGCTAGCATCGTAGCTAGCTAGC'

        # Exception
        with pytest.raises(ValidateException):
            evargs.assign('123XYZ', cast=str, validation=['regex', r'^XYZ.+$'])

    def test_validate_range(self):
        evargs = EvArgs()

        assert evargs.assign('123', cast=int, validation=('range', None, 200)) == 123
        assert evargs.assign('200', cast=int, validation=['range', 100, None]) == 200
        assert evargs.assign('199.9', cast=float, validation=[('unsigned',), ('range', 1, 200)]) == 199.9

        with pytest.raises(ValidateException):
            assert evargs.assign('201', cast=int, validation=('range', None, 200)) == 201

    def test_validate_unsigned(self):
        evargs = EvArgs()

        assert evargs.assign('1', cast=int, validation='unsigned') == 1

        with pytest.raises(ValidateException):
            assert evargs.assign('-1', cast=int, validation='unsigned') == -1

    def test_validate_positive(self):
        evargs = EvArgs()

        assert evargs.assign('1', cast=int, validation='positive') == 1

        with pytest.raises(ValidateException):
            assert evargs.assign('0', cast=int, validation='positive') == 0

    def test_validate_negative(self):
        evargs = EvArgs()

        assert evargs.assign('-1', cast=int, validation='negative') == -1

        with pytest.raises(ValidateException):
            assert evargs.assign('0', cast=int, validation='negative') == 0

    def test_validate_even_odd(self):
        evargs = EvArgs()

        assert evargs.assign('2', cast=int, validation='even') == 2
        assert evargs.assign('1', cast=int, validation='odd') == 1

    def test_validate_list(self):
        evargs = EvArgs()

        assert evargs.assign(['1', '2', '3'], cast='int', list=True, validation='unsigned') == [1, 2, 3]

        with pytest.raises(ValidateException):
            evargs.assign(['-1', '2', '3'], cast='int', list=True, validation='unsigned')

        assert evargs.assign(['1', '2', '3'], cast='int', list=True, post_apply=('size', 3))

        with pytest.raises(ValidateException):
            assert evargs.assign(['1', '2'], cast='int', list=True, post_apply=('size', 3))

        assert evargs.assign(['1', '2'], cast='int', list=True, post_apply='exist')

        with pytest.raises(ValidateException):
            assert evargs.assign([], cast='int', list=True, post_apply=('exist'))

    def test_multiple_validation(self):
        evargs = EvArgs()

        result = evargs.assign_values({
            'a': 'ABCD',
            'b': '3',
            'c': 'acdefg'
        }, {
            'a': {'cast': str, 'validation': [('size', 4), ('alphabet',)]},
            'b': {'cast': int, 'validation': [('range', 1, 50), ('odd',)]},
            'c': {'cast': str, 'validation': [('sizes', 5, 10), tuple(['regex', '^[a-z]+$'])]}
        })

        assert result['a'] == 'ABCD'
        assert result['b'] == 3
        assert result['c'] == 'acdefg'

        # Exception
        with pytest.raises(ValidateException):
            evargs.assign('ABC', cast=str, validation=[('size', 4), ('alphabet',)])

    def test_validate_method(self):
        evargs = EvArgs()

        # method
        assert evargs.assign('1', cast=int, validation=lambda v: True if v >= 0 else False) == 1

        # Exception
        with pytest.raises(ValidateException):
            evargs.assign('-8', cast=int, validation=lambda v: True if v >= 0 else False)


class MyValidator(Validator):
    def validate_length_limit(self, v):
        if not (len(v) == 8 or len(v) == 24):
            self.raise_error('Length is not 128,256.', v)


class TestExtendValidator():
    def test1(self):
        validator = MyValidator()
        evargs = EvArgs()
        evargs.set_validator(validator)

        # length_limit = MyValidator::validate_length_limit
        assert evargs.assign('12345678', cast=str, validation='length_limit') == '12345678'
