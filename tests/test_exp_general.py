from evargs import ExpEvArgs, EvArgsException, ValidateException
from evargs.modules import Operator
import pytest
import re


# Document: https://github.com/deer-hunt/evargs/
class TestExpGeneral:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_operator(self):
        evargs = ExpEvArgs()

        evargs.initialize({
            'a1': {'cast': int},
            'a2': {'cast': int},
            'b1': {'cast': int},
            'b2': {'cast': int},
            'c': {'cast': int},
            'd': {'cast': int},
        })

        evargs.parse('a1>1;a2 >= 1;b1<1;b2<=3;c=3;d != 3;')

        param = evargs.get_param('a1')
        assert param.operator == Operator.GREATER

        param = evargs.get_param('a2')
        assert param.operator == (Operator.GREATER | Operator.EQUAL)

        param = evargs.get_param('b1')
        assert param.operator == Operator.LESS

        param = evargs.get_param('c')
        assert param.operator == Operator.EQUAL

        param = evargs.get_param('d')
        assert param.operator == Operator.NOT_EQUAL

    def test_operator_error(self):
        evargs = ExpEvArgs()

        evargs.initialize({
            'a': {'cast': int}
        })

        evargs.parse('a>=1;')

        with pytest.raises(EvArgsException):
            evargs.parse('a=>1;')

        evargs.initialize({
            'a': {'cast': int}
        })

    def test_set_rule(self):
        evargs = ExpEvArgs()

        evargs.initialize({
            'a': {'cast': int},
            'b': {'cast': int, 'validation': ('range', 1, 3)}
        })

        evargs.set_rule('c', {'cast': int})

        evargs.parse('c=3')

        assert evargs.get('c') == 3

    def test_methods(self):
        evargs = ExpEvArgs()

        evargs.initialize({
            'a': {'cast': int, 'list': True},
            'b': {'cast': int},
            'c': {'cast': int},
        })

        evargs.put_values(
            {
                'a': [1, 2, 3],
                'b': 8
            }
        )

        assert evargs.get('a') == [1, 2, 3]
        assert evargs.has_param('d') is False

        param = evargs.get_param('a')

        assert param.value == [1, 2, 3]
        assert param.operator == Operator.EQUAL

        assert len(evargs.get_params()) == 2
        assert evargs.get_size() == 2
        assert evargs.get_rule('a') is not None
