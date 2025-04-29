from evargs import ExpEvArgs, Validator, ValidateException
import json

'''
python3 customize_validator.py
'''


class MyValidator(Validator):
    def validate_length248(self, v):
        if not (len(v) == 2 or len(v) == 4 or len(v) == 8):
            self.raise_error('Length is not 2,4,8.', v)


def main():
    validator = MyValidator()

    evargs = ExpEvArgs(validator)

    evargs.initialize({
        'a': {'cast': str, 'validation': 'length248'},
        'b': {'cast': str, 'validation': 'length248'},
    })

    evargs.parse('a=AA; b=12345678;')

    print('Output:')
    print(evargs.get('a'))
    print(evargs.get('b'))
    print('')

    try:
        evargs.parse('b=123456789;')
    except ValidateException as e:
        print('Error test:')
        print(str(e))


if __name__ == "__main__":
    main()
