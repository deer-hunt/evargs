from evargs import EvArgs, EvArgsException, EvValidateException
import pytest
import re


# Document: https://github.com/deer-hunt/evargs/
class TestRuleType:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_type_int(self):
        evargs = EvArgs()

        evargs.initialize({
            'int1a': {'type': int},
            'int1b': {'type': int},
            'int1c': {'type': int},
            'int1d': {'type': int},

            'int2a': {'type': int},
            'int2b': {'type': int},
            'int2c': {'type': int},
            'int2d': {'type': int},

            'int3': {'type': int},
            'int4': {'type': int},
            'int5': {'type': int, 'multiple': True},
            'int6': {'type': int, 'multiple': True},
        })

        assigns = '' \
                  'int1a=2;int1b= + 2;int1c=-2;int1d= - 2;' \
                  'int2a=2.1;int2b= + 2.1;int2c=-2.1;int2d= - 2.1;' \
                  'int3=;int4=;' \
                  'int6=1,2,3,4'

        evargs.parse(assigns)

        assert evargs.get('int1a') == 2
        assert evargs.get('int1b') == 2
        assert evargs.get('int1c') == -2
        assert evargs.get('int1d') == -2

        assert evargs.get('int2a') == 2
        assert evargs.get('int2b') == 2
        assert evargs.get('int2c') == -2
        assert evargs.get('int2d') == -2

        assert evargs.get('int3') is None
        assert evargs.get('int4') is None
        assert evargs.get('int5', 0) is None
        assert evargs.get('int6', 0) == 1

    def test_type_float(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': float},
            'b': {'type': 'float'},
            'c': {'type': float, 'default': 0.001},
            'd': {'type': float, 'default': 0.001}
        })

        assigns = 'a= 0.1 ;b=-0.2;c=0;d=;'

        evargs.parse(assigns)

        assert evargs.get('a') == 0.1
        assert evargs.get('b') == -0.2
        assert evargs.get('c') == 0
        assert evargs.get('d') == 0.001

    def test_type_bool(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': bool},
            'b': {'type': 'bool'},  # 'bool' = bool
            'c': {'type': 'bool'},
            'd': {'type': bool, 'default': False},
            'e': {'type': bool},
        })

        assigns = 'a= 1 ;b=True;c=0;d= ;e=True'

        evargs.parse(assigns)

        assert evargs.get('a') is True
        assert evargs.get('b') is True
        assert evargs.get('c') is False
        assert evargs.get('d') is False
        assert evargs.get('e') is True

    def test_type_bool_strict(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': 'bool_strict'},
            'b': {'type': 'bool_strict'},
            'c': {'type': 'bool_strict'},
            'd': {'type': 'bool_strict', 'default': False},
            'e': {'type': 'bool_strict'},
        })

        value = 'a= 1 ;b=0;c=;d= ;e = a'

        evargs.parse(value)

        assert evargs.get('a') is True
        assert evargs.get('b') is False
        assert evargs.get('c') is None
        assert evargs.get('d') is False
        assert evargs.get('e') is None

    def test_type_str(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': str},
            'b': {'type': 'str'},
            'c': {'type': str, 'default': 'B'},
            'd': {'type': str, 'default': 'B'},
            'e': {'type': str, 'default': ''},
            'f': {'type': str},
        })

        assigns = 'a= A ;b=A;c="A B C";d=;e='

        evargs.parse(assigns)

        assert evargs.get('a') == 'A'
        assert evargs.get('b') == 'A'
        assert evargs.get('c') == 'A B C'
        assert evargs.get('d') == 'B'
        assert evargs.get('e') == ''
        assert evargs.get('f') is None

    def test_type_complex(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': 'complex'},
            'b': {'type': 'complex'},
            'c': {'type': 'complex'},
        })

        assigns = 'a= 2j;b=1+5j;c="2+8j"'

        evargs.parse(assigns)

        assert evargs.get('a') == 2j
        assert evargs.get('b') == 1 + 5j
        assert evargs.get('c') == 2 + 8j

    def test_type_expression(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': 'expression'},
            'b': {'type': 'expression'},
            'c': {'type': 'expression'},
            'd': {'type': 'expression'},
        })

        assigns = 'a= 1 + 2 ;b= 2*4;c="1 * 4 + (10 - 4)/2";d=( (1 + 4) * (6 - 4))**2'

        evargs.parse(assigns)

        assert evargs.get('a') == 3
        assert evargs.get('b') == 8
        assert evargs.get('c') == 7
        assert evargs.get('d') == 100

    def test_type_raw(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': 'raw'},
            'b': {'type': 'raw'},
            'c': {'type': 'raw'},
            'd': {'type': 'raw'},
            'e': {'type': 'raw'},
        })

        # Skip parse

        evargs.put('a', '2')
        evargs.put('b', b'AAA')
        evargs.put('c', (1, 2, 3))
        evargs.put('d', {'a': 1, 'b': 2, 'c': 3})

        assert evargs.get('a') == '2'
        assert evargs.get('b') == b'AAA'
        assert evargs.get('c') == (1, 2, 3)
        assert evargs.get('d') == {'a': 1, 'b': 2, 'c': 3}
        assert evargs.get('e') is None

        with pytest.raises(EvValidateException):
            assert evargs.get('x') is None

    def test_type_fn(self):
        evargs = EvArgs()

        def fn_even(v):
            return int(float(v) / 2) * 2

        def fn_exp(v):
            return 2 ** int(float(v))

        evargs.initialize({
            'a1': {'type': fn_even},
            'a2': {'type': fn_even},
            'b1': {'type': fn_exp},
            'b2': {'type': fn_exp},
        })

        assigns = 'a1= 2;a2=9;b1=8;b2=10'

        evargs.parse(assigns)

        assert evargs.get('a1') == 2
        assert evargs.get('a2') == 8
        assert evargs.get('b1') == 256
        assert evargs.get('b2') == 1024
