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

    def test_cast_expression(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'cast': lambda v: ExpressionParser.parse(v)},
            'b': {'cast': lambda v: ExpressionParser.parse(v)},
            'c': {'cast': lambda v: ExpressionParser.parse(v)},
            'd': {'cast': lambda v: ExpressionParser.parse(v)},
        })

        assert evargs.assign('1 + 2', lambda v: ExpressionParser.parse(v)) == 3
        assert evargs.assign('2 * 4 ', lambda v: ExpressionParser.parse(v)) == 8
        assert evargs.assign('1 * 4 + (10 - 4)/2 ', lambda v: ExpressionParser.parse(v)) == 7
        assert evargs.assign('( (1 + 4) * (6 - 4))**2 ', lambda v: ExpressionParser.parse(v)) == 100
