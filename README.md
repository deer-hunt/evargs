# EvArgs

<div>

<a href="https://github.com/deer-hunt/evargs/actions/workflows/unit-tests.yml"><img alt="CI - Test" src="https://github.com/deer-hunt/evargs/actions/workflows/unit-tests.yml/badge.svg"></a>
<a href="https://github.com/deer-hunt/evargs/actions/workflows/unit-tests-windows.yml"><img alt="CI - Test" src="https://github.com/deer-hunt/evargs/actions/workflows/unit-tests-windows.yml/badge.svg"></a>
<a href="https://github.com/deer-hunt/evargs/actions/workflows/unit-tests-macos.yml"><img alt="CI - Test" src="https://github.com/deer-hunt/evargs/actions/workflows/unit-tests-macos.yml/badge.svg"></a>
<a href="https://github.com/deer-hunt/evargs/actions/workflows/lint.yml"><img alt="GitHub Actions build status (Lint)" src="https://github.com/deer-hunt/evargs/workflows/Lint/badge.svg"></a>
<a href="https://anaconda.org/conda-forge/evargs"> <img src="https://anaconda.org/conda-forge/evargs/badges/platforms.svg" /> </a>
<a href="https://codecov.io/gh/deer-hunt/evargs"><img alt="Coverage" src="https://codecov.io/github/deer-hunt/evargs/coverage.svg?branch=main"></a>
<img alt="PyPI - Status" src="https://img.shields.io/pypi/status/evargs">
<a href="https://github.com/deer-hunt/evargs/blob/main/LICENSE.md"><img alt="License - MIT" src="https://img.shields.io/pypi/l/evargs.svg"></a>
<a href="https://pypi.org/project/evargs/"><img alt="Newest PyPI version" src="https://img.shields.io/pypi/v/evargs.svg"></a>
<a href="https://anaconda.org/conda-forge/evargs"> <img src="https://anaconda.org/conda-forge/evargs/badges/version.svg" /></a>
<a href="https://pypi.org/project/evargs/"><img alt="Number of PyPI downloads" src="https://img.shields.io/pypi/dm/evargs.svg"></a>
<a href="https://pypi.org/project/evargs"><img alt="Supported Versions" src="https://img.shields.io/pypi/pyversions/evargs.svg"></a>

</div>

<div>
"EvArgs" is a Python module designed for value assignment, easy expression parsing, and type casting. It validates values based on defined rules and offers flexible configuration along with custom validation methods.
</div>


## Installation

**PyPI**

```bash
$ pip install evargs
or
$ pip3 install evargs
```

**Conda**

```
$ conda install conda-forge::evargs
```


## Requirements

- ```python``` and ```pip``` command
- Python 3.6 or later version.


## Features

- It can specify the condition or value-assignment using a simple expression. e.g. `a=1;b>5;c=>1;c<10;`
- Evaluate assigned values. e.g `evargs.evaluate('a', 1)`
- Type cast - str, int, round_int, float, bool, complex, Enum class, custom function...
- Type validation - unsigned, number range, alphabet, regex, any other...
- Put values. It's available to using `put` is without parsing the expression.
- Applying multiple validations.
- Applying Pre-processing method and Post-processing method. 
- Get assigned values.
- Make parameter's description.
- Other support methods for value-assignment.


## Usage

**Basic**

```
from evargs import EvArgs

evargs = EvArgs()

v = evargs.assign(' 1 ', cast=str, trim=True)
v = evargs.assign('1', cast=int, validation=('range', 1, 10))

rules = {'a': {'cast': int}, 'b': {'cast': float}}
values = {'a': '1', 'b': '2.2'}

values = evargs.assign_values(values, rules)
print(values)

evargs.assign('123', cast=int, validation=('range', 1, 150), name='a')
print(evargs.get('a'))
```


```
from evargs import ExpEvArgs

evargs = ExpEvArgs()

evargs.initialize({
  'a': {'cast': bool},
  'b': {'cast': int},
  'c': {'cast': int},
  'd': {'cast': float, 'default': 3.14},
  'e': {'cast': str},
  'f': {'cast': int, 'multiple': True},
}) 

evargs.parse('a=1;b>=5;c=10;d=;e=H2O;f>=5;f<100')

print(evargs.get('a'), evargs.evaluate('a', True))
print(evargs.get('b'), evargs.evaluate('b', 8))
print(evargs.get('c'), evargs.evaluate('c', 10))
print(evargs.get('d'), evargs.evaluate('d', 3.14))
print(evargs.get('e'), evargs.evaluate('e', 'H2O'))
print(evargs.evaluate('f', 50))


Result:
--
True True
True True
10 True
3.14 True
H2O True
```

**Various rules**

```
from evargs import EvArgs

evargs = EvArgs()

evargs.initialize({
  'a': {'cast': int, 'list': True},
  'b': {'cast': int, 'multiple': True},
  'c': {'cast': lambda v: v.upper()},
  'd': {'cast': lambda v: v.upper(), 'post_apply': lambda vals: '-'.join(vals)},
  'e': {'cast': int, 'validation': ['range', 1, 10]}
})

~~~~

print(print(evargs.get_values())

Result:
--
{'a': [25, 80, 443], 'b': [1, 6], 'c': 'TCP', 'd': 'X-Y-Z', 'e': 5}
```

```
evargs.assign(v, cast=ColorEnum, default=ColorEnum.RED)
evargs.assign(v, cast=('enum_value', ColorEnum), required=True)
evargs.assign(1, cast=int, choices=ColorEnum)
```


## Overview

There are 4 way methods in `EvArgs`. In each 4 way methods, it's available for "type-cast and validation" on `rule` option.

### a. Assign the value

Assigning the value. assign method's arguments is rule options. It's available to use type-cast, validation, any other features.

```
v = evargs.assign(' 1 ', cast=str, trim=True)
v = evargs.assign('1', cast=int, validation=('range', 1, 10))

v = evargs.assign_values({'a': {'cast': int}, 'b': {'cast': int}}, {'a': '1', 'b': '2'})

evargs.assign('1.5', cast=float, name='var1')
print(evargs.get('var1'))
```

### b. Put the value & Get the value

Putting the value, and get the value. The value is processed by rules, therefore it is not a simple setting.

```
evargs.initialize({
  'a': {'cast': int, validation='unsigned'},
  'b': {'cast': float, 'validation': ('range', 1, 10)}
});
  
evargs.put('a', 1)
evargs.put_values({...})

a = evargs.get('a')
```

### c. Parse the expression & Get the value [ExpEvArgs]

Parsing the expression, and get the value. This feature provides for dynamic value assign.

```
[Expression]
evargs.parse('a = 1;')

[Get]
a = evargs.get('a')
```

### d. Parse the expression & Evaluate [ExpEvArgs]

Parsing the expression, and evaluate the value. This feature provides for dynamic value assign and value evaluation.

```
[Expression]
evargs.parse('a >= 1; a<=10')

[Evaluate]
evargs.evaluate('a', 4) --> True
evargs.evaluate('a', 100) --> False
```

## Primary methods of EvArgs

| **Method**            | **Description**                                                                | **Doc/Code**                                                                                      |
|-----------------------|--------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------|
| `initialize`          | Initializes rules, default rule, and set options.                            | [doc](https://deer-hunt.github.io/evargs/modules/evargs.html#evargs.EvArgs.initialize) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_general.py) |
| `set_options`         | Set options.                                                                   | [doc](https://deer-hunt.github.io/evargs/modules/evargs.html#evargs.EvArgs.set_options) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_options.py) |
| `set_default_rule`    | Set the default rule.                                                          | [doc](https://deer-hunt.github.io/evargs/modules/evargs.html#evargs.EvArgs.set_default_rule) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_general.py) |
| `create_rule`         | Create rule by arguments. The default value is reflected.                     | [doc](https://deer-hunt.github.io/evargs/modules/evargs.html#evargs.EvArgs.create_rule) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_general.py) |
| `set_rule`            | Set a rule.                                                                    | [doc](https://deer-hunt.github.io/evargs/modules/evargs.html#evargs.EvArgs.set_rule) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_general.py) |
| `set_rules`           | Set the rules.                                                                 | [doc](https://deer-hunt.github.io/evargs/modules/evargs.html#evargs.EvArgs.set_rules) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_general.py) |
| `assign`              | Assign a value. If specifying `name`, the value is stored.                   | [doc](https://deer-hunt.github.io/evargs/modules/evargs.html#evargs.EvArgs.assign) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_assign.py) |
| `assign_values`       | Assign the values.                                                            | [doc](https://deer-hunt.github.io/evargs/modules/evargs.html#evargs.EvArgs.assign_values) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_assign.py) |
| `get_rule`            | Get the rule by each argument.                                                | [doc](https://deer-hunt.github.io/evargs/modules/evargs.html#evargs.EvArgs.get_rule) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_general.py) |
| `get_rule_options`    | Get the rule's option values.                                                | [doc](https://deer-hunt.github.io/evargs/modules/evargs.html#evargs.EvArgs.get_rule_options) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_general.py) |
| `get`                 | Get the value of a parameter by name and index.                              | [doc](https://deer-hunt.github.io/evargs/modules/evargs.html#evargs.EvArgs.get) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_get_put.py) |
| `get_values`          | Get the values of parameters.                                                | [doc](https://deer-hunt.github.io/evargs/modules/evargs.html#evargs.EvArgs.get_values) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_get_put.py) |
| `put`                 | Put the value.                                                               | [doc](https://deer-hunt.github.io/evargs/modules/evargs.html#evargs.EvArgs.put) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_get_put.py) |
| `put_values`          | Put the values of parameters.                                               | [doc](https://deer-hunt.github.io/evargs/modules/evargs.html#evargs.EvArgs.put_values) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_get_put.py) |
| `make_help`          | Make parameter's description. Refer to `Make help`.                        | [doc](https://deer-hunt.github.io/evargs/modules/evargs.html#evargs.EvArgs.make_help) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_show_help.py) |
| Other methods         | `has_param`, `get_param`, `get_size`, `delete`, `reset` ...               | [doc](https://deer-hunt.github.io/evargs/modules/evargs.html) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/) |

**ExpEvArgs**

| **Method**        | **Description**                                                                 | **Doc/Code** |
|------------------------|--------------------------------------------------------------------------------------|-----------------|
| `parse`                | Parse the expression based on rule option. e.g. `a=1; b>5; c=>1;c<10;`                    | [doc](https://deer-hunt.github.io/evargs/modules/evargs.html#evargs.ExpEvArgs.parse) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_exp_general.py) |
| `evaluate`            | Evaluate a parameter. Using `evaluate` after executing `parse`.                           | [doc](https://deer-hunt.github.io/evargs/modules/evargs.html#evargs.ExpEvArgs.evaluate) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_exp_evaluate.py) |

**Related**

- [EvArgs class's doc](https://deer-hunt.github.io/evargs/modules/evargs.html#evargs.EvArgs)
- [ExpEvArgs class's doc](https://deer-hunt.github.io/evargs/modules/evargs.html#evargs.ExpEvArgs)


## Rule options

The following are the rule options.

| Option name       | Type                         | Default       | Description                                                                                     | Code                                                                                     |
|--------------------|------------------------------|---------------|-------------------------------------------------------------------------------------------------|-----------------|
| `cast`            | `str`, `callable`           | `None`        | Cast-type (e.g., `int`, `str`, `bool`, `float`, `Enum class`, ...). Refer to `Type cast`.       | [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_cast.py) |
| `required`        | `bool`                      | `False`       | Whether the parameter is required.                                                               | [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_required_default.py) |
| `default`         | `any`                       | `None`        | Set the default value if the value is not provided.                                             | [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_required_default.py) |
| `nullable`         | `bool`                       | `True`        | Allow `None` value. Also, when casting to `int` or `float`, an empty string value is converted to `None`. | [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_assign.py) |
| `trim`            | `bool`, `str`               | `None`        | Trim the value if it is enabled. bool or str value for trim process.                           | [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_assign.py) |
| `validation`      | `str`, `tuple`, `list`, `callable` | `None`        | Validation name, list of arguments, or a custom validation method. And it's possible to specify multiple validations with tuple. Refer to `Value validation`. | [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_validation.py) |
| `choices`         | `list`, `tuple`, `Enum class` | `None`        | Restrict the value to predefined values.                                                   | [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_choices.py) |
| `pre_cast`        | `callable`                  | `None`        | Pre-casting method for the value.                                                               | [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_pre_post.py) |
| `post_cast`       | `callable`                  | `None`        | Post-casting method for the value.                                                              | [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_pre_post.py) |
| `pre_apply`       | `callable`                  | `None`        | Pre-processing method for the parameter before applying.                                       | [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_pre_post.py) |
| `post_apply`      | `callable`, `str`, `tuple`, `list`  | `None`        | Post-processing method for the parameter after applying. Validation method can also be specified. And it's possible to specify multiple regulations with tuple. | [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_pre_post.py) |
| `raise_error`     | `int [0, 1, 2]`            | `1`           | Raise an error during casting.<br> `0: Cancel error`<br> `1: Raise error if default is none`<br> `2: Raise all error `    | [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_error.py) |
| `list`            | `bool`                      | `False`       | The value is list value if it is enabled.                                                      | [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_assign.py) |
| `multiple`        | `bool`                      | `False`       | Allow multiple values.                                                                           | [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_multiple.py) |
| `help`            | `str`, `tuple/list`         | `None`        | Description for the value.                                                                       | [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_show_help.py) |

> There is also a description about `The order of value processing` in a later section.

**ExpEvArgs**

| Option name       | Type                         | Default       | Description                                                                                     | Code                |
|--------------------|------------------------------|---------------|-------------------------------------------------------------------------------------------------|-----------------|
| `evaluation`        | `callable`                  | `None`        | Evaluation method for the value.                                                                   | [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_exp_evaluate.py) |
| `evaluation_apply`  | `callable`               | `None`        | Evaluation method for the parameter.                                                           | [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_exp_multiple.py) |
| `allowed_operator`   | `int`                  | `-1`        | Set allowed operators using a bitmask value. `-1` is all operators. e.g. `Operator.EQUAL│Operator.GREATER` Related: [Operator class](https://deer-hunt.github.io/evargs/modules/modules.html#evargs.Operator)           | [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_exp_evaluate.py) |
| `multiple_or`     | `bool`                      | `False`        | Whether to use logical OR for multiple condition values.                                       | [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_exp_multiple.py) |
| `list_or`         | `bool`                      | `None`        | Whether to use logical OR for list values. Adjusts automatically by operator if the value is None. | [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_exp_evaluate.py) |

**Example**

```
evargs.assign(v, cast=str, list=True)
evargs.assign(v, cast=int, multiple=True)
evargs.assign(v, pre_cast=lambda v: v.upper())
```

```
evargs.initialize({
  'a': {'cast': str, 'list': True},
  'b': {'cast': int, 'multiple': True},
  'c': {'pre_cast': lambda v: v.upper()},
})
```

```
evargs.set_rules({
  'a': {'cast': str, 'list': True},
  'b': {'cast': int, 'multiple': True},
  'c': {'pre_cast': lambda v: v.upper()},
})
```

## Type cast

| **Type cast**         | **Description**                                                                   | **Doc/Code** |
|-------------------|-------------------------------------------------------------------------|-----------------|
| `int`, `'int'`               | Casting to int.                                | [doc](https://deer-hunt.github.io/evargs/modules/type-cast.html#evargs.TypeCast.to_int) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_type_cast.py) |
| `'round_int'`               | Casting to int with round.                | [doc](https://deer-hunt.github.io/evargs/modules/type-cast.html#evargs.TypeCast.to_round_int) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_type_cast.py) |
| `float`, `'float'`           | Casting to float.                              | [doc](https://deer-hunt.github.io/evargs/modules/type-cast.html#evargs.TypeCast.to_float) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_type_cast.py) |
| `complex`, `'complex'`        | Casting to complex.               | [doc](https://deer-hunt.github.io/evargs/modules/type-cast.html#evargs.TypeCast.to_complex) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_type_cast.py) |
| `bool`, `'bool'`           | Casting to bool.                              | [doc](https://deer-hunt.github.io/evargs/modules/type-cast.html#evargs.TypeCast.to_bool) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_type_cast.py) |
| `'bool_strict'`    | Casting to bool strictly.                           | [doc](https://deer-hunt.github.io/evargs/modules/type-cast.html#evargs.TypeCast.bool_strict) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_type_cast.py) |
| `'bool_loose'`    | Casting to bool loosely.                           | [doc](https://deer-hunt.github.io/evargs/modules/type-cast.html#evargs.TypeCast.bool_loose) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_type_cast.py) |
| `str`, `'str'`    | Casting to str.                                                                                    | [doc](https://deer-hunt.github.io/evargs/modules/type-cast.html#evargs.TypeCast.to_str) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_type_cast.py) |
| `Enum class`    | Casting to Enum class.                            | [doc](https://deer-hunt.github.io/evargs/modules/type-cast.html#evargs.TypeCast.to_enum) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_cast_enum.py) |
| `('enum', Enum class)`    | Casting to Enum class by Enum's name or Enum's value.           | [doc](https://deer-hunt.github.io/evargs/modules/type-cast.html#evargs.TypeCast.to_enum) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_cast_enum.py) |
| `('enum_value', Enum class)`    | Casting to Enum class by Enum's value.                          | [doc](https://deer-hunt.github.io/evargs/modules/type-cast.html#evargs.TypeCast.to_enum) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_cast_enum.py) |
| `('enum_name', Enum class)`    | Casting to Enum class by Enum's name.                         | [doc](https://deer-hunt.github.io/evargs/modules/type-cast.html#evargs.TypeCast.to_enum) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_cast_enum.py) |
| `'raw'`            | The casting process is not be executed.                                                  | - |
| `callable`       | Custom callable function for casting. e.g. `lambda v: v.upper()`                    | - |

**Related**

- [test_rule_cast.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_cast.py)
- [test_rule_cast_enum.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_cast_enum.py)
- [TypeCast class](https://deer-hunt.github.io/evargs/modules/type-cast.html)


## Value validation

In the value validation, `required` option is available to checking for the value existence and `choices` option is available to restricting the value. Additionally, you can use the following validation rules or custom function in `validation` option.

**Validations**

| **Name**          | **Value Type**       | **Description**                                                                                     | **Doc/Code**                                                                                              |
|-------------------|----------------------|-----------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------|
| `exist`           | `any`                | The value is exist.                                                                                 | [doc](https://deer-hunt.github.io/evargs/modules/validator.html#evargs.Validator.validate_exist) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_validation.py) |
| `size`            | `any`                | The value length is exactly `size`.                                                                  | [doc](https://deer-hunt.github.io/evargs/modules/validator.html#evargs.Validator.validate_size) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_validation.py) |
| `sizes`           | `any`                | The value length is sizes `min_size` and `max_size`.                                               | [doc](https://deer-hunt.github.io/evargs/modules/validator.html#evargs.Validator.validate_sizes) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_validation.py) |
| `enum`             | `any`                | The value is enum class's value.                                                                          | [doc](https://deer-hunt.github.io/evargs/modules/validator.html#evargs.Validator.validate_enum) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_validation.py) |
| `alphabet`        | `str`                | Alphabetic characters.                                                                                | [doc](https://deer-hunt.github.io/evargs/modules/validator.html#evargs.Validator.validate_alphabet) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_validation.py) |
| `alphanumeric`    | `str`                | Alphanumeric characters.                                                                              | [doc](https://deer-hunt.github.io/evargs/modules/validator.html#evargs.Validator.validate_alphanumeric) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_validation.py) |
| `ascii`           | `str`                | ASCII characters.                                                                                     | [doc](https://deer-hunt.github.io/evargs/modules/validator.html#evargs.Validator.validate_ascii) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_validation.py) |
| `printable_ascii` | `str`                | Printable ASCII characters.                                                                            | [doc](https://deer-hunt.github.io/evargs/modules/validator.html#evargs.Validator.validate_printable_ascii) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_validation.py) |
| `standard_ascii`  | `str`                | Standard ASCII characters.                                                                             | [doc](https://deer-hunt.github.io/evargs/modules/validator.html#evargs.Validator.validate_standard_ascii) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_validation.py) |
| `char_numeric`    | `str`                | Numeric characters.                                                                                    | [doc](https://deer-hunt.github.io/evargs/modules/validator.html#evargs.Validator.validate_char_numeric) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_validation.py) |
| `regex`           | `str`                | The string matches the regular expression.                                                            | [doc](https://deer-hunt.github.io/evargs/modules/validator.html#evargs.Validator.validate_regex) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_validation.py) |
| `range`           | `int`, `float`      | The numeric value is within range `min_v` to `max_v`.                                               | [doc](https://deer-hunt.github.io/evargs/modules/validator.html#evargs.Validator.validate_range) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_validation.py) |
| `unsigned`        | `int`, `float`      | Unsigned number.                                                                                     | [doc](https://deer-hunt.github.io/evargs/modules/validator.html#evargs.Validator.validate_unsigned) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_validation.py) |
| `positive`        | `int`, `float`      | Positive number.                                                                                     | [doc](https://deer-hunt.github.io/evargs/modules/validator.html#evargs.Validator.validate_positive) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_validation.py) |
| `negative`        | `int`, `float`      | Negative number.                                                                                     | [doc](https://deer-hunt.github.io/evargs/modules/validator.html#evargs.Validator.validate_negative) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_validation.py) |
| `even`            | `int`                | Even int.                                                                                            | [doc](https://deer-hunt.github.io/evargs/modules/validator.html#evargs.Validator.validate_even) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_validation.py) |
| `odd`             | `int`                | Odd int.                                                                                             | [doc](https://deer-hunt.github.io/evargs/modules/validator.html#evargs.Validator.validate_odd) / [code](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_validation.py) |

**Format of `validation` and `post_apply`**

```
# Single validation
'validation': 'validation_name'  # No parameter - str
'validation': function  # callable
'validation': ('validation_name', param1, param2...) - tuple
'validation': ['validation_name', param1, param2...] - list

# Multiple validations
'validation': [('validation_name',), ('validation_name', 4)] - list -> tuple, tuple
'validation': [tuple(['validation_name']), ('validation_name', 4), function] - list -> tuple, tuple, callable
```

**e.g.**

```
evargs.assign(v, cast=int, choices=[1, 2, 3])
evargs.assign(v, cast=int, choices=EnumClass)
```

```
evargs.assign(v, cast=str, validation=('size', 3))
evargs.assign(v, cast=str, validation=('sizes', 4, 10))
evargs.assign(v, cast=str, validation='alphabet')
evargs.assign(v, cast=int, validation=('range', None, 100))
evargs.assign(v, cast=str, validation=('regex', r'^ABC\d+XYZ$', re.I))
evargs.assign(v, cast=int, validation=lambda n, v: True if v >= 0 else False)
evargs.assign(v, cast=str, validation=[('size', 4), ('alphabet',)])

# Validation in post_apply
evargs.assign(['1', '2', '3'], cast=int, list=True, post_apply='exist')
```

**Related**

- [test_rule_validation.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_validation.py)
- [Validator class](https://deer-hunt.github.io/evargs/modules/validator.html)


## The order of value processing

This is description of the order of value processing, internal specification.

1. `pre_apply` : Pre applying. Processing to whole value.
2. `trim` : Trim if the value is str.
3. `pre_cast` : Pre casting.
4. `cast` : Casting.
5. `post_cast` : Post casting.
6. `required` : Validating the value exists.
7. `validation` : Validation.
8. `choices` : Validating choices.
9. `post_apply` : Post applying. This is last phase. It's possible for validation and value modification..

> If "list" mode is enabled in the rule options, processing for "each value" in [trim - choices].


## Description of options

### `flexible=True`

It can be operated even if the rule is not defined.

e.g. specifying `flexible=True` and `default_rule={...}`. 

### `required_all=True`

All parameters defined in rules must have values assigned. The behavior is equivalent to specifying 'required=True' for each rule.

### `ignore_unknown=True`

Ignoring and excluding the unknown parameter. The error does not occur if the unknown parameter is assigned.

### `default_rule={...}`

Default rule for all parameters. e.g. `{'cast': int, 'default': -1}`


## Make help

`make_help` method can make parameter's description. `get_help_formatter` method provide some displaying features.

**e.g.**

```
desc = evargs.make_help()

 Name              | * | e.g.    | Validation | Description                           
---------------------------------------------------------------------------------------
 planet_name       | Y | Jupiter |            | Name of the planet.                   
 distance_from_sun | N |         | unsigned   | Distance from the Sun in kilometers.  
 diameter          | N | 6779    | customize  | Diameter of the planet in kilometers. 
 has_water         | N | 1       |            | Indicates if the planet has water.    
 surface_color     | N | Black   |            | Main color of the surface.            
```

```
help_formatter = evargs.get_help_formatter()

help_formatter.set_columns({
  'name': 'Name',
  'required': '*',
  'cast': 'Type cast',
  'help': 'Desc'
})
```

Also `ListFormatter` class can also be used independently to adjust and display dict and list data. The example is [here](https://github.com/deer-hunt/evargs/tree/main/examples/show_list_data.py).

```
# python3 show_list_data.py 

 Compound Name  | Elements                                           | Molecular Formula | Melting Point | Uses          
--------------------------------------------------------------------------------------------------------------------------
 Aspirin        | Carbon (C), Hydrogen (H), Oxygen (O)               | C9H8O4            | 135°C         | Pain reliever 
 Glucose        | Carbon (C), Hydrogen (H), Oxygen (O)               | C6H12O6           | 146°C         | Energy source 
 Acetaminophen  | Carbon (C), Hydrogen (H), Nitrogen (N), Oxygen (O) | C8H9NO            | 169-172°C     | Pain reliever 
 Niacin         | Carbon (C), Hydrogen (H), Nitrogen (N)             | C6H5NO2           | 234-236°C     | Nutrient      
 Salicylic Acid | Carbon (C), Hydrogen (H), Oxygen (O)               | C7H6O3            | 158-160°C     | Preservative  
```

**Related**

- [test_show_help.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_show_help.py)
- [show_list_data.py](https://github.com/deer-hunt/evargs/tree/main/examples/show_list_data.py)
- [ListFormatter class](https://deer-hunt.github.io/evargs/modules/list-formatter.html)



## Examples and Test code

### Examples

There are some examples in `./examples/`.

| Program Name | Description |
|--------------|-------------|
| [basic.py](https://github.com/deer-hunt/evargs/tree/main/examples/basic.py) | Demonstrates basic usage of `EvArgs`, including parameter initialization, parsing, and evaluation. |
| [calculate_metals.py](https://github.com/deer-hunt/evargs/tree/main/examples/calculate_metals.py) | Using`ExpEvArgs`, validation, cast, range, default. |
| [convert_chemical_cho.py](https://github.com/deer-hunt/evargs/tree/main/examples/convert_chemical_cho.py) | Convert values from `argparse.ArgumentParser`. Using trim, post_cast, choices, post_apply. |
| [rules_evaluate.py](https://github.com/deer-hunt/evargs/tree/main/examples/rules_evaluate.py) | Simple rules and evaluate examples. |
| [customize_validator.py](https://github.com/deer-hunt/evargs/tree/main/examples/customize_validator.py) |Extending `Validator` class, using `ExpEvArgs`. |
| [simple_type_cast_validator.py](https://github.com/deer-hunt/evargs/tree/main/examples/simple_type_cast_validator.py) | Simple type casting and validation without `EvArgs class`. |
| [show_help.py](https://github.com/deer-hunt/evargs/tree/main/examples/show_help.py) | Show help using`HelpFormatter` |
| [show_list_data.py](https://github.com/deer-hunt/evargs/tree/main/examples/show_list_data.py) | Display list-based parameter data using `ListDataFormatter`. |


###  Test code

There are many examples in `./tests/`.

| File | Description |
|-----------|-------------|
| [test_assign.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_assign.py) | Tests for assigning parameters and parsing values. |
| [test_general.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_general.py) | General tests for `EvArgs`. |
| [test_options.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_options.py) | Tests for options of `flexible`, `required_all`, `ignore_unknown`, and `set_options`. |
| [test_error.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_error.py) | Tests for error handling in `EvArgs`. |
| [test_exception.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_exception.py) | Tests specific exceptions raised by invalid inputs in `EvArgs`. |
| [test_get_put.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_get_put.py) | Tests for `get` and `put` methods. |
| [test_rule_validation.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_validation.py) | Tests for rule validation, including `validation`, and custom validation methods. |
| [test_rule_choices.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_validation.py) | Tests for `choices`. |
| [test_rule_cast.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_cast.py) | Tests for type handling in rules, such as `int`, `float`, `bool`, `str`, `complex`, `Enum class` and custom types. |
| [test_rule_cast_enum.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_cast_enum.py) | Tests for Enum type in rules. |
| [test_rule_required_default.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_required_default.py) | Tests for `required` and `default` options. |
| [test_rule_pre_post.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_pre_post.py) | Tests for `pre_cast` and `post_cast` for value transformations. |
| [test_rule_multiple.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_multiple.py) | Tests for `multiple` option in rules. |
| [test_exp_general.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_exp_general.py) | Tests for `ExpEvArgs` including general usages. |
| [test_exp_evaluate.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_exp_evaluate.py) | Tests for `ExpEvArgs` and including `evaluate`. |
| [test_exp_multiple.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_exp_multiple.py) | Tests for `ExpEvArgs` including `evaluate` and `multiple`. |
| [test_show_help.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_show_help.py) | Tests for showing help. |
| [test_list_formatter.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_list_formatter.py) | Tests for `HelpFormatter`, `ListFormatter` class. |
| [test_type_cast.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_type_cast.py) | Tests for `TypeCast` class. |
| [test_validator.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_validator.py) | Tests for `Validator` class. |
| [test_helper.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_helper.py) | Tests for ExpressionParser. |


## Class documentation

Class documentation's top page is [here](https://deer-hunt.github.io/evargs/py-modindex.html).

- [EvArgs class](https://deer-hunt.github.io/evargs/modules/evargs.html)
- [TypeCast class](https://deer-hunt.github.io/evargs/modules/type-cast.html)
- [Validator class](https://deer-hunt.github.io/evargs/modules/validator.html)
- [HelpFormatter class](https://deer-hunt.github.io/evargs/modules/list-formatter.html#evargs.HelpFormatter)
- [ListFormatter class](https://deer-hunt.github.io/evargs/modules/list-formatter.html#evargs.ListFormatter)
- [EvArgsException class / ValidateException class](https://deer-hunt.github.io/evargs/modules/exception.html)


## Dependencies

No dependency.


## Other OSS

- [IpSurv](https://github.com/deer-hunt/ipsurv/)
- [IpServer](https://github.com/deer-hunt/ipserver/)
