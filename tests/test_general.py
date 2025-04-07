from evargs import EvArgs, EvArgsException, EvValidateException
import pytest
import re


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

    def test_operator(self):
        evargs = EvArgs()

        evargs.initialize({
            'a1': {'type': int},
            'a2': {'type': int},
            'b1': {'type': int},
            'b2': {'type': int},
            'c': {'type': int},
            'd': {'type': int},
        })

        evargs.parse('a1>1;a2 >= 1;b1<1;b2<=3;c=3;d != 3;')

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

    def test_set_rule(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': int},
            'b': {'type': int}
        })

        evargs.set_rule('c', {'type': int})

        evargs.parse('c=3')

        assert evargs.get('c') == 3

    def test_methods(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': int, 'list': True},
            'b': {'type': int},
            'c': {'type': int},
        })

        assigns = 'a= 1,2,3 ; b=8; c=80,443;'

        evargs.parse(assigns)

        assert evargs.get('a') == [1, 2, 3]
        assert evargs.has_param('d') is False
        assert evargs.get_param('a').name == 'a'
        assert len(evargs.get_params()) == 3
        assert evargs.count_params() == 3
        assert evargs.get_rule('a') is not None

    def test_errors(self):
        evargs = EvArgs()

        with pytest.raises(EvArgsException):
            evargs.initialize({
                'a': {'type': int, 'unknown': True}
            })

        evargs.initialize({
            'a': {'type': int}
        })

        with pytest.raises(EvArgsException):
            evargs.parse('a>= 1 a< ; ')

        with pytest.raises(EvValidateException):
            evargs.parse('e1=8')
