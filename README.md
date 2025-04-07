# evargs

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
"evargs" is a lightweight python module for easy expression parsing and value-casting, validating by rules, and it provide flexible configuration and custom validation method.
</div>

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

evargs.parse('a= 1 ;b=True;c=10;d=;e=H2O')

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
  'e': {'type': int, 'validate': ['range', 1, 10]}
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
- Applying Pre-processing method and Post-processing method. 
- Get assigned values.
- Set default rule.
- Other support methods for value-assignment.

## Overview

There are 3 way usages in `evargs`. The behavior of "value-casting and validation" based on `rules` is common to 3 way.

### a. Parsing expression & Evaluation

Parsing the expression, and evaluate the value.

```
Expression:
"a >= 1; a<=10"

Evaluation:
evargs.evaluate('a', 4) --> True
evargs.evaluate('a', 100) --> False
```

### b. Parsing expression & Get the value

Parsing the expression, and get the value.

```
Expression:
"a = 1;"

Get:
a = evargs.get('a')
```

### c. Putting the value & Get the value

Putting the value, and get the value. The value is processed by rules, therefore it is not a simple setting.

```
Put:
evargs.put('a', 1)

Get:
a = evargs.get('a')
```


## Rule Options

The following are the rule options.

| Option name             | Type               | Description                                                                                     |
|--------------------|--------------------|-------------------------------------------------------------------------------------------------|
| `list`            | `bool`            | Whether the parameter is a list value.                                                         |
| `multiple`        | `bool`            | Allows multiple condition values.                                                              |
| `type`            | `str`,`callable` | Set cast type (e.g., `int`, `str`, `bool`, `bool_strict`, `float`, `complex`, `str`, `expression`, `callable function`).            |
| `require`         | `bool`            | Whether the parameter is required.                                                             |
| `default`         | `any`             | Set the default value if the value is not provided.                                            |
| `choices`         | `list`            | Restrict the parameter to a set of predefined values.                                          |
| `validate`        | `str`,`list`,`callable` | Validation name, list of arguments, or a custom validation method.                            |
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
| `count_params     | -                                                                                      | Get parameter's length.                 |


## Introduction of options

### `flexible=True`

It can be operated even if the rule is not defined.

e.g. specifying `flexible=True` and `default_rule={...}`. 

### `require_all=True`

All parameters defined in rules must have values assigned. The behavior is equivalent to specifying 'required=True' for each rule.

### `ignore_unknown=True`

Ignoring and excluding the unknown parameter. The error does not occur if the unknown parameter is assigned.

### `default_rule={...}`

Default rule for all parameters. e.g. `{'type': int, 'default': -1}`


## Test code examples

There are many examples in `./tests/`.

| File | Description |
|-----------|-------------|
| [test_general.py](https://github.com/deer-hunt/evargs/blob/master/tests/test_general.py) | General tests for `EvArgs`, including flexible rules, required parameters, and error handling. |
| [test_get_put.py](https://github.com/deer-hunt/evargs/blob/master/tests/test_get_put.py) | Tests for `get` and `put` methods. |
| [test_rule_validate.py](https://github.com/deer-hunt/evargs/blob/master/tests/test_rule_validate.py) | Tests for rule validation, including `choices`, `validate`, and custom validation methods. |
| [test_rule_type.py](https://github.com/deer-hunt/evargs/blob/master/tests/test_rule_type.py) | Tests for type handling in rules, such as `int`, `float`, `bool`, `str`, `complex`, and custom types. |
| [test_rule_require_default.py](https://github.com/deer-hunt/evargs/blob/master/tests/test_rule_require_default.py) | Tests for `require` and `default` options. |
| [test_rule_pre_post.py](https://github.com/deer-hunt/evargs/blob/master/tests/test_rule_pre_post.py) | Tests for `pre_apply` and `post_apply` for value transformations. |
| [test_rule_multiple.py](https://github.com/deer-hunt/evargs/blob/master/tests/test_rule_multiple.py) | Tests for `multiple` option in rules. |
| [test_rule_evaluate.py](https://github.com/deer-hunt/evargs/blob/master/tests/test_rule_evaluate.py) | Tests for `evaluate` and `evaluate_param` options, including logical operations and custom evaluations. |
| [test_value_caster.py](https://github.com/deer-hunt/evargs/blob/master/tests/test_value_caster.py) | Tests for `ValueCaster` methods. |
| [test_validator.py](https://github.com/deer-hunt/evargs/blob/master/tests/test_validator.py) | Tests for `Validator` methods. |


## Dependencies

No dependency.


## Other OSS

- [IpSurv](https://github.com/deer-hunt/ipsurv/)
- [IpServer](https://github.com/deer-hunt/ipserver/)
