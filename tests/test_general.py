from evargs import EvArgs, EvArgsException, EvValidateException
import pytest
import re


# Document: https://github.com/deer-hunt/evargs/
class TestGeneral:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_operator(self):
        evargs = EvArgs()

        evargs.initialize({
            'a1': {'type': int},
            'a2': {'type': int},
            'b1': {'type': int},
            'b2': {'type': int},
            'c': {'type': int},
            'd': {'type': int},
        })

        evargs.parse('a1>1;a2 >= 1;b1<1;b2<=3;c=3;d != 3;')

    def test_operator_error(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': int}
        })

        with pytest.raises(EvArgsException):
            evargs.parse('a=>1;')

        evargs.initialize({
            'a': {'type': int}
        })

    def test_set_rule(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': int},
            'b': {'type': int}
        })

        evargs.set_rule('c', {'type': int})

        evargs.parse('c=3')

        assert evargs.get('c') == 3

    def test_methods(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': int, 'list': True},
            'b': {'type': int},
            'c': {'type': int},
        })

        assigns = 'a= 1,2,3 ; b=8; c=80,443;'

        evargs.parse(assigns)

        assert evargs.get('a') == [1, 2, 3]
        assert evargs.has_param('d') is False
        assert evargs.get_param('a').name == 'a'
        assert len(evargs.get_params()) == 3
        assert evargs.count_params() == 3
        assert evargs.get_rule('a') is not None

    def test_errors(self):
        evargs = EvArgs()

        with pytest.raises(EvArgsException):
            evargs.initialize({
                'a': {'type': int, 'unknown': True}
            })

        evargs.initialize({
            'a': {'type': int}
        })

        with pytest.raises(EvArgsException):
            evargs.parse('a>= 1 a< ; ')

        with pytest.raises(EvValidateException):
            evargs.parse('e1=8')
