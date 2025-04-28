from evargs import EvArgs, EvArgsException, ValidateException
import pytest
import re


# Document: https://github.com/deer-hunt/evargs/
class TestAssign:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_assign(self):
        evargs = EvArgs()

        assert evargs.assign('1', cast=int) == 1
        assert evargs.assign('1', cast=str) == '1'
        assert evargs.assign('A', cast=int, default=1) == 1

        with pytest.raises(ValidateException):
            assert evargs.assign('A', cast=int, default=1, raise_error=2) == 1

        assert evargs.assign(' 1 ', cast=str, trim=True) == '1'
        assert evargs.assign(' a ', cast=str, trim=True) == 'a'
        assert evargs.assign([' 1 ', 2, ' 3', 4.0], cast=int, trim=True, list=True) == [1, 2, 3, 4]
        assert evargs.assign(['  ', None, ' 1 ', 'a'], cast=int, default=1, trim=True, list=True) == [1, 1, 1, 1]
        assert evargs.assign(' 1 ', cast=int, default=1, trim=True, multiple=True) == 1  # If name is None, multiple is unavailable in assign method.

        with pytest.raises(ValidateException):
            assert evargs.assign('-1', cast=int, validation=('range', 1, 10))

        with pytest.raises(ValidateException):
            assert evargs.assign('a123z', cast=str, validation=('regex', r'^[a-z]{1,5}\d{1,2}$'))

        with pytest.raises(ValidateException):
            assert evargs.assign('a', cast=int, required=True)

        with pytest.raises(ValidateException):
            assert evargs.assign('', cast=str, required=True)

        with pytest.raises(ValidateException):
            assert evargs.assign([' 1 ', 99], cast=int, choices=[1, 2, 3], list=True)

    def test_assign_args(self):
        evargs = EvArgs()

        evargs.assign(['1', '2'], int, True, 0, True, True, 'unsigned', None, None, None, None, 'exist', 1, True, False, None, 'a')

        rule = evargs.get_rule('a')

        assert rule['default'] == 0
        assert rule['validation'] == 'unsigned'
        assert rule['post_apply'] == 'exist'
        assert rule['raise_error'] == 1

        assert evargs.get('a') == [1, 2]

    def test_assign_values(self):
        evargs = EvArgs()

        assert evargs.assign_values({
            'a': '1', 'b': '2'
        }, {
            'a': {'cast': int}, 'b': {'cast': int}
        }) == {'a': 1, 'b': 2}

        assert evargs.assign_values({
            'b': 'xyz'
        }, {
            'a': {'cast': str, 'default': 'ABC'}, 'b': {'cast': str}
        }) == {'a': 'ABC', 'b': 'xyz'}

        assert evargs.assign_values({
            'a': ['1.1', '2.2', '3.3']
        }, {
            'a': {'cast': float, 'list': True}
        }) == {'a': [1.1, 2.2, 3.3]}

        assert evargs.assign_values({
            'a': ' XYZ '
        }, {
            'a': {'cast': str, 'trim': True, 'validation': ('size', 3)}}
        ) == {'a': 'XYZ'}

    def test_assign_store(self):
        evargs = EvArgs()

        evargs.assign('1', cast=int, name='a')
        assert evargs.get('a') == 1

        evargs.assign('A', cast=int, default=2, name='a')
        assert evargs.get('a') == 2

        evargs.assign(' 1 ', cast=str, trim=True, name='b')
        assert evargs.get('b') == '1'

        evargs.assign([' 1 ', 2, ' 3', 4.0], cast=int, trim=True, list=True, name='c')

        assert evargs.get('c') == [1, 2, 3, 4]

        assert evargs.assign('1', cast=int, multiple=True, name='d') == 1
        assert evargs.assign('2', cast=int, multiple=True, name='d') == 2

        assert evargs.get('d', 1) == 2
        assert evargs.get('d') == [1, 2]
        params = evargs.get_param('d')

        assert evargs.assign('5', cast=int, multiple=True, name='d') == 5
        assert params.get_size() == 3

        assert evargs.get('c') == [1, 2, 3, 4]

        evargs.assign_values({
            'a': ['1.1', '2.2', '3.3'],
            'b': '1.1'
        }, {
            'a': {'cast': float, 'list': True},
            'b': {'cast': float}
        }, store=True)

        assert evargs.get('a') == [1.1, 2.2, 3.3]
        assert evargs.get('b') == 1.1

    def test_trim(self):
        evargs = EvArgs()

        assert evargs.assign(' 1 ', cast=int, trim=True) == 1
        assert evargs.assign(' 1.1 ', cast=int, trim=True) == 1
        assert evargs.assign(' 1.1 ', cast=float, trim='  ') == 1.1
        assert evargs.assign(' . 1.1 .', cast=float, trim=' .') == 1.1
        assert evargs.assign('     ', cast=str, trim=True) == ''
        assert evargs.assign('   123 .;  ', cast=str, trim=' .;') == '123'
        assert evargs.assign(' a ', cast=str, trim=True) == 'a'

    def test_nullable(self):
        evargs = EvArgs()

        assert evargs.assign('', cast=int, nullable=True) is None
        assert evargs.assign(None, cast=int, nullable=True) is None
        assert evargs.assign(' A ', trim=True, cast=int, nullable=True, raise_error=0) is None
        assert evargs.assign('', cast=str, nullable=True) == ''
        assert evargs.assign('    ', cast=str, trim=True, nullable=True) == ''
        assert evargs.assign(None, cast=str, nullable=True) is None
        assert evargs.assign('1.1-', cast=float, nullable=True, raise_error=0) is None
