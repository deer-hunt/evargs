from evargs.value_caster import ValueCaster
import pytest


# Document: https://github.com/deer-hunt/evargs/
class TestValueCaster:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_int(self):
        assert ValueCaster.to_int('1') == 1

    def test_bool(self):
        assert ValueCaster.to_bool('1') == 1
        assert ValueCaster.to_bool('A') is False

    def test_bool_strict(self):
        assert ValueCaster.to_bool('1', True) == 1
        assert ValueCaster.to_bool('A', True) is None

    def test_expression(self):
        assert ValueCaster.expression('-6') == -6
        assert ValueCaster.expression('1+2+3') == 6
        assert ValueCaster.expression('((4 + 2) * 3)') == 18
