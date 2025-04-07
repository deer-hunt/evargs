from evargs import EvArgs, EvArgsException, EvValidateException
import pytest
import re


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
            'a': {'type': int, 'validate': 'unsigned'},
        }).parse('a=1;')

        assert evargs.get('a') == 1

        # range
        evargs.initialize({
            'a': {'type': int, 'validate': ['range', None, 200]},
            'b': {'type': int, 'validate': ['range', 100, None]},
            'c': {'type': float, 'validate': ['range', 0, 200]},
        }).parse('a=123;b=200;c=199.9')

        assert evargs.get('a') == 123
        assert evargs.get('c') == 199.9

    def test_validate_size(self):
        evargs = EvArgs()

        # size
        evargs.initialize({
            'a': {'type': str, 'validate': ['size', 3]},
        }).parse('a=ABC;')

        # between
        evargs.initialize({
            'a': {'type': str, 'validate': ['between', 4, None]},
            'b': {'type': str, 'validate': ['between', None, 10]},
        }).parse('a=ABCD;b=ABCDEFGHI')

        assert evargs.get('a') == 'ABCD'
        assert evargs.get('b') == 'ABCDEFGHI'

    def test_validate_str(self):
        evargs = EvArgs()

        # alphabet
        evargs.initialize({
            'a': {'type': str, 'validate': 'alphabet'},
        }).parse('a=AbcD;')

        assert evargs.get('a') == 'AbcD'

        evargs.initialize({
            'a': {'type': str, 'validate': 'alphanumeric'},
        }).parse('a=Abc123;')

        assert evargs.get('a') == 'Abc123'

        # printable_ascii
        evargs.initialize({
            'a': {'type': str, 'validate': 'printable_ascii'},
        }).parse('a="Abc 123";')

        assert evargs.get('a') == 'Abc 123'

    def test_validate_regex(self):
        evargs = EvArgs()

        # regex
        evargs.initialize({
            'a': {'type': int, 'validate': ['regex', r'^\d{3}$']},
            'b': {'type': str, 'validate': ['regex', r'^ABC\d{5,10}XYZ$', re.I]},
        }).parse('a=123;b=AbC12345XyZ')

        assert evargs.get('a') == 123
        assert evargs.get('b') == 'AbC12345XyZ'

        evargs.initialize({
            'dna': {'type': str, 'validate': ['regex', r'^[ATGC]+$']},
        }).parse('dna=ATGCGTACGTAGCTAGCTAGCTAGCATCGTAGCTAGCTAGC')

        assert evargs.get('dna') == 'ATGCGTACGTAGCTAGCTAGCTAGCATCGTAGCTAGCTAGC'

        # Exception
        with pytest.raises(EvValidateException):
            evargs.initialize({
                'a': {'type': str, 'validate': ['regex', r'^XYZ.+$']},
            }).parse('a=123XYZ')

    def test_validate_method(self):
        evargs = EvArgs()

        # method
        evargs.initialize({
            'a': {'type': int, 'validate': lambda n, v: True if v >= 0 else False},
        }).parse('a=1;')

        assert evargs.get('a') == 1

        # Exception
        with pytest.raises(EvValidateException):
            evargs.initialize({
                'a': {'type': int, 'validate': lambda n, v: True if v >= 0 else False},
                'b': {'type': int, 'validate': lambda n, v: True if v >= 0 else False},
            }).parse('a=1;b = - 8;')
