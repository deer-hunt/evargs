from enum import Enum

import pytest

from evargs.type_cast import TypeCast


# Document: https://github.com/deer-hunt/evargs/
class TestTypeCast:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_int(self):
        assert TypeCast.to_int('1') == 1
        assert TypeCast.to_int(' 1 ') == 1
        assert TypeCast.to_int('', default=0) == 0
        assert TypeCast.to_int('', nullable=True) is None

        with pytest.raises(ValueError):
            assert TypeCast.to_int('') is None

        assert TypeCast.to_int(' aaa ', raise_error=0) is None

        assert TypeCast.to_int(' aaa ', 2) == 2

        with pytest.raises(ValueError):
            assert TypeCast.to_int(' aaa ')

        with pytest.raises(ValueError):
            assert TypeCast.to_int(' 1 a', default=2, raise_error=TypeCast.ERROR_ALL)

    def test_round_int(self):
        assert TypeCast.to_round_int('1') == 1
        assert TypeCast.to_round_int(' 1.1 ') == 1
        assert TypeCast.to_round_int('1.4') == 1
        assert TypeCast.to_round_int('1.5') == 2
        assert TypeCast.to_round_int('2.1') == 2
        assert TypeCast.to_round_int('2.5') == 3
        assert TypeCast.to_round_int('3.1') == 3

        assert TypeCast.to_round_int(' 0 ') == 0
        assert TypeCast.to_round_int(' 0.0 ') == 0
        assert TypeCast.to_round_int('0.1') == 0
        assert TypeCast.to_round_int('0.5') == 1

        assert TypeCast.to_round_int('-1') == -1
        assert TypeCast.to_round_int(' -1.1 ') == -1
        assert TypeCast.to_round_int('-1.4') == -1
        assert TypeCast.to_round_int('-1.5') == -2
        assert TypeCast.to_round_int('-2.1') == -2
        assert TypeCast.to_round_int('-2.5') == -3
        assert TypeCast.to_round_int('-3.1') == -3

        assert TypeCast.to_round_int('-0.1') == 0
        assert TypeCast.to_round_int('-0.5') == -1

        assert TypeCast.to_round_int('', default=0) == 0
        assert TypeCast.to_round_int('', nullable=True) is None

        with pytest.raises(ValueError):
            assert TypeCast.to_int('') is None

        with pytest.raises(ValueError):
            assert TypeCast.to_int(' aaa ')

        with pytest.raises(ValueError):
            assert TypeCast.to_int(' 1 a', default=2, raise_error=TypeCast.ERROR_ALL)

    def test_float(self):
        assert TypeCast.to_float('1.1') == 1.1
        assert TypeCast.to_float(' 1.1 ') == 1.1
        assert TypeCast.to_float(' -1.1 ') == -1.1
        assert TypeCast.to_float(' aaa ', raise_error=0) is None

        assert TypeCast.to_float(' aaa ', 2.1) == 2.1
        assert TypeCast.to_float('', nullable=True) is None

        with pytest.raises(ValueError):
            assert TypeCast.to_float(' aaa ') is None

        with pytest.raises(ValueError):
            assert TypeCast.to_float(' 1.0 a', default=2, raise_error=TypeCast.ERROR_ALL)

    def test_str(self):
        assert TypeCast.to_str('a') == 'a'
        assert TypeCast.to_str('') == ''
        assert TypeCast.to_str(None, 'A') == 'A'
        assert TypeCast.to_str('', 'A') == 'A'
        assert TypeCast.to_str('') == ''

        with pytest.raises(ValueError):
            assert TypeCast.to_str(None)

    def test_bool(self):
        assert TypeCast.to_bool('1') is True
        assert TypeCast.to_bool(1) is True
        assert TypeCast.to_bool(2) is True
        assert TypeCast.to_bool(2.5) is True
        assert TypeCast.to_bool(0) is False
        assert TypeCast.to_bool(-1) is False
        assert TypeCast.to_bool('0') is False
        assert TypeCast.to_bool('True') is True
        assert TypeCast.to_bool('true') is True
        assert TypeCast.to_bool('', False) is False
        assert TypeCast.to_bool(None, none_cast=True) is False
        assert TypeCast.to_bool('A', raise_error=0) is None
        assert TypeCast.to_bool('A', default=False) is False

        with pytest.raises(ValueError):
            assert TypeCast.to_bool('A', default=False, raise_error=TypeCast.ERROR_ALL)

        with pytest.raises(ValueError):
            assert TypeCast.to_bool('A') is False

        with pytest.raises(ValueError):
            assert TypeCast.to_bool(None, none_cast=False) is None

    def test_bool_loose(self):
        assert TypeCast.bool_loose('1') is True
        assert TypeCast.bool_loose(' 1 ') is True
        assert TypeCast.bool_loose(' A ') is False
        assert TypeCast.bool_loose('True') is True
        assert TypeCast.bool_loose(1) is True
        assert TypeCast.bool_loose(None) is False
        assert TypeCast.bool_loose(1.5) is True

    def test_bool_strict(self):
        assert TypeCast.bool_strict('1') == 1
        assert TypeCast.bool_strict(' 1 ') == 1
        assert TypeCast.bool_strict('A', raise_error=0) is None
        assert TypeCast.bool_strict('True', raise_error=0) is None
        assert TypeCast.bool_strict(1) is True
        assert TypeCast.bool_strict(None, raise_error=0) is None
        assert TypeCast.bool_strict(1.5, raise_error=0) is None

    def test_enum(self):
        assert TypeCast.to_enum(Color, 1) == Color.RED
        assert TypeCast.to_enum(Color, 3.5) == Color.PURPLE
        assert TypeCast.to_enum(Color, 'Sky blue') == Color.SKY_BLUE

        assert TypeCast.to_enum(Color, 'RED', is_name=True) == Color.RED
        assert TypeCast.to_enum(Color, 'SKY_BLUE', is_name=True) == Color.SKY_BLUE

        with pytest.raises(ValueError):
            assert TypeCast.to_enum(Color, 1, is_name=True, is_value=False) is None

        assert TypeCast.to_enum(Color, 'RED', is_name=True) == Color.RED
        assert TypeCast.to_enum(Color, 'RED', is_value=True, raise_error=0) is None

        assert TypeCast.to_enum(Color, 'GREEN', is_value=True) == Color.APPLE_GREEN
        assert TypeCast.to_enum(Color, 'GREEN', is_value=False, is_name=True) == Color.GREEN

    def test_enum_loose(self):
        assert TypeCast.to_enum_loose(Color, 1) == Color.RED
        assert TypeCast.to_enum_loose(Color, '1') == Color.RED
        assert TypeCast.to_enum_loose(Color, ' 1 ') == Color.RED

        assert TypeCast.to_enum_loose(Color, '3.5') == Color.PURPLE

        assert TypeCast.to_enum_loose(Color, '1', is_name=True, is_value=False, raise_error=0) is None
        assert TypeCast.to_enum_loose(Color, 'BLUE', is_name=True, is_value=False) is Color.BLUE
        assert TypeCast.to_enum_loose(Color, '100', default=Color.WHITE) == Color.WHITE

        with pytest.raises(ValueError):
            assert TypeCast.to_enum_loose(Color, '1', is_name=True, is_value=False) is None

    def test_enum_default(self):
        assert TypeCast.to_enum(Color, 10, default=Color.WHITE) == Color.WHITE
        assert TypeCast.to_enum(Color, 'AAA', default=Color.WHITE) == Color.WHITE

        assert TypeCast.to_enum(Color, 1, default=Color.WHITE) == Color.RED
        assert TypeCast.to_enum(Color, 1, is_value=False, default=Color.WHITE) == Color.WHITE
        assert TypeCast.to_enum(Color, '1', default=Color.WHITE) == Color.WHITE

    def test_noop(self):
        assert TypeCast.noop(123) == 123
        assert TypeCast.noop('123') == '123'
        assert TypeCast.noop(None, 123) == 123
        assert TypeCast.noop(None, nullable=True) is None
        assert TypeCast.noop(None, raise_error=0) is None

        with pytest.raises(ValueError):
            assert TypeCast.noop(None) is None


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

    PURPLE = 3.5
    WHITE = 100

    SKY_BLUE = 'Sky blue'

    APPLE_GREEN = 'GREEN'
