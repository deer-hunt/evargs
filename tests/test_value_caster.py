from enum import Enum

import pytest

from evargs.value_caster import ValueCaster


# Document: https://github.com/deer-hunt/evargs/
class TestValueCaster:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_int(self):
        assert ValueCaster.to_int('1') == 1
        assert ValueCaster.to_int(' 1 ') == 1

        assert ValueCaster.to_int(' aaa ', ignore_error=True) is None

        with pytest.raises(Exception):
            assert ValueCaster.to_float(' aaa ') is None

    def test_float(self):
        assert ValueCaster.to_float('1.1') == 1.1
        assert ValueCaster.to_float(' 1.1 ') == 1.1
        assert ValueCaster.to_float(' -1.1 ') == -1.1
        assert ValueCaster.to_float(' aaa ', ignore_error=True) is None

        with pytest.raises(Exception):
            assert ValueCaster.to_float(' aaa ') is None

    def test_bool(self):
        assert ValueCaster.to_bool('1') == 1
        assert ValueCaster.to_bool('A') is False

    def test_bool_strict(self):
        assert ValueCaster.to_bool('1', True) == 1
        assert ValueCaster.to_bool('A', True) is None

    def test_enum(self):
        assert ValueCaster.to_enum(Color, 1) == Color.RED
        assert ValueCaster.to_enum(Color, 3.5) == Color.PURPLE
        assert ValueCaster.to_enum(Color, 'Sky blue') == Color.SKY_BLUE

        assert ValueCaster.to_enum(Color, 'RED', is_name=True) == Color.RED
        assert ValueCaster.to_enum(Color, 'SKY_BLUE', is_name=True) == Color.SKY_BLUE

        assert ValueCaster.to_enum(Color, 1, is_name=True, is_value=False) is None

        assert ValueCaster.to_enum(Color, 'RED', is_name=True) == Color.RED
        assert ValueCaster.to_enum(Color, 'RED', is_value=True) is None

        assert ValueCaster.to_enum(Color, 'GREEN', is_value=True) == Color.APPLE_GREEN
        assert ValueCaster.to_enum(Color, 'GREEN', is_value=False, is_name=True) == Color.GREEN

    def test_enum_loose(self):
        assert ValueCaster.to_enum_loose(Color, 1) == Color.RED
        assert ValueCaster.to_enum_loose(Color, '1') == Color.RED
        assert ValueCaster.to_enum_loose(Color, ' 1 ') == Color.RED

        assert ValueCaster.to_enum_loose(Color, '3.5') == Color.PURPLE

        assert ValueCaster.to_enum_loose(Color, '1', is_name=True, is_value=False) is None
        assert ValueCaster.to_enum_loose(Color, 'BLUE', is_name=True, is_value=False) is Color.BLUE
        assert ValueCaster.to_enum_loose(Color, '100', illegal_value=Color.WHITE) == Color.WHITE

    def test_enum_illegal(self):
        assert ValueCaster.to_enum(Color, 10, illegal_value=Color.WHITE) == Color.WHITE
        assert ValueCaster.to_enum(Color, 'AAA', illegal_value=Color.WHITE) == Color.WHITE

        assert ValueCaster.to_enum(Color, 1, illegal_value=Color.WHITE) == Color.RED
        assert ValueCaster.to_enum(Color, 1, is_value=False, illegal_value=Color.WHITE) == Color.WHITE
        assert ValueCaster.to_enum(Color, '1', illegal_value=Color.WHITE) == Color.WHITE


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

    PURPLE = 3.5
    WHITE = 100

    SKY_BLUE = 'Sky blue'

    APPLE_GREEN = 'GREEN'
