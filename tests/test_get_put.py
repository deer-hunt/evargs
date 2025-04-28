from evargs import EvArgs, EvArgsException, ValidateException
from evargs.modules import MultipleParam
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
            'a': {'cast': int},
            'b': {'cast': str},
            'c': {'cast': int, 'list': True},
            'd': {'cast': int, 'multiple': True},
        })

        evargs.put_values({
            'a': 1,
            'b': 'abc',
            'c': [1, 2, 3],
            'd': 1
        })

        evargs.put('d', 2)
        evargs.put('d', 3)

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
            'a': {'cast': int, 'list': True},
            'b': {'cast': int, 'multiple': True},
            'c': {'cast': int, 'list': True, 'multiple': True},
        })

        evargs.put_values({
            'a': [1, 2, 3],
            'b': 1,
            'c': [1, 2, 3]
        })

        evargs.put('b', 2)

        evargs.put('c', ['1', '2', '3'])

        values = evargs.get_values()

        assert values['a'] == [1, 2, 3]
        assert values['b'] == [1, 2]
        assert values['c'] == [[1, 2, 3], [1, 2, 3]]

    def test_put(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'cast': int},
            'b': {'cast': int, 'list': True},
            'c': {'cast': int, 'multiple': True},
        })

        evargs.put('a', 1)
        evargs.put('b', [7, 8, 9])
        evargs.put('c', 1)
        evargs.put('c', 2)

        assert evargs.get('a') == 1
        assert evargs.get('b') == [7, 8, 9]
        assert evargs.get('c') == [1, 2]
        assert evargs.get('c', 1) == 2

        evargs.delete('c')
        evargs.put('c', 3)
        evargs.put('c', 5)

        assert evargs.get('c', 0) == 3
        assert evargs.get('c', 1) == 5

        evargs.initialize({
            'a': {'cast': int, 'validation': 'unsigned'},
        })

        with pytest.raises(ValidateException):
            evargs.put('a', -1)

    def test_put_values(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'cast': int},
            'b': {'cast': str},
            'c': {'cast': str},
        }, ignore_unknown=True)

        evargs.put_values({'a': 1, 'b': 'BBB', 'c': 'CCC', 'x': 'XXXX'})

        assert evargs.get('a') == 1
        assert evargs.get('b') == 'BBB'

    def test_put_keep_original(self):
        evargs = EvArgs()

        evargs.initialize({
            'a': {'cast': int, 'validation': 'unsigned'},
            'b': {'cast': int, 'validation': ('range', 1, 100)},
            'c': {'cast': float},
        })

        evargs.put('a', -1, keep_original=True)
        evargs.put('b', 101, keep_original=True)
        evargs.put('c', 1, keep_original=True)

        assert evargs.get('a') == -1
        assert evargs.get('b') == 101
        assert evargs.get('c') == 1

        evargs.put_values({
            'a': -2,
            'b': 102,
            'c': 2
        }, keep_original=True)

        assert evargs.get('a') == -2
        assert evargs.get('b') == 102
        assert evargs.get('c') == 2

    def test_delete(self):
        evargs = EvArgs()

        # Using assign instead of initialize().parse()
        evargs.initialize({
            'a': {'cast': int, 'list': True},
            'b': {'cast': int},
        })

        evargs.put_values({
            'a': [1, 2, 3]
        })

        evargs.delete('a')

        assert evargs.get('a') == []

        evargs.reset()

        assert evargs.get_values() == {}
