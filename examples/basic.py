from evargs import EvArgs, EvArgsException, EvValidateException
import sys

'''
python3 basic.py
'''


def main():
    evargs = EvArgs()

    evargs.initialize({
        'a': {'type': bool},
        'b': {'type': 'bool'},  # 'bool' = bool
        'c': {'type': int},
        'd': {'type': float, 'default': 3.14},
        'e': {'type': str},
    })

    evargs.parse('a= 1 ;b=True;c=10;d=;e=H2O')

    print(evargs.get('a'), evargs.evaluate('a', True))
    print(evargs.get('b'), evargs.evaluate('b', True))
    print(evargs.get('c'), evargs.evaluate('c', 10))
    print(evargs.get('d'), evargs.evaluate('d', 3.14))
    print(evargs.get('e'), evargs.evaluate('e', 'H2O'))


if __name__ == "__main__":
    main()
