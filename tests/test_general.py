from evargs import EvArgs, EvArgsException, ValidateException
import pytest
import re


# Document: https://github.com/deer-hunt/evargs/
class TestGeneral:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_default_rule(self):
        evargs = EvArgs()

        evargs.set_default_rule({
            'validation': ['range', 1, 100]
        })

        evargs.initialize({
            'a': {'cast': int, 'list': True},
            'b': {'cast': int},
            'c': {'cast': int},
        })

        assert evargs.get_rule('a')['nullable'] is True

    def test_get_rule(self):
        evargs = EvArgs()

        evargs.set_default_rule({
            'default': 1
        })

        assert evargs.get_rule(rule={'cast': int, 'default': 2})['default'] == 2
        assert evargs.get_rule(rule={'cast': int})['default'] == 1

        rules = {
            'a': {'cast': int, 'default': 3},
            'b': {'cast': int},
        }

        assert evargs.get_rule('a', rules=rules)['default'] == 3
        assert evargs.get_rule('b', rules=rules)['default'] == 1

    def test_get_rule_options(self):
        evargs = EvArgs()

        evargs.set_default_rule({'default': 1})

        rules = {
            'a': {'cast': int, 'default': 1},
            'b': {'cast': int, 'default': 2},
            'c': {'cast': str},
            'd': {'cast': str}
        }

        defaults = evargs.get_rule_options('default', rules)

        assert defaults['b'] == 2
        assert defaults['c'] == 1

        evargs = EvArgs()

        evargs.initialize(rules)

        defaults = evargs.get_rule_options('default')

        assert defaults['b'] == 2
        assert defaults['c'] is None

    def test_create_rule(self):
        evargs = EvArgs()

        evargs.set_default_rule({'required': True, 'validation': 'alphabet'})

        rule = evargs.create_rule(required=False)

        assert rule['required'] is False

        rule = evargs.create_rule(required=True)

        assert rule['required'] is True

        rule = evargs.create_rule(raise_error=0)

        assert rule['required'] is True
        assert rule['raise_error'] == 0

        rule = evargs.create_rule(validation=None)

        assert rule['validation'] is None

        with pytest.raises(EvArgsException):
            evargs.create_rule(unknown=False)

    def test_create_rule_args(self):
        evargs = EvArgs()

        rule = evargs.create_rule(int, True, 0, True, True, 'unsigned', None, None, None, None, 'exist', 1, True, False, {'help': 'Help!'})

        assert rule['validation'] == 'unsigned'
        assert rule['post_apply'] == 'exist'
        assert rule['raise_error'] == 1
        assert rule['list'] is True
        assert rule['multiple'] is False
        assert rule['help'] == 'Help!'

    def test_set_rule(self):
        evargs = EvArgs()

        evargs.set_rule('a', {'cast': int, 'default': 1})
        evargs.set_rule('b', {'cast': int, 'default': 2})
        evargs.set_rule('c', {'cast': str})

        evargs.put('a', None)
        evargs.put('b', 3)
        evargs.put('c', 'ABC')

        assert evargs.get('a') == 1
        assert evargs.get('b') == 3
        assert evargs.get('c') == 'ABC'

    def test_set_rules(self):
        evargs = EvArgs()

        evargs.set_rules({
            'a': {'cast': int, 'default': 1},
            'b': {'cast': int, 'default': 2},
            'c': {'cast': str}
        })

        evargs.put('a', None)
        evargs.put('b', 3)
        evargs.put('c', 'ABC')

        assert evargs.get('a') == 1
        assert evargs.get('b') == 3
        assert evargs.get('c') == 'ABC'
