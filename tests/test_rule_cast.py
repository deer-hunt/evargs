import pytest

from evargs import EvArgs, ValidateException
from evargs.helper import ExpressionParser


# Document: https://github.com/deer-hunt/evargs/
class TestRuleCast:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_cast_int(self):
        evargs = EvArgs()

        assert evargs.assign('2', cast=int) == 2
        assert evargs.assign(' +2', cast=int) == 2
        assert evargs.assign(' -2', cast=int) == -2
        assert evargs.assign('2.1', cast=int) == 2
        assert evargs.assign('+2.1', cast=int) == 2
        assert evargs.assign('-2.1', cast='int') == -2
        assert evargs.assign(-2.1, cast='int') == -2
        assert evargs.assign(None, cast='int', default=3) == 3
        assert evargs.assign('AAA', cast='int', default=5) == 5

        assert evargs.assign('', cast=int) is None
        assert evargs.assign('', cast=int, raise_error=False) is None

        with pytest.raises(ValidateException):
            evargs.assign(None, cast=int, nullable=False)

        evargs.initialize({
            'int1': {'cast': int},
            'int2': {'cast': int, 'nullable': False},
            'int3': {'cast': int, 'list': True},
            'int4': {'cast': int, 'multiple': True},
        })

        evargs.put('int1', 1)

        evargs.put('int1', '2')

        assert evargs.get('int1') == 2

        with pytest.raises(ValidateException):
            evargs.put('int2', '')

        evargs.put('int3', [1, 2, 3])

        assert evargs.get('int3') == [1, 2, 3]

        evargs.put('int3', '')

        assert evargs.get('int3') == []

        evargs.put('int4', 1)

    def test_cast_round_int(self):
        evargs = EvArgs()

        assert evargs.assign('0', cast='round_int') == 0
        assert evargs.assign('0.4', cast='round_int') == 0
        assert evargs.assign('0.5', cast='round_int') == 1
        assert evargs.assign('1.4', cast='round_int') == 1

        assert evargs.assign('1.5', cast='round_int') == 2
        assert evargs.assign('2', cast='round_int') == 2
        assert evargs.assign('2.1', cast='round_int') == 2
        assert evargs.assign(' -2.1', cast='round_int') == -2
        assert evargs.assign('2.4', cast='round_int') == 2

        assert evargs.assign('3.1', cast='round_int') == 3
        assert evargs.assign('3.5', cast='round_int') == 4

        assert evargs.assign('-2.1', cast='round_int') == -2
        assert evargs.assign(-2.1, cast='round_int') == -2
        assert evargs.assign(-2.5, cast='round_int') == -3
        assert evargs.assign(-3.4, cast='round_int') == -3

        assert evargs.assign(None, cast='round_int', default=3) == 3
        assert evargs.assign('AAA', cast='round_int', default=5) == 5

        assert evargs.assign('', cast='round_int') is None
        assert evargs.assign('', cast='round_int', raise_error=False) is None

        with pytest.raises(ValidateException):
            evargs.assign(None, cast='round_int', nullable=False)

    def test_cast_float(self):
        evargs = EvArgs()

        assert evargs.assign('2.1', cast=float) == 2.1
        assert evargs.assign(2.2, cast=float) == 2.2
        assert evargs.assign(' -2.5', cast=float) == -2.5
        assert evargs.assign('0.1', cast=float) == 0.1
        assert evargs.assign('+2.1', cast=float) == 2.1
        assert evargs.assign('-20.1', cast='float') == -20.1
        assert evargs.assign(-2.1, cast='float') == -2.1
        assert evargs.assign(None, cast='float', default=3.3) == 3.3
        assert evargs.assign('AAA', cast='float', default=5.5) == 5.5

        assert evargs.assign('', cast=float) is None
        assert evargs.assign('', cast=float, raise_error=False) is None

        with pytest.raises(ValidateException):
            evargs.assign(None, cast=float, nullable=False)

        evargs.initialize({
            'float1': {'cast': float},
            'float2': {'cast': float, 'nullable': False},
            'float3': {'cast': float, 'list': True},
            'float4': {'cast': float, 'multiple': True},
        })

        evargs.put('float1', 1.1)

        evargs.put('float1', '2.1')

        assert evargs.get('float1') == 2.1

        with pytest.raises(ValidateException):
            evargs.put('float2', '')

        evargs.put('float3', [1.1, 2.2, 3.3])

        assert evargs.get('float3') == [1.1, 2.2, 3.3]

        evargs.put('float3', '')

        assert evargs.get('float3') == []

        evargs.put('float4', 1.1)

    def test_cast_complex(self):
        evargs = EvArgs()

        assert evargs.assign('2', cast=complex) == 2
        assert evargs.assign(2j + 1, cast=complex) == 2j + 1
        assert evargs.assign('4+4j', cast=complex) == 4 + 4j
        assert evargs.assign('10j', cast=complex) == 10j
        assert evargs.assign('0.5j', cast=complex) == 0.5j
        assert evargs.assign('-20.1', cast='complex') == -20.1
        assert evargs.assign(None, cast='complex', default=10j) == 10j
        assert evargs.assign('AAA', cast='complex', default=1.5j) == 1.5j

        assert evargs.assign('', cast=complex) is None
        assert evargs.assign('', cast=complex, raise_error=False) is None

        with pytest.raises(ValidateException):
            evargs.assign(None, cast=complex, nullable=False)

        evargs.initialize({
            'complex1': {'cast': complex},
            'complex2': {'cast': complex, 'nullable': False},
        })

        evargs.put('complex1', 10j + 1)

        evargs.put('complex1', '1+4j')

        evargs.put('complex2', 1 + 5j)

    def test_cast_str(self):
        evargs = EvArgs()

        assert evargs.assign(1, cast=str) == '1'
        assert evargs.assign(1.1, cast=str) == '1.1'
        assert evargs.assign('c', cast=str) == 'c'
        assert evargs.assign(None, cast='str') is None
        assert evargs.assign('', cast='str') == ''

    def test_cast_bool(self):
        evargs = EvArgs()

        assert evargs.assign(1, cast=bool) is True
        assert evargs.assign('1', cast=bool) is True
        assert evargs.assign(0, cast=bool) is False
        assert evargs.assign('0', cast=bool) is False
        assert evargs.assign(None, cast=bool, default=False) is False

    def test_cast_bool_strict(self):
        evargs = EvArgs()

        assert evargs.assign(1, cast='bool_strict') is True
        assert evargs.assign('1', cast='bool_strict') is True
        assert evargs.assign('', cast='bool_strict', default=True) is True
        assert evargs.assign(None, cast='bool_strict') is None
        assert evargs.assign('AAAAA', cast='bool_strict', raise_error=False) is None

    def test_cast_raw(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'cast': 'raw'},
            'b': {'cast': 'raw'},
            'c': {'cast': 'raw'},
            'd': {'cast': 'raw'},
            'e': {'cast': 'raw', 'nullable': True},
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

        with pytest.raises(ValidateException):
            assert evargs.get('x') is None

    def test_cast_fn(self):
        evargs = EvArgs()

        def fn_even(v):
            return int(float(v) / 2) * 2

        def fn_calc(v):
            return 2 ** int(float(v))

        assert evargs.assign(2, cast=fn_even) == 2
        assert evargs.assign(9, cast=fn_even) == 8
        assert evargs.assign(8, cast=fn_calc) == 256
        assert evargs.assign(10, cast=fn_calc) == 1024

        evargs.initialize({
            'a': {'cast': lambda v: None}
        })

        with pytest.raises(ValidateException):
            evargs.assign(None, cast=lambda v: None, nullable=False)

    def test_cast_expression(self):
        evargs = EvArgs()

        assert evargs.assign('1 + 2', lambda v: ExpressionParser.parse(v)) == 3
        assert evargs.assign('2 * 4 ', lambda v: ExpressionParser.parse(v)) == 8
        assert evargs.assign('1 * 4 + (10 - 4)/2 ', lambda v: ExpressionParser.parse(v)) == 7
        assert evargs.assign('( (1 + 4) * (6 - 4))**2 ', lambda v: ExpressionParser.parse(v)) == 100
