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
<img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/deer-hunt/evargs">
<a href="https://pypi.org/project/evargs"><img alt="Supported Versions" src="https://img.shields.io/pypi/pyversions/evargs.svg"></a>

</div>

<div>
"EvArgs" is a lightweight python module for easy expression parsing and value-casting, validating by rules, and it provides flexible configuration and custom validation method.
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


## Usage

**Basic**

```
from evargs import EvArgs

evargs = EvArgs()

evargs.initialize({
  'a': {'type': bool},
  'b': {'type': 'bool'},  # 'bool' = bool
  'c': {'type': int},
  'd': {'type': float, 'default': 3.14},
  'e': {'type': str}
}) 

evargs.parse('a=1;b=True;c=10;d=;e=H2O')

print(evargs.get('a'), evargs.evaluate('a', True))
print(evargs.get('b'), evargs.evaluate('b', True))
print(evargs.get('c'), evargs.evaluate('c', 10))
print(evargs.get('d'), evargs.evaluate('d', 3.14))
print(evargs.get('e'), evargs.evaluate('e', 'H2O'))


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
  'a': {'type': int, 'list': True},
  'b': {'type': int, 'multiple': True},
  'c': {'type': lambda v: v.upper()},
  'd': {'type': lambda v: v.upper(), 'post_apply_param': lambda vals: '-'.join(vals)},
  'e': {'type': int, 'validation': ['range', 1, 10]}
})

evargs.parse('a=25,80,443; b>= 1; b<6; c=tcp; d=X,Y,z ;e=5;')

print(print(evargs.get_values())

Result:
--
{'a': [25, 80, 443], 'b': [1, 6], 'c': 'TCP', 'd': 'X-Y-Z', 'e': 5}
```


## Features

- It can specify the condition or value-assignment using a simple expression. e.g. `a=1;b>5`
- Evaluate assigned values. e.g `evargs.evaluate('a', 1)`
- Put values. It's available to using `put` is without parsing the expression.
- Value casting - str, int, float, complex...
- Value validation - unsigned, number range, alphabet, regex, any other...
- Applying multiple validations.
- Applying Pre-processing method and Post-processing method. 
- Get assigned values.
- Set default rule.
- Make parameter's description.
- Other support methods for value-assignment.


## Overview

There are 3 way usages in `EvArgs`. The behavior of "value-casting and validation" based on `rules` is common to 3 way.

### a. Parsing expression & Evaluation

Parsing the expression, and evaluate the value.

```
[Expression]
"a >= 1; a<=10"

[Evaluation]
evargs.evaluate('a', 4) --> True
evargs.evaluate('a', 100) --> False
```

### b. Parsing expression & Get the value

Parsing the expression, and get the value.

```
[Expression]
"a = 1;"

[Get]
a = evargs.get('a')
```

### c. Putting the value & Get the value

Putting the value, and get the value. The value is processed by rules, therefore it is not a simple setting.

```
[Put]
evargs.put('a', 1)

[Get]
a = evargs.get('a')
```


## Rules

The following are the rule options.

| Option name             | Type               | Description                                                                                     |
|--------------------|--------------------|-------------------------------------------------------------------------------------------------|
| `list`            | `bool`            | Whether the parameter is a list value.                                                         |
| `multiple`        | `bool`            | Allows multiple condition values.                                                              |
| `type`            | `str`,`callable` | Set cast type (e.g., `int`, `str`, `bool`, `bool_strict`, `float`, ...). Refer to `Value casting`.            |
| `require`         | `bool`            | Whether the parameter is required.                                                             |
| `default`         | `any`             | Set the default value if the value is not provided.                                            |
| `choices`         | `list`            | Restrict the parameter to a set of predefined values.                                          |
| `validation`        | `str`,`list`,`callable` | Validation name, list of arguments, or a custom validation method. It also available for multiple validations.  Refer to `Value Validation`.                            |
| `pre_apply`       | `callable`        | Pre-processing method for the value before applying.                                   |
| `post_apply`      | `callable`        | Post-processing method for the value after applying.                                   |
| `pre_apply_param` | `callable`        | Pre-processing method for the parameter before applying.                                |
| `post_apply_param`| `callable`        | Post-processing method for the parameter after applying.                                |
| `evaluate`        | `callable`        | Evaluation method for the value.                                                      |
| `evaluate_param`  | `callable`        | Evaluation method for the parameter.                                                   |
| `multiple_or`  | `bool`            | Whether to use logical OR for multiple condition values.                                       |
| `list_or`      | `bool`            | Whether to use logical OR for list values. Adjusts automatically by operator if the value is None. |
| `prevent_error`   | `bool`            | Prevent errors during processing.                                                              |

**Example**

```
evargs.initialize({
  'a': {'type': str, 'list': True},
  'b': {'type': int, 'multiple': True},
  'c': {'pre_apply': lambda v: v.upper()},
})
```

```
evargs.set_rules({
  'a': {'type': str, 'list': True},
  'b': {'type': int, 'multiple': True},
  'c': {'pre_apply': lambda v: v.upper()},
})
```

## Value Casting

| **Type**         | **Description**                                                                   |
|-------------------|-------------------------------------------------------------------------|
| `int`, int            | Casting to int.                                   |
| `float`, float          | Casting to float.                              |
| `bool`, bool           | Casting to bool.                             |
| `bool_strict`    | Casting to bool or None.                        |
| `complex`, `"complex"`        | Casting to complex.          |
|  `str`, `'str'`    | Casting to str.                                                                        |
| `expression`     | Evaluating mathematical expressions. e.g., `2 * (3 + 4)`.            |
| `raw`            | The casting process is not be executed.                                        |
| `callable`       | Custom callable function for casting. e.g. lambda v: v.upper()        |

**Related**

- [test_rule_type.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_type.py)
- [ValueCaster class](https://deer-hunt.github.io/evargs/modules/value-helper.html#evargs.value_caster.ValueCaster)


## Value Validation

In the value validation, `require` option is available to checking for the value existence and `choices` option is available to restricting the value. Additionally, you can use the following validation rules or custom function in `validation` option.

**Validations**

| **name**    | **Value Type**       | **Arguments**                                                                                     | **Description**                                                                                     |
|-------------------------|----------------------|--------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|
| `size`         | `str`               | `size: int`                                                                   | The string length is exactly `size`.                                                       |
| `between`      | `str`               | `min_size: int, max_size: int`                                     | The string length is between `min_size` and `max_size`.                                     |
| `alphabet`     | `str`               | -                                                                             | Alphabetic characters.                                             |
| `alphanumeric` | `str`               | -                                                                             | Alphanumeric characters.                                           |
| `ascii`        | `str`               | -                                                                             　　| ASCII characters.                                                  |
| `printable_ascii` | `str`            | -                                                                             | Printable ASCII characters.                                        |
| `standard_ascii` | `str`             | -                                                                             | Standard ASCII characters. |
| `char_numeric` | `str`              | -                                                                             | Numeric characters.                                          |
| `regex`        | `str`               | `regex: str, [regex option]`                                             | The string matches the regular expression. |
| `range`        | `int`, `float`      | `min_v, max_v`                                                           | The numeric value is within range `min_v` to `max_v`.                                   |
| `unsigned`     | `int`, `float`      | -                                                                              | Unsigned number.                                                         |
| `even`         | `int`               | -                                                                              　　|  Even int.                                                              |
| `odd`          | `int`               | -                                                                              　　| Odd int.                                                             |

**Format**

```
# Single validation
'validation': 'validation_name'  # No parameter - str
'validation': ('validation_name', param1, param2...) - tuple
'validation': ['validation_name', param1, param2...] - list

# Multiple validation
'validation': [('validation_name',), ('validation_name', 4)] - list -> tuple, tuple
'validation': [tuple(['validation_name']), ('validation_name', 4)] - list -> tuple, tuple
```

**e.g.**

```
evargs.initialize({
  'a': {'type': str, 'validation': ['size', 3]},
  'b': {'type': str, 'validation': ['between', 4, 10]},
  'c': {'type': str, 'validation': 'alphabet'},
  'd': {'type': int, 'validation': ['range', None, 100]},
  'e': {'type': str, 'validation': ['regex', r'^ABC\d+XYZ$', re.I]},
  'f': {'type': int, 'validation': lambda n, v: True if v >= 0 else False},
  'g': {'type': str, 'validation': [('size', 4), ('alphabet',)]}
})
```

**Related**

- [test_rule_validation.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_validation.py)
- [Validator class](https://deer-hunt.github.io/evargs/modules/value-helper.html#module-evargs.validator)


## Primary methods

| **Method**       | **Arguments**                                            | **Description**                                                                 |
|------------------------|---------------------------------------------------|--------------------------------------------------------------------------------------|
| `initialize`          | `(rules, default_rule=None, flexible=False, require_all=False, ignore_unknown=False)`  | Initializes rules, default rule, and set options.                 |
| `set_options`         | `(flexible=False, require_all=False, ignore_unknown=False)`                | Set options.              |
| `set_default`         | `(default_rule=None)`                                                                      | Set the default rule.       |
| `set_rules`           | `(rules)`                                                                                   | Set the rules.                                                 |
| `set_rule`            | `(name, rule)`                                                                          | Set a rule.                                                    |
| `parse`               | `(assigns)`                                                                                   | Parse the expression.                                   |
| `evaluate`            | `(name, v)`                                                                              | Evaluate a parameter.                                  |
| `get`                 | `(name, index=-1)`                                                                     | Get the value of a parameter by name and index.        |
| `get_values`          | -                                                                                             | Get the values of parameters.                                |
| `put`                 | `(name, value, operator=Operator.EQUAL, reset=False)`                     | Put the value.                                             |
| `put_values`          | `(values, operator=Operator.EQUAL, reset=False)`                              | Put the values of parameters.                  |
| `reset`                | `(name)`                                                                                      | Reset the value.                                       |
| `reset_params`    | -                                                                                      | Reset the values of parameters.                 |
| `count_params`     | -                                                                                      | Get parameter's length.                 |
| `make_help`     | `(params=None, append_example=False, skip_headers=False)`     | Make parameter's description. `Refer to Make help`                |

**Related**

- [EvArgs class's doc](https://deer-hunt.github.io/evargs/modules/evargs.html)


## Description of options

### `flexible=True`

It can be operated even if the rule is not defined.

e.g. specifying `flexible=True` and `default_rule={...}`. 

### `require_all=True`

All parameters defined in rules must have values assigned. The behavior is equivalent to specifying 'require=True' for each rule.

### `ignore_unknown=True`

Ignoring and excluding the unknown parameter. The error does not occur if the unknown parameter is assigned.

### `default_rule={...}`

Default rule for all parameters. e.g. `{'type': int, 'default': -1}`


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
  'require': '*',
  'type': 'Type',
  'help': 'Desc'
})
```

Also `BaseHelpFormatter` class can also be used independently to adjust and display dict and list data. The example is [here](https://github.com/deer-hunt/evargs/tree/main/examples/show_list_data.py).

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

- [test_help.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_help.py)
- [show_list_data.py](https://github.com/deer-hunt/evargs/tree/main/examples/show_list_data.py)
- [HelpFormatter class](https://deer-hunt.github.io/evargs/modules/value-helper.html#module-evargs.help_formatter)



## Examples and Test code

### Examples

There are some examples in `./examples/`.

- [basic.py](https://github.com/deer-hunt/evargs/tree/main/examples/basic.py)
- [calculate_metals.py](https://github.com/deer-hunt/evargs/tree/main/examples/calculate_metals.py)
- [various_rules.py](https://github.com/deer-hunt/evargs/tree/main/examples/various_rules.py)
- [customize_validator.py](https://github.com/deer-hunt/evargs/tree/main/examples/customize_validator.py)
- [show_help.py](https://github.com/deer-hunt/evargs/tree/main/examples/show_help.py)
- [show_list_data.py](https://github.com/deer-hunt/evargs/tree/main/examples/show_list_data.py)


###  Test code

There are many examples in `./tests/`.

| File | Description |
|-----------|-------------|
| [test_general.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_general.py) | General tests for `EvArgs`. |
| [test_options.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_options.py) | Tests for options of `flexible`, `require_all`, `ignore_unknown`, and `set_options`. |
| [test_get_put.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_get_put.py) | Tests for `get` and `put` methods. |
| [test_help.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_help.py) | Tests for showing help. |
| [test_help_formatter.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_help_formatter.py) | Tests for `HelpFormatter` class. |
| [test_rule_validation.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_validation.py) | Tests for rule validation, including `choices`, `validation`, and custom validation methods. |
| [test_rule_type.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_type.py) | Tests for type handling in rules, such as `int`, `float`, `bool`, `str`, `complex`, and custom types. |
| [test_rule_require_default.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_require_default.py) | Tests for `require` and `default` options. |
| [test_rule_pre_post.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_pre_post.py) | Tests for `pre_apply` and `post_apply` for value transformations. |
| [test_rule_multiple.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_multiple.py) | Tests for `multiple` option in rules. |
| [test_rule_evaluate.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_rule_evaluate.py) | Tests for `evaluate` and `evaluate_param` options, including logical operations and custom evaluations. |
| [test_value_caster.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_value_caster.py) | Tests for `ValueCaster` class. |
| [test_validator.py](https://github.com/deer-hunt/evargs/blob/main/tests/test_validator.py) | Tests for `Validator` class. |


## Class docs

- [EvArgs class](https://deer-hunt.github.io/evargs/modules/evargs.html)
- [Validator class](https://deer-hunt.github.io/evargs/modules/value-helper.html#module-evargs.validator)
- [ValueCaster class](https://deer-hunt.github.io/evargs/modules/value-helper.html#evargs.value_caster.ValueCaster)
- [HelpFormatter class](https://deer-hunt.github.io/evargs/modules/value-helper.html#evargs.help_formatter.HelpFormatter)
- [BaseHelpFormatter class](https://deer-hunt.github.io/evargs/modules/value-helper.html#evargs.help_formatter.BaseHelpFormatter)
- [EvArgsException class / EvValidateException class](https://deer-hunt.github.io/evargs/modules/evargs.html#module-evargs.exception)


## Dependencies

No dependency.


## Other OSS

- [IpSurv](https://github.com/deer-hunt/ipsurv/)
- [IpServer](https://github.com/deer-hunt/ipserver/)
