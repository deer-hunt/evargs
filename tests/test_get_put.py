from evargs import EvArgs, EvArgsException, EvValidateException
import pytest
import re


# Document: https://github.com/deer-hunt/evargs/
class TestGetPut:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_get(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': int},
            'b': {'type': str},
            'c': {'type': int, 'list': True},
            'd': {'type': int, 'multiple': True},
        })

        evargs.parse('a=1;b=abc;c=1,2,3;d=1;d=2;d=3')

        assert evargs.get('a') == 1
        assert evargs.get('a', 0) == 1
        assert evargs.get('b') == 'abc'
        assert evargs.get('c', 0) == [1, 2, 3]
        assert evargs.get('c', -1) == [1, 2, 3]

        assert evargs.get('d', 0) == 1
        assert evargs.get('d', 1) == 2
        assert evargs.get('d', -1) == [1, 2, 3]

    def test_get_values(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': int, 'list': True},
            'b': {'type': int, 'multiple': True},
            'c': {'type': int, 'list': True, 'multiple': True},
        })

        evargs.parse('a=1,2,3;b=1;b=2;c=1,2;c=3,4;')

        assert evargs.get('a') == [1, 2, 3]
        assert evargs.get_values()['b'] == [1, 2]
        assert evargs.get_values()['c'] == [[1, 2], [3, 4]]
        assert evargs.get_param('c').get_list() == [1, 2, 3, 4]

    def test_put(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': int},
            'b': {'type': int, 'list': True},
            'c': {'type': int, 'multiple': True},
        }).parse('b=2,3,4;c=1')

        evargs.put('a', 1)
        evargs.put('b', [7, 8, 9])
        evargs.put('c', 2)

        assert evargs.get('a') == 1
        assert evargs.get('b') == [7, 8, 9]
        assert evargs.get('c') == [1, 2]
        assert evargs.get('c', 1) == 2

        evargs.reset('c')
        evargs.put('c', 3)

        assert evargs.get('c', 0) == 3
        assert evargs.get('c', 1) is None

        evargs.initialize({
            'a': {'type': int, 'validation': 'unsigned'},
        }).parse('a=1;')

        with pytest.raises(EvValidateException):
            evargs.put('a', -1)

    def test_put_values(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': int},
            'b': {'type': str},
            'c': {'type': str},
        }, ignore_unknown=True).parse('a=1;b=2;c=3')

        evargs.put_values({'a': 1, 'b': 'BBB', 'c': 'CCC', 'x': 'XXXX'})

        assert evargs.get('a') == 1
        assert evargs.get('b') == 'BBB'

    def test_reset(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'type': int, 'list': True},
            'b': {'type': int},
        })

        evargs.parse('a=1,2,3;b=1;')

        evargs.reset('a')

        assert evargs.get('a') == []

        evargs.reset_params()

        assert evargs.get_values() == {}
