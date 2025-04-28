from evargs import EvArgs, EvArgsException, ValidateException
import pytest
import re


# Document: https://github.com/deer-hunt/evargs/
class TestOptions:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_flexible(self):
        evargs = EvArgs()

        evargs.initialize({}, {'default': 'B'}, flexible=True)

        assert evargs.assign('1') == '1'
        assert evargs.assign('2') == '2'
        assert evargs.assign(None) == 'B'

        evargs.initialize({}, {'cast': int, 'default': 3}, flexible=True)

        assert evargs.assign('1') == 1
        assert evargs.assign('2') == 2
        assert evargs.assign('3.23') == 3
        assert evargs.assign('') == 3

        evargs.initialize({}, {'cast': int, 'list': True}, flexible=True)

        assert evargs.assign([1, 2, 3]) == [1, 2, 3]
        assert evargs.assign(['1', '2', '3']) == [1, 2, 3]
        assert evargs.assign([1.2, 2.1, 3.3]) == [1, 2, 3]

    def test_required_all(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'cast': int, 'default': 1},
            'b': {'cast': int, 'default': 1},
            'c': {'cast': str},
            'd': {'cast': str}
        }, required_all=True)

        with pytest.raises(ValidateException):
            evargs.assign('')

        with pytest.raises(ValidateException):
            evargs.assign(None)

    def test_ignore_unknown(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'cast': int, 'default': 1},
        })

        with pytest.raises(ValidateException):
            assert evargs.get('z') is None

        evargs.initialize({
            'a': {'cast': int, 'default': 1},
        }, ignore_unknown=True)

        assert evargs.get('z') is None

    def test_set_options(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'cast': int},
            'b': {'cast': int},
            'c': {'cast': int},
        })

        evargs.set_options(required_all=True, ignore_unknown=True)

        evargs.put('a', 1)
        evargs.put('c', '3')

        assert evargs.get('a') == 1
        assert evargs.get('c') == 3

        with pytest.raises(ValidateException):
            assert evargs.get('b') is None
