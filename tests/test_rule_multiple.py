from evargs import EvArgs, EvArgsException, EvValidateException
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
            'multi1': {'type': int, 'multiple': True},
            'multi2': {'type': int, 'default': 9, 'multiple': True, 'prevent_error': True},
            'multi3': {'type': int, 'multiple': True},
        })

        assigns = '' \
                  'multi1=1;multi1=2;multi1=3;' \
                  'multi2=1;multi2=0;multi2=;multi2=a;'

        evargs.parse(assigns)

        assert evargs.get('multi1', 0) == 1
        assert evargs.get('multi1', 1) == 2
        assert evargs.get('multi1', 2) == 3
        assert evargs.get('multi1', -1) == [1, 2, 3]

        assert evargs.get('multi2', 0) == 1
        assert evargs.get('multi2', 1) == 0
        assert evargs.get('multi2', 2) == 9

    def test_multiple_evaluate(self):
        evargs = EvArgs()

        evargs.initialize({
            'multi1': {'type': int, 'multiple': True},
            'multi2': {'type': int, 'multiple': True, 'multiple_or': True},
        })

        assigns = 'multi1>=5;multi1<=10;' \
                  'multi2<5;multi2>10;'

        evargs.parse(assigns)

        assert evargs.evaluate('multi1', 4) is False
        assert evargs.evaluate('multi1', 5) is True
        assert evargs.evaluate('multi1', 10) is True
        assert evargs.evaluate('multi1', 11) is False

        assert evargs.evaluate('multi2', 3) is True
        assert evargs.evaluate('multi2', 12) is True
