import pytest

from evargs import EvArgs
from evargs.helper import ExpressionParser


# Document: https://github.com/deer-hunt/evargs/
class TestExpressionParser:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_expression(self):
        assert ExpressionParser.parse('-6') == -6
        assert ExpressionParser.parse('1+2+3') == 6
        assert ExpressionParser.parse('((4 + 2) * 3)') == 18


class TestHelper:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_type_expression(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': lambda v: ExpressionParser.parse(v)},
            'b': {'type': lambda v: ExpressionParser.parse(v)},
            'c': {'type': lambda v: ExpressionParser.parse(v)},
            'd': {'type': lambda v: ExpressionParser.parse(v)},
        })

        assigns = 'a= 1 + 2 ;b= 2*4;c="1 * 4 + (10 - 4)/2";d=( (1 + 4) * (6 - 4))**2'

        evargs.parse(assigns)

        assert evargs.get('a') == 3
        assert evargs.get('b') == 8
        assert evargs.get('c') == 7
        assert evargs.get('d') == 100
