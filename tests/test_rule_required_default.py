from evargs import EvArgs, EvArgsException, ValidateException
import pytest
import re


# Document: https://github.com/deer-hunt/evargs/
class TestRuleRequiredDefault:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_required(self):
        evargs = EvArgs()

        # Testing required parameters with assign_values
        result = evargs.assign_values({
            'a': '1',  # Provided value
            'b': '',  # Empty, but has default
            'c': 'A',  # Provided value
            'd': ''  # Empty, but has default
        }, {
            'a': {'cast': int, 'required': True},
            'b': {'cast': int, 'required': True, 'default': 1},
            'c': {'cast': str, 'required': True},
            'd': {'cast': str, 'required': True, 'default': 'A'}
        })

        assert result['a'] == 1
        assert result['b'] == 1
        assert result['c'] == 'A'
        assert result['d'] == 'A'

        assert evargs.assign(0, cast=int, required=True) == 0

        # Exception when required parameter has empty value and no default
        with pytest.raises(ValidateException):
            evargs.assign(None, cast=int, required=True)

        with pytest.raises(ValidateException):
            evargs.assign('', cast=int, required=True)

        with pytest.raises(ValidateException):
            evargs.assign(' a ', cast=int, required=True, raise_error=0)

        with pytest.raises(ValidateException):
            evargs.assign('', cast=str, required=True)

        # Exception when required parameter is not provided
        with pytest.raises(ValidateException):
            evargs.assign_values({
                'a': ''  # Parameter 'c' is missing but required
            }, {
                'a': {'cast': int},
                'c': {'cast': str, 'required': True}
            })

        # Default value used when parameter is empty
        assert evargs.assign('', cast=int, required=True, default=3) == 3

    def test_default(self):
        evargs = EvArgs()

        assert evargs.assign('', cast=int, default=1) == 1
        assert evargs.assign('A', cast=int, default=2, raise_error=False) == 2
        assert evargs.assign('', cast=int, default=1, pre_apply=lambda v: [1, '', ''], list=True) == [1, 1, 1]

        assert evargs.assign('', cast=str, default='1') == '1'
        assert evargs.assign('', cast=str, default='2') == '2'
        assert evargs.assign('', cast=str, default='A', list=True) == []
        assert evargs.assign('', cast=str, default='A', pre_apply=lambda v: [1, '', ''], list=True) == ['1', 'A', 'A']

    def test_required_default(self):
        evargs = EvArgs()

        assert evargs.assign('1', cast=int, required=True) == 1
        assert evargs.assign('', cast=int, required=True, default=1) == 1
        assert evargs.assign('A', cast=str, required=True) == 'A'
        assert evargs.assign('', cast=str, required=True, default='A') == 'A'
