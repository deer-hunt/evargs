from evargs import EvArgs, EvArgsException, EvValidateException
import pytest
import re


# Document: https://github.com/deer-hunt/evargs/
class TestRuleEvaluate:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_evaluate1(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': int, 'multiple': True},
            'a2': {'type': int},
            'a3': {'type': int},
            'b': {'type': int},
            'c': {'type': int, 'list': True},
            'd': {'type': lambda v: v.upper()},
            'e': {'type': float},
            'e2': {'type': float, 'list': True},
            'f': {'type': lambda v: v.upper(), 'post_apply_param': lambda vals: '-'.join(vals)},
            'g': {'type': int},
            'h': {'type': int},
            'z': {'type': int, 'multiple': True}
        })

        assigns = 'a>= 1; a<6 ; a2=+2; a3= -2; b=8; b=9; c=80,443; d=tcp; e=4.5; e2=1.1,1.2,1.3; f=X,Y,z ; g=-1; g=-2; g=-3;h != 9 ; ;z>=5; z<7'

        evargs.parse(assigns)

        assert evargs.evaluate('a', 1) is True
        assert evargs.evaluate('a', 5) is True
        assert evargs.evaluate('a', 7) is False
        assert evargs.evaluate('a2', 2) is True
        assert evargs.evaluate('a3', -2) is True
        assert evargs.evaluate('c', 443) is True
        assert evargs.evaluate('d', 'TCP') is True
        assert evargs.evaluate('e', 4.5) is True
        assert evargs.evaluate('e2', 1.1) is True
        assert evargs.evaluate('f', 'X-Y-Z') is True
        assert evargs.evaluate('g', -3) is True
        assert evargs.evaluate('h', 8) is True
        assert evargs.evaluate('z', 999) is False

    def test_evaluate2(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': str},
        })

        assigns = 'a= "A,B,C" ;'

        evargs.parse(assigns)

        assert evargs.evaluate('a', 'A,B,C') is True

        assigns = "a= ' A,B,C ';"

        evargs.parse(assigns)

        assert evargs.evaluate('a', ' A,B,C ') is True

    def test_evaluate_list(self):
        evargs = EvArgs()

        # `list_or` adjust automatically by operator if `list_or` is None.
        #  = : True
        #  > : True
        #  < : True
        #  != : False

        evargs.initialize({
            'a': {'type': int, 'list': True},
            'b1': {'type': int, 'list': True, 'list_or': None},
            'b2': {'type': int, 'list': True, 'list_or': None},
            'c': {'type': int, 'list': True},
        })

        evargs.parse('a= 1,2,3,4,5;b1>5,6,7;b2>=5,6,7;c!=1,5,10')

        assert evargs.evaluate('a', 1) is True
        assert evargs.evaluate('a', 2) is True
        assert evargs.evaluate('a', 6) is False

        assert evargs.evaluate('b1', 10) is True
        assert evargs.evaluate('b1', 6) is True

        assert evargs.evaluate('b2', 10) is True
        assert evargs.evaluate('b2', 5) is True

        assert evargs.evaluate('c', 1) is False
        assert evargs.evaluate('c', 4) is True
        assert evargs.evaluate('c', 10) is False
        assert evargs.evaluate('c', 20) is True

    def test_evaluate_multiple(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': int, 'multiple': True},
            'b': {'type': int, 'multiple': True, 'multiple_or': False},
            'c': {'type': int, 'multiple': True, 'multiple_or': True},
        })

        assigns = 'a>=1; a<10;' \
                  'b>=1; b<10;' \
                  'c<1; c>10;'

        evargs.parse(assigns)

        assert evargs.evaluate('a', 3) is True
        assert evargs.evaluate('b', 3) is True
        assert evargs.evaluate('c', -10) is True
        assert evargs.evaluate('c', 20) is True

    def test_evaluate_customize(self):
        evargs = EvArgs()

        # Force True
        evargs.initialize({
            'a': {'type': int, 'evaluate': lambda v, *args: True},
        }).parse('a=1')

        assert evargs.get('a') == 1

        assert evargs.evaluate('a', 2) is True

        # Pass
        evargs.initialize({
            'a': {'type': int, 'evaluate': lambda v, *args: None},
        }).parse('a=1')

        assert evargs.evaluate('a', 1) is True

        # evaluate_param
        evargs.initialize({
            'a': {'type': int, 'evaluate_param': lambda rule, param, v: v % param.get(0) == 0},
            'b': {'type': int, 'multiple': True, 'evaluate_param': lambda rule, param, v: v % param.get(0) == param.get(1)},
        }).parse('a=3;b=3;b=1;')

        assert evargs.evaluate('a', 3) is True
        assert evargs.evaluate('a', 6) is True
        assert evargs.evaluate('a', 8) is False

        assert evargs.evaluate('b', 7) is True
        assert evargs.evaluate('b', 13) is True
