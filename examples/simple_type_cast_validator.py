import re
from evargs import TypeCast, Validator, ValidateException
from enum import Enum

'''
python3 simple_type_cast_validator.py
'''


class H_He_Li_Be(Enum):
    H = 1
    HE = 2
    LI = 3
    BE = 4


def exec_fn(fn, v):
    r = fn(v)

    print(v, r)


def exec_fn_enum(fn, cls, v):
    r = fn(cls, v)

    print(v, r)


def main():
    type_cast()
    validator()


def type_cast():
    print('to_int:')

    fn = TypeCast.to_int

    exec_fn(fn, '123')
    exec_fn(fn, ' 456 ')
    exec_fn(fn, '-1.5')
    exec_fn(fn, '-123')

    print('')
    print('to_round_int:')

    fn = TypeCast.to_round_int

    exec_fn(fn, '0.4')
    exec_fn(fn, '0.5')
    exec_fn(fn, '1.1')
    exec_fn(fn, '1.5')
    exec_fn(fn, '1.8')
    exec_fn(fn, '2.1')
    exec_fn(fn, '2.5')
    exec_fn(fn, '3.1')
    exec_fn(fn, '3.5')
    exec_fn(fn, '-0.5')
    exec_fn(fn, '-1.5')
    exec_fn(fn, '-2.1')
    exec_fn(fn, '-2.5')
    exec_fn(fn, '-3.1')

    print('')
    print('to_float:')

    fn = TypeCast.to_float

    exec_fn(fn, '1.4')
    exec_fn(fn, '2.5')

    print('')
    print('to_bool:')

    fn = TypeCast.to_bool

    exec_fn(fn, '1')
    exec_fn(fn, 'True')
    exec_fn(fn, '0')
    exec_fn(fn, 0)
    exec_fn(fn, 'False')

    print('')
    print('to_enum:')

    fn = TypeCast.to_enum_loose

    exec_fn_enum(fn, H_He_Li_Be, 1)
    exec_fn_enum(fn, H_He_Li_Be, 3)
    exec_fn_enum(fn, H_He_Li_Be, 4)

    fn = TypeCast.to_enum_loose

    exec_fn_enum(fn, H_He_Li_Be, '1')
    exec_fn_enum(fn, H_He_Li_Be, '2')
    exec_fn_enum(fn, H_He_Li_Be, 3)
    exec_fn_enum(fn, H_He_Li_Be, 4)
    exec_fn_enum(fn, H_He_Li_Be, ' 1 ')


def exec_validate(fn, v, *args):
    try:
        fn(v, *args)

        success = True
    except ValidateException:
        success = False

    print(v, success)


def validator():
    print('')
    print('validator:')

    validator = Validator()

    exec_validate(validator.validate_size, 'ABC', 3)
    exec_validate(validator.validate_sizes, 'ABCD', 3, 10)
    exec_validate(validator.validate_size, [1, 2, 3], 3)
    exec_validate(validator.validate_size, [1, 2, 3], 4)

    exec_validate(validator.validate_alphabet, 'ABC')
    exec_validate(validator.validate_alphanumeric, 'ABC123')
    exec_validate(validator.validate_char_numeric, '21332')
    exec_validate(validator.validate_char_numeric, '21332D')
    exec_validate(validator.validate_regex, 'abcd', r'^[a-d]{1,5}$')
    exec_validate(validator.validate_regex, 'abcd123', r'^[a-d]{1,5}$')

    exec_validate(validator.validate_unsigned, 5)
    exec_validate(validator.validate_unsigned, -5)

    print('')


if __name__ == '__main__':
    main()
