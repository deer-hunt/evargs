from evargs import EvArgs, EvArgsException, ValidateException
import pytest
import re


# Document: https://github.com/deer-hunt/evargs/
class TestRulePrePost:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_pre_cast(self):
        evargs = EvArgs()

        def pre_cast(v):
            return v + '1'

        assert evargs.assign('1', cast=int, pre_cast=pre_cast) == 11
        assert evargs.assign('', cast=int, pre_cast=pre_cast, default=5) == 1
        assert evargs.assign(['1', '2', '3'], cast=int, pre_cast=pre_cast, list=True) == [11, 21, 31]
        assert evargs.assign('<33>', cast=int, pre_cast=lambda v: v.strip('<> ')) == 33

    def test_post_cast(self):
        evargs = EvArgs()

        def post_cast(v):
            return v + 1

        assert evargs.assign('1', cast=int, post_cast=post_cast) == 2
        assert evargs.assign('', cast=int, post_cast=post_cast, default=5, raise_error=False) == 6
        assert evargs.assign(['1', '2', '3'], cast=int, post_cast=post_cast, list=True) == [2, 3, 4]
        assert evargs.assign('Abc', cast=str, post_cast=str.upper) == 'ABC'

    def test_pre_apply(self):
        evargs = EvArgs()

        assert evargs.assign(['1', '2', '3'], cast=int, pre_apply=lambda values: values + ['4'], list=True) == [1, 2, 3, 4]
        assert evargs.assign('', cast=int, pre_apply=lambda v: 4) == 4
        assert evargs.assign(['1', '2', '3'], cast=int, pre_apply=lambda values: ''.join(values)) == 123

    def test_post_apply(self):
        evargs = EvArgs()

        assert evargs.assign(['1', '2', '3'], cast=int, post_apply=lambda values: values[:-1], list=True) == [1, 2]

        assert evargs.assign('', cast=int, post_apply=lambda v: 5, raise_error=False) == 5

        assert evargs.assign(['1', '2', '3'], cast=int, post_apply=lambda values: sum(values), list=True) == 6
        assert evargs.assign(['1', '2', '3'], cast=int, post_apply=lambda values: [sum(values)], list=True) == [6]

        assert evargs.assign(['4', '5', '6'], cast=int, post_apply=('size', 3), list=True) == [4, 5, 6]

        assert evargs.assign('12345', validation=('size', 5)) == '12345'

        assert evargs.assign([5, 6, 7], post_apply=('size', 3), list=True) == [5, 6, 7]

    def test_post_apply_complex(self):
        evargs = EvArgs()

        assert evargs.assign(['1', '2', '3'], cast=int, post_apply=[lambda values: values[:-1], lambda values: sum(values)], list=True) == 3

        assert evargs.assign(['1', '2', '3'], cast=int, post_apply=[lambda values: sum(values), ('range', 1, 10)], list=True) == 6

        assert evargs.assign('abcdefghi', cast=str, post_apply=[lambda v: v[:6], ('size', 6)]) == 'abcdef'

    def test_dynamic_value(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'cast': int},
            'b': {'cast': int},
            'dynamic1': {'cast': int, 'post_apply': lambda v: evargs.get('a') + evargs.get('b')},
            'dynamic2': {'cast': int, 'post_apply': lambda v: v + evargs.get('a') * evargs.get('b')},
        })

        evargs.put_values({
            'a': 2,
            'b': '3',
            'dynamic2': 10
        })

        assert evargs.get('dynamic1') == 5
        assert evargs.get('dynamic2') == 16
