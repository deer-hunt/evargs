from evargs import ExpEvArgs, EvArgsException, ValidateException, Operator
import pytest
import re


# Document: https://github.com/deer-hunt/evargs/
class TestExpEvaluate:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_cast(self):
        evargs = ExpEvArgs()

        evargs.initialize({
            'int1': {'cast': int},
            'int2': {'cast': int},
            'int3': {'cast': int},
            'float1': {'cast': float},
            'str1': {'cast': str},
        })

        evargs.parse('int1=10;int2=-1;int3= -5 ;float1=3.14;str1=XYZ')

        assert evargs.get('int1') == 10
        assert evargs.get('int2') == -1
        assert evargs.get('int3') == -5
        assert evargs.get('float1') == 3.14
        assert evargs.get('str1') == 'XYZ'

    def test_not_equal(self):
        evargs = ExpEvArgs()

        evargs.initialize({
            'int1': {'cast': int},
            'float1': {'cast': float},
            'str1': {'cast': str},
        })

        evargs.parse('int1 != 5;float1!=1.2;str1!=TGC')

        assert evargs.get('int1') == 5
        assert evargs.get('float1') == 1.2
        assert evargs.get('str1') == 'TGC'

        assert evargs.evaluate('int1', 5) is False
        assert evargs.evaluate('int1', 1) is True

        assert evargs.evaluate('float1', 1.2) is False
        assert evargs.evaluate('float1', 1.3) is True

        assert evargs.evaluate('str1', 'TGC') is False
        assert evargs.evaluate('str1', '') is True

        evargs.parse('str1!=TGC', reset=False)
        assert evargs.evaluate('str1', 'TGX') is True

    def test_default(self):
        evargs = ExpEvArgs()

        evargs.initialize({
            'a': {'cast': int, 'default': 42},
            'b': {'cast': str, 'default': 'default_value'},
        })

        evargs.parse('a=;b=')

        assert evargs.get('a') == 42
        assert evargs.get('b') == 'default_value'

    def test_str(self):
        evargs = ExpEvArgs()

        evargs.initialize({
            'a': {'cast': str},
        })

        expression = 'a= "A,B,C" ;'

        evargs.parse(expression)

        assert evargs.evaluate('a', 'A,B,C') is True

        expression = "a= ' A,B,C ';"

        evargs.parse(expression)

        assert evargs.evaluate('a', ' A,B,C ') is True

    def test_validation(self):
        evargs = ExpEvArgs()

        evargs.initialize({
            'a': {'cast': int, 'validation': ('range', 1, 100)},
            'b': {'cast': str, 'choices': ['A', 'T', 'G', 'C']},
        })

        evargs.parse('a=50;b=T')
        assert evargs.get('a') == 50
        assert evargs.get('b') == 'T'

        with pytest.raises(ValidateException):
            evargs.parse('a=150')

        with pytest.raises(ValidateException):
            evargs.parse('b=X')

    def test_evaluate_list(self):
        evargs = ExpEvArgs()

        # `list_or` adjust automatically by operator if `list_or` is None.
        #  = : True
        #  > : True
        #  < : True
        #  != : False

        evargs.initialize({
            'a': {'cast': int, 'list': True},
            'b': {'cast': int, 'list': True, 'list_or': None},
            'c': {'cast': int, 'list': True},
        })

        evargs.parse('a= 1,2,3,4,5; b>5,6,7;;c!=1,5,10')

        assert evargs.evaluate('a', 1) is True
        assert evargs.evaluate('a', 2) is True
        assert evargs.evaluate('a', 6) is False

        assert evargs.evaluate('b', 10) is True
        assert evargs.evaluate('b', 6) is True
        assert evargs.evaluate('b', 1) is False

        assert evargs.evaluate('c', 4) is True
        assert evargs.evaluate('c', 20) is True
        assert evargs.evaluate('c', 1) is False
        assert evargs.evaluate('c', 10) is False

    def test_restrict_operator(self):
        evargs = ExpEvArgs()

        evargs.initialize({
            'a': {'cast': int, 'allowed_operator': Operator.EQUAL},
            'b': {'cast': int, 'allowed_operator': (Operator.EQUAL | Operator.GREATER)},
            'c': {'cast': int, 'allowed_operator': Operator.NOT_EQUAL}
        })

        evargs.parse('a=1; b>=2; c!=4')

        with pytest.raises(EvArgsException):
            evargs.parse('a!=1')

        with pytest.raises(EvArgsException):
            evargs.parse('a>1')

        with pytest.raises(EvArgsException):
            evargs.parse('b<=1')

        with pytest.raises(EvArgsException):
            evargs.parse('c=1')

    def test_cast_fn(self):
        evargs = ExpEvArgs()

        evargs.initialize({
            'a': {'cast': lambda v: v.upper()},
            'b': {'cast': lambda v: v.upper(), 'post_apply': lambda vals: '-'.join(vals)}
        })

        expression = 'a=tcp; b=X,Y,z ; '

        evargs.parse(expression)

        assert evargs.evaluate('a', 'TCP') is True
        assert evargs.evaluate('b', 'X-Y-Z') is True

    def test_evaluation(self):
        evargs = ExpEvArgs()

        # Force True
        evargs.initialize({
            'a': {'cast': int, 'evaluation': lambda v, *args: True},
        }).parse('a=1')

        assert evargs.get('a') == 1

        assert evargs.evaluate('a', 2) is True

        # Pass
        evargs.initialize({
            'a': {'cast': int, 'evaluation': lambda v, *args: None},
        }).parse('a=1')

        assert evargs.evaluate('a', 1) is True
