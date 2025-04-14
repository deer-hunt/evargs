from enum import Enum

import pytest

from evargs import EvArgs, EvValidateException


# Document: https://github.com/deer-hunt/evargs/
class TestRuleTypeEnum:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_type_enum(self):
        class Color(Enum):
            RED = 1
            GREEN = 2
            BLUE = 3
            EMERALD_GREEN = 2.5

        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': Color},
            'b': {'type': Color, 'require': True},
            'c': {'type': Color},
            'd': {'type': Color, 'default': Color.BLUE},
        })

        evargs.parse('a=RED;b=3;c=X;d=')

        assert evargs.get('a') == Color.RED
        assert evargs.get('b') == Color.BLUE
        assert evargs.get('c') is None
        assert evargs.get('d') == Color.BLUE

        with pytest.raises(EvValidateException):
            evargs.parse('b=')

    def test_type_tuple_enum(self):
        class Color(Enum):
            RED = 1
            GREEN = 2
            BLUE = 3
            EMERALD_GREEN = 2.5

        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': ('enum', Color)},  # name or value
            'b': {'type': ('enum_value', Color)},  # value
            'c': {'type': ('enum_name', Color)},  # name
        })

        evargs.parse('a=RED;b=3;c=3')

        assert evargs.get('a') == Color.RED
        assert evargs.get('b') == Color.BLUE
        assert evargs.get('c') is None
