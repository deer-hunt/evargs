from enum import Enum

import pytest

from evargs import EvArgs, EvValidateException


# Document: https://github.com/deer-hunt/evargs/
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
    EMERALD_GREEN = 2.5


class TestRuleTypeEnum:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_type_enum(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': Color},
            'b': {'type': Color, 'require': True},
            'c': {'type': Color},
            'd': {'type': Color, 'default': Color.BLUE},
            'e': {'type': Color, 'list': True},
        })

        evargs.parse('a=RED;b=3;c=X;d=;e=1,2,1,3')

        assert evargs.get('a') == Color.RED
        assert evargs.get('b') == Color.BLUE
        assert evargs.get('c') is None
        assert evargs.get('d') == Color.BLUE
        assert evargs.get('e') == [Color.RED, Color.GREEN, Color.RED, Color.BLUE]

        with pytest.raises(EvValidateException):
            evargs.parse('b=')

    def test_type_tuple_enum(self):
        evargs = EvArgs()

        # name or value
        evargs.initialize({
            'a': {'type': ('enum', Color)},
            'b': {'type': ('enum', Color), 'default': Color.BLUE},
            'c': {'type': ('enum', Color), 'multiple': True},
        })

        evargs.parse('a=RED;b=0;c=2;c=EMERALD_GREEN')

        assert evargs.get('a') == Color.RED
        assert evargs.get('b') == Color.BLUE
        assert evargs.get('c', 0) == Color.GREEN
        assert evargs.get('c', 1) == Color.EMERALD_GREEN

    def test_type_tuple_enum_value(self):
        evargs = EvArgs()

        # value
        evargs.initialize({
            'a': {'type': ('enum_value', Color)},
            'b': {'type': ('enum_value', Color), 'default': Color.BLUE},
            'c': {'type': ('enum_value', Color), 'multiple': True},
        })

        evargs.parse('a=1;b=;c=BLUE;c=2.5;')

        assert evargs.get('a') == Color.RED
        assert evargs.get('b') == Color.BLUE
        assert evargs.get('c', 0) is None
        assert evargs.get('c', 1) is Color.EMERALD_GREEN

    def test_type_tuple_enum_name(self):
        evargs = EvArgs()

        # value
        evargs.initialize({
            'a': {'type': ('enum_name', Color)},
            'b': {'type': ('enum_name', Color), 'default': Color.BLUE},
            'c': {'type': ('enum_name', Color), 'multiple': True},
        })

        evargs.parse('a=RED;b=;c=3;c=EMERALD_GREEN')

        assert evargs.get('a') == Color.RED
        assert evargs.get('b') == Color.BLUE
        assert evargs.get('c', 0) is None
        assert evargs.get('c', 1) is Color.EMERALD_GREEN
