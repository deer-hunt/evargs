from evargs import EvArgs, EvArgsException, EvValidateException
import pytest
import re


# Document: https://github.com/deer-hunt/evargs/
class TestRulePrePost:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_pre_apply(self):
        evargs = EvArgs()

        def pre_apply(v):
            return v + '1'

        evargs.initialize({
            'a': {'type': int, 'pre_apply': pre_apply},
            'b': {'type': int, 'pre_apply': pre_apply, 'default': 5},
            'c': {'type': int, 'pre_apply': pre_apply, 'list': True},
            'd': {'type': int, 'pre_apply': pre_apply, 'multiple': True},
            'e': {'type': int, 'pre_apply': lambda v: v.strip('<> ')},
        })

        assigns = 'a=1;b=;c=1,2,3;d=1;d=2;e="<33>"'

        evargs.parse(assigns)

        assert evargs.get('a') == 11
        assert evargs.get('b') == 5
        assert evargs.get('c') == [11, 21, 31]
        assert evargs.get('d', 0) == 11
        assert evargs.get('e') == 33

    def test_post_apply(self):
        evargs = EvArgs()

        def post_apply(v):
            return v + 1

        evargs.initialize({
            'a': {'type': int, 'post_apply': post_apply},
            'b': {'type': int, 'post_apply': post_apply, 'default': 5},
            'c': {'type': int, 'post_apply': post_apply, 'list': True},
            'd': {'type': int, 'post_apply': post_apply, 'multiple': True},
            'e': {'type': str, 'post_apply': str.upper},
        })

        assigns = 'a=1;b=;c=1,2,3;d=1;d=2;e=Abc'

        evargs.parse(assigns)

        assert evargs.get('a') == 2
        assert evargs.get('b') == 5
        assert evargs.get('c') == [2, 3, 4]
        assert evargs.get('d', 0) == 2
        assert evargs.get('e') == 'ABC'

    def test_pre_apply_param(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': int, 'pre_apply_param': lambda values: values + ['4'], 'list': True},
            'b': {'type': int, 'pre_apply_param': lambda values: values + ['4']},
            'c': {'type': int, 'pre_apply_param': lambda values: [''.join(values)]},
            'd': {'type': int, 'pre_apply_param': lambda values: [values[0] + '1'], 'multiple': True},
        })

        evargs.parse('a=1,2,3;b=;c=1,2,3;d=1;d=2')

        assert evargs.get('a') == [1, 2, 3, 4]
        assert evargs.get('b') == 4
        assert evargs.get('c') == 123
        assert evargs.get('d', 0) == 11
        assert evargs.get('d', 1) == 21

    def test_post_apply_param(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': int, 'post_apply_param': lambda values: values[:-1], 'list': True},
            'b': {'type': int, 'post_apply_param': lambda values: 5},
            'c': {'type': int, 'post_apply_param': lambda values: sum(values)},
            'd': {'type': int, 'post_apply_param': lambda values: values[0] * 2, 'multiple': True},
            'e': {'type': int, 'post_apply_param': lambda values: [sum(values)], 'list': True},
        })

        assigns = 'a=1,2,3;b=;c=1,2,3;d=2;d=3;e=1,2,3'

        evargs.parse(assigns)

        assert evargs.get('a') == [1, 2]
        assert evargs.get('b') == 5
        assert evargs.get('c') == 6
        assert evargs.get('d', 0) == 4
        assert evargs.get('e') == [6]

    def test_dynamic_value(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': int},
            'b': {'type': int},
            'dynamic1': {'type': int, 'post_apply_param': lambda v: evargs.get('a') + evargs.get('b')},
            'dynamic2': {'type': int, 'post_apply_param': lambda v: v[0] + evargs.get('a') * evargs.get('b')},
        })

        assigns = 'a=2;b=3;dynamic2=10;'

        evargs.parse(assigns)

        assert evargs.get('dynamic1') == 5
        assert evargs.get('dynamic2') == 16
