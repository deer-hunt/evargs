from evargs import ExpEvArgs, EvArgsException, ValidateException
import json

'''
python3 various_rules.py
'''


def main():
    evargs = ExpEvArgs()

    evargs.initialize({
        'a': {'cast': int, 'list': True},
        'b': {'cast': int, 'multiple': True},
        'c': {'cast': lambda v: v.upper()},
        'd': {'cast': lambda v: v.upper(), 'post_apply': lambda vals: '-'.join(vals)},
        'e': {'cast': int, 'validation': ['range', 1, 10]}
    })

    evargs.parse('a=25,80,443; b>= 1; b<6; c=tcp; d=X,Y,z ;e=5;')

    print(json.dumps(evargs.get_values(), indent=4))

    print('')
    print('b:')
    print(1, evargs.evaluate('b', 1))
    print(5, evargs.evaluate('b', 5))
    print(10, evargs.evaluate('b', 10))


if __name__ == "__main__":
    main()
