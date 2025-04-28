from enum import Enum

import pytest

from evargs import EvArgs, ValidateException, EvArgsException
from evargs.type_cast import TypeCast


# Document: https://github.com/deer-hunt/evargs/
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
    EMERALD_GREEN = 2.5


class TestRuleCastEnum:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_cast_enum(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'cast': Color},
            'b': {'cast': Color, 'required': True},
            'c': {'cast': Color, 'raise_error': False},
            'd': {'cast': Color, 'default': Color.BLUE},
            'e': {'cast': Color, 'nullable': True},
        })

        evargs.put('a', 'RED')
        evargs.put('b', 3)
        evargs.put('c', 'X')
        evargs.put('d', '')
        evargs.put('e', '')

        assert evargs.get('a') == Color.RED
        assert evargs.get('b') == Color.BLUE
        assert evargs.get('c') is None
        assert evargs.get('d') == Color.BLUE
        assert evargs.get('e') is None

        with pytest.raises(ValidateException):
            evargs.put('b', None)

    def test_cast_enum_list(self):
        evargs = EvArgs()

        assert evargs.assign(['RED', 2, 3, 2.5], cast=Color, list=True) == [Color.RED, Color.GREEN, Color.BLUE, Color.EMERALD_GREEN]
        assert evargs.assign(['RED', 2, -9], cast=Color, list=True, default=Color.RED) == [Color.RED, Color.GREEN, Color.RED]
        assert evargs.assign(['RED', 1, None], cast=('enum', Color), list=True, default=Color.RED) == [Color.RED, Color.RED, Color.RED]

    def test_other(self):
        evargs = EvArgs()

        assert evargs.assign([1.0, 1.5], pre_cast=lambda v: sum(v), cast=Color) == Color.EMERALD_GREEN
        assert evargs.assign(['1', 2], cast=int, list=True, post_apply=[lambda v: sum(v), ('enum', Color)]) == 3
        assert evargs.assign(['1', 2], cast=int, list=True, post_apply=[lambda v: sum(v), lambda v: TypeCast.to_enum(Color, v)]) == Color.BLUE

    def test_cast_tuple_enum(self):
        evargs = EvArgs()

        # name or value
        evargs.initialize({
            'a': {'cast': ('enum', Color)},
            'b': {'cast': ('enum', Color), 'default': Color.BLUE},
            'c': {'cast': ('enum', Color)},
        })

        assert evargs.assign('RED', cast=('enum', Color)) == Color.RED
        assert evargs.assign('0', cast=('enum', Color), default=Color.BLUE) == Color.BLUE
        assert evargs.assign('EMERALD_GREEN', cast=('enum', Color)) == Color.EMERALD_GREEN

    def test_cast_tuple_enum_value(self):
        evargs = EvArgs()

        # value
        evargs.initialize({
            'a': {'cast': ('enum_value', Color)},
            'b': {'cast': ('enum_value', Color), 'default': Color.BLUE},
            'c': {'cast': ('enum_value', Color), 'multiple': True, 'raise_error': False},
        })

        evargs.put('a', 1)
        evargs.put('b', None)
        evargs.put('c', 'BLUE')
        evargs.put('c', 2.5)

        assert evargs.get('a') == Color.RED
        assert evargs.get('b') == Color.BLUE
        assert evargs.get('c', 0) is None
        assert evargs.get('c', 1) == Color.EMERALD_GREEN

        assert evargs.assign('1', cast=('enum_value', Color)) == Color.RED
        assert evargs.assign('BLUE', cast=('enum_value', Color)) is None
        assert evargs.assign(2.5, cast=('enum_value', Color)) is Color.EMERALD_GREEN

    def test_cast_tuple_enum_name(self):
        evargs = EvArgs()

        # name
        assert evargs.assign('RED', cast=('enum_name', Color)) == Color.RED
        assert evargs.assign('', cast=('enum_name', Color), default=Color.BLUE) == Color.BLUE
        assert evargs.assign('EMERALD_GREEN', cast=('enum_name', Color)) is Color.EMERALD_GREEN

    def test_cast_tuple_error(self):
        evargs = EvArgs()

        # value
        evargs.initialize({
            'a': {'cast': ('unknown', None)},
        })

        with pytest.raises(ValidateException):
            evargs.put('a', '1')
