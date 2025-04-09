from evargs import EvArgs, EvArgsException, EvValidateException
import pytest
import re


# Document: https://github.com/deer-hunt/evargs/
class TestGeneral:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_flexible(self):
        evargs = EvArgs()

        evargs.initialize({}, {'default': 'B'}, flexible=True)

        assigns = 'a=1;b= 2 ;c=A;d=;'

        evargs.parse(assigns)

        assert evargs.get('a') == '1'
        assert evargs.get('b') == '2'
        assert evargs.get('c') == 'A'
        assert evargs.get('d') == 'B'

        evargs.initialize({}, {'type': int, 'default': 3}, flexible=True)

        assigns = 'a=1;b= 2 ;c=3.23;'

        evargs.parse(assigns)

        assert evargs.get('a') == 1
        assert evargs.get('b') == 2
        assert evargs.get('c') == 3
        assert evargs.get('d') == 3

        evargs.initialize({}, {'type': int, 'list': True}, flexible=True)

        assigns = 'a=1,2,3;b= 1,2,3 ;c= 1.2, 2.1, 3.3;'

        evargs.parse(assigns)

        assert evargs.get('a') == [1, 2, 3]
        assert evargs.get('b') == [1, 2, 3]
        assert evargs.get('c') == [1, 2, 3]

    def test_require_all(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': int, 'default': 1},
            'b': {'type': int, 'default': 1},
            'c': {'type': str},
            'd': {'type': str}
        }, require_all=True)

        assigns = 'b= 2 ;d=;'

        with pytest.raises(EvValidateException):
            evargs.parse(assigns)

    def test_ignore_unknown(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': int, 'default': 1},
        }, ignore_unknown=True)

        evargs.parse('b= 2 ;c=;')  # Exception does not raise.

        assert evargs.get('a') == 1
        assert evargs.get('b') is None

        evargs.initialize({
            'a': {'type': int, 'default': 1},
        })

        with pytest.raises(EvValidateException):
            evargs.parse('b= 2 ;c=;')  # Exception raise.

    def test_set_options(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': int},
            'b': {'type': int},
            'c': {'type': int},
        })

        evargs.set_options(require_all=True, ignore_unknown=True)

        evargs.parse('a=1;b=2;c=3;d=3')

        assert evargs.get('a') == 1
        assert evargs.get('c') == 3

        with pytest.raises(EvValidateException):
            evargs.parse('a=1;b=2;')
