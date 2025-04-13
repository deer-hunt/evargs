from evargs import EvArgs, Validator, EvValidateException
import json

'''
python3 customize_validator.py
'''


class MyValidator(Validator):
    def validate_length248(self, name: str, v):
        if not (len(v) == 2 or len(v) == 4 or len(v) == 8):
            self.raise_error('Length is not 2,4,8.')


def main():
    validator = MyValidator()

    evargs = EvArgs(validator)

    evargs.initialize({
        'a': {'type': str, 'validation': 'length248'},
        'b': {'type': str, 'validation': 'length248'},
    })

    evargs.parse('a=AA; b=12345678;')

    print('Output:')
    print(evargs.get('a'))
    print(evargs.get('b'))
    print('')

    try:
        evargs.parse('b=123456789;')
    except EvValidateException as e:
        print('Error test:')
        print(str(e))


if __name__ == "__main__":
    main()
