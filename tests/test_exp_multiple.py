from evargs import ExpEvArgs, EvArgsException, ValidateException
import pytest
import re


# Document: https://github.com/deer-hunt/evargs/
class TestExpMultiple:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_evaluate_multiple(self):
        evargs = ExpEvArgs()

        evargs.initialize({
            'a': {'cast': int, 'multiple': True},
            'b': {'cast': int, 'multiple': True, 'multiple_or': False},
            'c': {'cast': int, 'multiple': True, 'multiple_or': True},
        })

        expression = 'a=1; a=3;' \
                     'b=1; b=3;' \
                     'c=1; c=3;'

        evargs.parse(expression)

        assert evargs.evaluate('a', 1) is False
        assert evargs.evaluate('a', 3) is False
        assert evargs.evaluate('a', 4) is False

        assert evargs.evaluate('b', 1) is False
        assert evargs.evaluate('b', 3) is False

        assert evargs.evaluate('c', 1) is True
        assert evargs.evaluate('c', 3) is True
        assert evargs.evaluate('c', 9) is False

    def test_evaluate_multiple_range(self):
        evargs = ExpEvArgs()

        evargs.initialize({
            'a': {'cast': int, 'multiple': True},
            'b': {'cast': int, 'multiple': True, 'multiple_or': False},
            'c': {'cast': int, 'multiple': True, 'multiple_or': True},
        })

        expression = 'a>=1; a<10;' \
                     'b>=1; b<10;' \
                     'c<1; c>10;'

        evargs.parse(expression)

        assert evargs.evaluate('a', 3) is True
        assert evargs.evaluate('b', 9) is True
        assert evargs.evaluate('a', 10) is False

        assert evargs.evaluate('b', 3) is True
        assert evargs.evaluate('b', 9) is True
        assert evargs.evaluate('b', 10) is False

        assert evargs.evaluate('c', -10) is True
        assert evargs.evaluate('c', 20) is True
        assert evargs.evaluate('c', 3) is False
        assert evargs.evaluate('c', 10) is False

    def test_evaluation_apply(self):
        evargs = ExpEvArgs()

        evargs.initialize({
            'a': {'cast': int, 'evaluation_apply': lambda rule, param, v: v % param.value == 0},
            'b': {'cast': int, 'multiple': True, 'evaluation_apply': lambda rule, multi_param, v: v % multi_param.get(0).value == multi_param.get(1).value},
        }).parse('a=3;b=3;b=1;')

        assert evargs.evaluate('a', 3) is True
        assert evargs.evaluate('a', 6) is True
        assert evargs.evaluate('a', 8) is False

        assert evargs.evaluate('b', 7) is True
        assert evargs.evaluate('b', 13) is True
