from evargs import EvArgs, EvArgsException, ValidateException
from enum import Enum
import pytest
import re


# Document: https://github.com/deer-hunt/evargs/
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
    EMERALD_GREEN = 2.5


class TestRuleChoices:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_choices(self):
        evargs = EvArgs()

        values = evargs.assign_values({
            'a': '3',
            'b': 'A',
            'c': ['1', '2'],
        }, {
            'a': {'cast': int, 'choices': [1, 2, 3]},
            'b': {'cast': str, 'choices': ('A', 'B', 'C')},
            'c': {'cast': int, 'choices': [1, 2, 3], 'list': True}
        })

        assert values['a'] == 3
        assert values['b'] == 'A'
        assert values['c'] == [1, 2]

        with pytest.raises(ValidateException):
            evargs.put('a', '5')

        with pytest.raises(ValidateException):
            evargs.put('b', 'Z')

    def test_choices_enum(self):
        evargs = EvArgs()

        assert evargs.assign('1', cast=int, choices=Color) == 1
        assert evargs.assign('2.5', cast=float, choices=Color) == 2.5

        with pytest.raises(ValidateException):
            evargs.assign('5', cast=int, choices=Color)

        assert evargs.assign([1, 1.5], cast=lambda v: sum(v), choices=Color) == 2.5
