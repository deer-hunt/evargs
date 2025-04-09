from evargs import EvArgs, EvArgsException, EvValidateException
import pytest
import re


# Document: https://github.com/deer-hunt/evargs/
class TestRuleRequireDefault:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_require(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': int, 'require': True},
            'b': {'type': int, 'require': True, 'default': 1},
            'c': {'type': str, 'require': True},
            'd': {'type': str, 'require': True, 'default': 'A'}
        })

        assigns = 'a=1;b=;c=A;d=;'

        evargs.parse(assigns)

        assert evargs.get('a') == 1
        assert evargs.get('b') == 1
        assert evargs.get('c') == 'A'
        assert evargs.get('d') == 'A'

        evargs.initialize({
            'a': {'type': int, 'require': True}
        })

        with pytest.raises(EvValidateException):
            evargs.parse('a=;')

        evargs.initialize({
            'c': {'type': str, 'require': True}
        })

        with pytest.raises(EvValidateException):
            evargs.parse('a=;')

        evargs.initialize({
            'b': {'type': int, 'require': True, 'default': 3},
        })

        evargs.parse('b=;')

        assert evargs.get('b') == 3

    def test_default(self):
        evargs = EvArgs()

        evargs.initialize({
            'int_a': {'type': int, 'default': 1},
            'int_b': {'type': int, 'default': 2},
            'int_c': {'type': int, 'default': 3, 'multiple': True},
            'int_d': {'type': int, 'default': [1, 2, 3], 'list': True},

            'str_a': {'type': str, 'default': '1'},
            'str_b': {'type': str, 'default': '2'},
            'str_c': {'type': str, 'default': '3', 'multiple': True},
            'str_d': {'type': str, 'default': ['1', '2', '3'], 'list': True}
        })

        assigns = '' \
                  ';int_b=3;int_d=' \
                  ';str_b=3;str_d='

        evargs.parse(assigns)

        assert evargs.get('int_a') == 1
        assert evargs.get('int_b') == 3
        assert evargs.get('int_c', 0) == 3
        assert evargs.get('int_d') == [1, 2, 3]

        assert evargs.get('str_a') == '1'
        assert evargs.get('str_b') == '3'
        assert evargs.get('str_c', 0) == '3'
        assert evargs.get('str_d') == ['1', '2', '3']

    def test_require_default(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': int, 'require': True},
            'b': {'type': int, 'require': True, 'default': 1},
            'c': {'type': str, 'require': True},
            'd': {'type': str, 'require': True, 'default': 'A'}
        })

        assigns = 'a=1;b=;c=A;d=;'

        evargs.parse(assigns)

        assert evargs.get('a') == 1
        assert evargs.get('b') == 1
        assert evargs.get('c') == 'A'
        assert evargs.get('d') == 'A'
