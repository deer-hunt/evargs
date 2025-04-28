from evargs import EvArgs, ExpEvArgs, EvArgsException, ValidateException
import pytest
import re


# Document: https://github.com/deer-hunt/evargs/
class TestRuleMultiple:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_multiple(self):
        evargs = EvArgs()

        evargs.initialize({
            'multi1': {'cast': int, 'multiple': True},
            'multi2': {'cast': int, 'default': 9, 'multiple': True},
            'multi3': {'cast': int, 'multiple': True},
        })

        evargs.put('multi1', 1)
        evargs.put('multi1', 2)
        evargs.put('multi1', 3)

        assert evargs.get('multi1', 0) == 1
        assert evargs.get('multi1', 1) == 2
        assert evargs.get('multi1', 2) == 3
        assert evargs.get('multi1', -1) == [1, 2, 3]

        evargs.put('multi2', 1)
        evargs.put('multi2', 2)
        evargs.put('multi2', None)

        assert evargs.get('multi2', 0) == 1
        assert evargs.get('multi2', 1) == 2
        assert evargs.get('multi2', 2) == 9

    def test_multiple_evaluate(self):
        evargs = ExpEvArgs()

        evargs.initialize({
            'multi1': {'cast': int, 'multiple': True},
            'multi2': {'cast': int, 'multiple': True, 'multiple_or': True},
        })

        expression = 'multi1>=5;multi1<=10;' \
                     'multi2<5;multi2>10;'

        evargs.parse(expression)

        assert evargs.evaluate('multi1', 4) is False
        assert evargs.evaluate('multi1', 5) is True
        assert evargs.evaluate('multi1', 10) is True
        assert evargs.evaluate('multi1', 11) is False

        assert evargs.evaluate('multi2', 3) is True
        assert evargs.evaluate('multi2', 12) is True
