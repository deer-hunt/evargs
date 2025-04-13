from evargs import EvArgs, EvArgsException, EvValidateException
import json

'''
python3 various_rules.py
'''


def main():
    evargs = EvArgs()

    evargs.initialize({
        'a': {'type': int, 'list': True},
        'b': {'type': int, 'multiple': True},
        'c': {'type': lambda v: v.upper()},
        'd': {'type': lambda v: v.upper(), 'post_apply_param': lambda vals: '-'.join(vals)},
        'e': {'type': int, 'validation': ['range', 1, 10]}
    })

    evargs.parse('a=25,80,443; b>= 1; b<6; c=tcp; d=X,Y,z ;e=5;')

    print(json.dumps(evargs.get_values(), indent=4))


if __name__ == "__main__":
    main()
