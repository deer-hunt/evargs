from enum import Enum
from typing import Type, Optional, Union, overload

from evargs.exception import EvArgsException, ValidateException
from evargs.list_formatter import HelpFormatter
from evargs.modules import ParamValue, MultipleParam
from evargs.validator import Validator
from evargs.type_cast import TypeCast

'''
EvArgs

Document:
https://github.com/deer-hunt/evargs/

Class Doc:
https://deer-hunt.github.io/evargs/modules/evargs.html

Tests:
https://github.com/deer-hunt/evargs/blob/main/tests/

Rules description:
https://github.com/deer-hunt/evargs/#rule-options
'''


class EvArgs:
    def __init__(self, validator: Validator = None):
        """Initialize instance with default settings and an optional validator."""
        self.defined_rule = {
            'cast': None, 'required': False, 'default': None, 'nullable': True, 'trim': None,
            'validation': None, 'choices': None,
            'pre_cast': None, 'post_cast': None, 'pre_apply': None, 'post_apply': None,
            'raise_error': TypeCast.ERROR_DEFAULT_NONE,
            'list': False, 'multiple': False,
            'help': None
        }

        self.rules = {}
        self.default_rule = {}
        self.params = {}

        self.flexible = False
        self.required_all = False
        self.ignore_unknown = False

        if validator is not None:
            self.validator = validator
        else:
            self.validator = self.get_validator()

        self.type_cast = self.get_type_cast()

        self.help_formatter = None

    def get_validator(self) -> Validator:
        """Return Validator instance."""
        return Validator()

    def set_validator(self, validator: Validator):
        """Set Validator instance."""
        self.validator = validator

    def get_type_cast(self) -> Type[TypeCast]:
        """Return TypeCast class."""
        return TypeCast

    def set_type_cast(self, type_cast: Type[TypeCast]):
        """Set TypeCast class."""
        self.type_cast = type_cast

    def get_help_formatter(self) -> HelpFormatter:
        """Return HelpFormatter instance."""
        if not self.help_formatter:
            self.help_formatter = HelpFormatter()

        return self.help_formatter

    def set_help_formatter(self, help_formatter: HelpFormatter):
        """Set HelpFormatter instance."""
        self.help_formatter = help_formatter

    def set_options(self, flexible: bool = False, required_all: bool = False, ignore_unknown: bool = False):
        """Set options."""
        self.flexible = flexible
        self.required_all = required_all
        self.ignore_unknown = ignore_unknown

    def set_default_rule(self, default_rule: dict):
        """Set the default rule."""
        self.default_rule = {**self.defined_rule, **default_rule}

    def initialize(self, rules: Optional[dict], default_rule: dict = None, flexible: bool = False, required_all: bool = False, ignore_unknown: bool = False):
        """Initialize rules and options for the instance."""
        if default_rule:
            self.set_default_rule(default_rule)

        self.set_options(flexible, required_all, ignore_unknown)

        if rules is not None:
            self.set_rules(rules)

        return self

    def set_rule(self, name: str, rule: dict):
        """Set rule."""
        self.rules[name] = self.create_rule(rule=rule)

        return self

    def set_rules(self, rules: dict):
        """Set rules."""
        self.rules = {}

        for name, rule in rules.items():
            self.set_rule(name, rule)

        return self

    def make_kwargs(self, args: tuple, keys: list, kwargs: dict = None):
        """Make kwargs from args."""
        rkwargs = dict(zip(keys, args))

        if kwargs is not None:
            for k, v in kwargs.items():
                rkwargs[k] = v

        return rkwargs

    @overload
    def create_rule(self, cast: Union[str, callable] = None, required: bool = False, default: any = None, nullable: bool = True, trim: Union[bool, str] = None,
                    validation: Union[str, list, tuple, callable] = None, choices: Union[list, tuple, Type[Enum]] = None, pre_cast: callable = None, post_cast: callable = None, pre_apply: callable = None, post_apply: Union[callable, str, list, tuple] = None,
                    raise_error: int = TypeCast.ERROR_DEFAULT_NONE, list: bool = False, multiple: bool = False, rule: dict = None) -> dict:
        """Create rule by arguments. The default value is reflected."""
        ...

    def create_rule(self, *args, **kwargs) -> dict:
        if len(args) > 0:
            kwargs = self.make_kwargs(args, ['cast', 'required', 'default', 'nullable', 'trim', 'validation', 'choices', 'pre_cast', 'post_cast', 'pre_apply', 'post_apply', 'raise_error', 'list', 'multiple', 'rule'], kwargs)

        default_rule = self.default_rule if len(self.default_rule) > 0 else self.defined_rule

        rule = kwargs.pop('rule', None)
        rule = rule if rule is not None else {}

        rule = {**default_rule, **rule, **kwargs}

        for k, v in rule.items():
            if k not in self.defined_rule:
                raise EvArgsException(f'Unknown rule option.({k})', EvArgsException.ERROR_GENERAL)

        return rule

    @overload
    def assign(self, value: any, cast: Union[str, callable] = None, required: bool = False, default: any = None, nullable: bool = True, trim: Union[bool, str] = None,
               validation: Union[str, list, tuple, callable] = None, choices: Union[list, tuple, Type[Enum]] = None, pre_cast: callable = None, post_cast: callable = None, pre_apply: callable = None, post_apply: callable = None,
               raise_error: int = TypeCast.ERROR_DEFAULT_NONE, list: bool = False, multiple: bool = False, rule: dict = None, name: str = None) -> any:
        """Assign value by rule options."""
        ...

    def assign(self, value: any, *args, **kwargs) -> any:
        if len(args) > 0:
            kwargs = self.make_kwargs(args, ['cast', 'required', 'default', 'nullable', 'trim', 'validation', 'choices', 'pre_cast', 'post_cast', 'pre_apply', 'post_apply', 'raise_error', 'list', 'multiple', 'rule', 'name'], kwargs)

        name = kwargs.pop('name', None)

        rule = self.create_rule(*args, **kwargs)

        v = self._apply_rule(rule, value)

        if name is not None:
            self.rules[name] = rule
            self.put(name, v)

        return v

    def assign_values(self, values: dict, rules: dict, store: bool = False) -> dict:
        """Assign values by rule options."""
        for name, rule in rules.items():
            value = values.get(name)

            store_name = name if store else None

            values[name] = self.assign(value, rule=rule, name=store_name)

        return values

    def get_rule(self, name: str = None, rule: dict = None, rules: dict = None) -> dict:
        """Get a rule."""
        if name is not None and rules is None:
            return self._get_rule(name)
        elif not rule:
            rule = rules.get(name)

        if rule is None:
            self._raise_unknown_param(name)

        return self.create_rule(rule=rule)

    def get_rule_options(self, option: str, rules: dict = None) -> dict:
        """Get the rule's option values."""
        if rules is None:
            rules = self.rules

        values = {}

        for name, rule in rules.items():
            rule = self.get_rule(rule=rule)

            values[name] = rule.get(option)

        return values

    def _get_rule(self, name: str) -> dict:
        rule = self.rules.get(name)

        if rule is None and self.flexible:
            rule = self.default_rule

        if rule is None:
            self._raise_unknown_param(name)

        return rule

    def _add_by_rule(self, rule: dict, name: str, v: any, keep_original: bool = False) -> ParamValue:
        try:
            if not keep_original:
                v = self._apply_rule(rule, v)

            param = self._build_param(name, rule)

            param.value = v

            if not rule.get('multiple'):
                self.params[name] = param
            else:
                multiple_param = self.params.get(name)

                if not multiple_param:
                    multiple_param = MultipleParam()
                    self.params[name] = multiple_param

                multiple_param.add(param)
        except (EvArgsException, ValidateException) as e:
            e.set_name(name)
            raise e
        except Exception as e:
            raise e

        return param

    def _build_param(self, name: str, rule: dict) -> ParamValue:
        return ParamValue()

    def _apply_rule(self, rule: dict, v: any) -> any:
        try:
            pre_apply = rule.get('pre_apply')

            if pre_apply:
                v = pre_apply(v)

            if not rule.get('list'):
                v = self._apply_cast_value(rule, v)
            else:
                v = v if v is not None else []
                v = list(map(lambda t: self._apply_cast_value(rule, t), v))

            post_apply = rule.get('post_apply')

            if post_apply:
                v = self._apply_regulation(post_apply, v)
        except (EvArgsException, ValidateException) as e:
            raise e
        except Exception:
            raise EvArgsException('Error occurred in applying a rule.')

        return v

    def _apply_cast_value(self, rule: dict, v: any):
        trim = rule.get('trim')

        if trim:
            v = self._apply_trim(v, trim)

        pre_cast = rule.get('pre_cast')

        if pre_cast:
            v = pre_cast(v)

        type_cast = rule.get('cast')
        default = rule.get('default')
        nullable = rule.get('nullable', False)

        raise_error = rule.get('raise_error')

        try:
            if type_cast == int or type_cast == 'int':
                v = self.type_cast.to_int(v, default, nullable, raise_error)
            elif type_cast == float or type_cast == 'float':
                v = self.type_cast.to_float(v, default, nullable, raise_error)
            elif type_cast == complex or type_cast == 'complex':
                v = self.type_cast.to_complex(v, default, nullable, raise_error)
            elif type_cast == str or type_cast == 'str':
                v = self.type_cast.to_str(v, default, nullable, raise_error)
            elif type_cast == bool or type_cast == 'bool':
                v = self.type_cast.to_bool(v, default, nullable, raise_error)
            elif type_cast == 'bool_strict':
                v = self.type_cast.bool_strict(v, default, nullable, raise_error)
            elif type_cast == 'bool_loose':
                v = self.type_cast.bool_loose(v, default)
            elif type_cast == 'round_int':
                v = self.type_cast.to_round_int(v, default, nullable, raise_error)
            elif isinstance(type_cast, Enum.__class__):
                v = self._apply_cast_item(v, 'enum', [type_cast], default, nullable, raise_error)
            elif isinstance(type_cast, tuple):
                v = self._apply_cast_item(v, type_cast[0], type_cast[1:], default, nullable, raise_error)
            elif callable(type_cast):
                v = self.type_cast.noop(type_cast(v), default, nullable, raise_error)
            else:  # raw
                v = self.type_cast.noop(v, default, nullable, raise_error)
        except ValueError as e:
            if raise_error:
                raise ValidateException(str(e), ValidateException.ERROR_CAST)
            else:
                v = None

        post_cast = rule.get('post_cast')

        if post_cast:
            v = post_cast(v)

        if TypeCast.is_empty(v):
            if rule.get('required') or self.required_all:
                raise ValidateException('Require parameter.', ValidateException.ERROR_REQUIRED)

        if v is not None:
            self._validate(rule, v)

        return v

    def _apply_trim(self, v: any, trim: Union[str, bool]):
        if isinstance(v, str):
            t = trim if trim is not True else ' '

            v = v.strip(t)

        return v

    def _apply_cast_item(self, v: any, cmd: str, args: list, default: any, nullable: bool, raise_error: int):
        if cmd == 'enum':
            v = self.type_cast.to_enum_loose(args[0], v, is_value=True, is_name=True, default=default, nullable=nullable, raise_error=raise_error)
        elif cmd == 'enum_value':
            v = self.type_cast.to_enum_loose(args[0], v, is_value=True, is_name=False, default=default, nullable=nullable, raise_error=raise_error)
        elif cmd == 'enum_name':
            v = self.type_cast.to_enum_loose(args[0], v, is_value=False, is_name=True, default=default, nullable=nullable, raise_error=raise_error)
        else:
            raise ValueError('Unknown type cast.')

        return v

    def _validate(self, rule: dict, value: any):
        validation = rule.get('validation')

        if validation:
            self._apply_validation(validation, value)

        choices = rule.get('choices')

        if choices:
            self._validate_choices(choices, value)

    def _apply_validation(self, validation: Union[str, list, tuple, callable], v: any):
        args = []

        try:
            if isinstance(validation, (list, tuple)) and isinstance(validation[0], str):
                [validation, *args] = validation

            if isinstance(validation, str):
                self._validate_exec(validation, v, args)
            elif isinstance(validation, list):
                for w in validation:
                    self._apply_validation(w, v)
            elif callable(validation):
                success = validation(v, *args)

                if not success:
                    self.validator.raise_error('Validation error.', v)
        except ValidateException as e:
            raise e
        except Exception:
            self.validator.raise_error('Validation process error.', v, ValidateException.ERROR_PROCESS)

    def _apply_regulation(self, regulation: Union[str, list, tuple, callable], v: any) -> any:
        args = []

        try:
            if isinstance(regulation, (list, tuple)) and isinstance(regulation[0], str):
                [regulation, *args] = regulation

            if isinstance(regulation, str):
                self._validate_exec(regulation, v, args)
            elif isinstance(regulation, list):
                for w in regulation:
                    v = self._apply_regulation(w, v)
            elif callable(regulation):
                v = regulation(v, *args)
        except ValidateException as e:
            raise e
        except Exception:
            raise EvArgsException('Process error.', EvArgsException.ERROR_PROCESS)

        return v

    def _validate_exec(self, validation: str, v: any, args: list):
        fn = getattr(self.validator, 'validate_' + validation, None)

        if not fn:
            raise EvArgsException(f'Validation method is not found.({validation})', EvArgsException.ERROR_PROCESS)

        fn(v, *args)

    def _validate_choices(self, choices: any, value: any):
        if not isinstance(choices, Enum.__class__):
            if value not in choices:
                self.validator.raise_error('Out of choices.', value, ValidateException.ERROR_OUT_CHOICES)
        else:
            self.validator.validate_enum(value, choices)

    def get(self, name: str, index: int = -1) -> any:
        """Get a parameter value by name and index."""
        rule = self._get_rule(name)

        if rule is None:
            return None

        param = self.get_param(name)

        if param is None:
            param = self._add_by_rule(rule, name, None)

        if isinstance(param, MultipleParam):
            if index < 0:
                return param.get_values()

            return param.get(index).value

        return param.value

    def get_values(self) -> dict:
        """Get a dict of values."""
        values = {}

        for name in self.params:
            values[name] = self.get(name)

        return values

    def put(self, name: str, value: any, multiple_reset: bool = False, keep_original: bool = False):
        """Add or update a parameter value."""
        if multiple_reset:
            self.delete(name)

        rule = self._get_rule(name)

        if rule is not None:
            self._add_by_rule(rule, name, value, keep_original)

    def put_values(self, values: dict, multiple_reset: bool = False, keep_original: bool = False):
        """Add or update parameter values."""
        for name, value in values.items():
            self.put(name, value, multiple_reset, keep_original)

    def has_param(self, name: str) -> bool:
        """Check if a parameter with the given name exists."""
        return (name in self.params)

    def get_param(self, name: str) -> Union[ParamValue, MultipleParam]:
        """Get a parameter by name."""
        param = self.params.get(name)

        rule = self._get_rule(name)

        if rule is not None and param is None and self.flexible:
            param = self._add_by_rule(rule, name, None)

        return param

    def get_params(self) -> dict:
        """Get the parameters."""
        return self.params

    def get_size(self) -> int:
        """Get the number of parameters."""
        return len(self.params)

    def delete(self, name: str):
        """Delete a parameter value."""
        del self.params[name]

    def reset(self):
        """Delete all parameter values."""
        self.params = {}

    def make_help(self, params: list = None, append_example: bool = False, skip_headers: bool = False) -> str:
        """Make a formatted help message based on rules."""
        help_formatter = self.get_help_formatter()

        if append_example:
            help_formatter.enable_example()

        return help_formatter.make(self.rules, params, skip_headers)

    def _raise_unknown_param(self, name: str):
        if not self.ignore_unknown:
            name = name if name is not None else '-'

            raise ValidateException(f'Unknown parameter.({name})', ValidateException.ERROR_UNKNOWN_PARAM)
