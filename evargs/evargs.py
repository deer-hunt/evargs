import io
import re
import tokenize

from evargs.exception import EvArgsException, EvValidateException
from evargs.modules import Param, ParamItem, Operator
from evargs.validator import Validator
from evargs.value_caster import ValueCaster
from evargs.help_formatter import HelpFormatter

'''
[EvArgs]

Document:
https://github.com/deer-hunt/evargs/

Class Doc:
https://deer-hunt.github.io/evargs/modules/evargs.html

Tests:
https://github.com/deer-hunt/evargs/blob/main/tests/

Rules description:
https://github.com/deer-hunt/evargs/#rules

Example:
ev_parser = EvaluationParser({
    'a': {'type': int, 'multiple': True},
    'b': {'type': int, 'default': 2},
})

value = 'a>= 1; a<6 ; b=8; c=80,443; d=a,b; e=4.5'

ev_parser.parse(value)
'''


class EvArgs:
    RULE = {
        'help': None,
        'list': False, 'multiple': False,
        'type': None, 'require': False, 'default': None,
        'choices': None, 'validation': None,
        'pre_apply': None, 'post_apply': None,
        'pre_apply_param': None, 'post_apply_param': None,
        'evaluate': None, 'evaluate_param': None, 'multiple_or': None, 'list_or': None,
        'prevent_error': False,
    }

    def __init__(self, validator: Validator = None):
        self.rules = {}
        self.default_rule = {}
        self.params = {}

        self.flexible = False
        self.require_all = False
        self.ignore_unknown = False

        if validator is not None:
            self.validator = validator
        else:
            self.validator = self.get_validator()

        self.value_caster = self.get_value_caster()

        self.help_formatter = None

    def get_validator(self) -> Validator:
        return Validator()

    def set_validator(self, validator: Validator):
        self.validator = validator

    def get_value_caster(self) -> type:
        return ValueCaster

    def set_value_caster(self, value_caster: type):
        self.value_caster = value_caster

    def get_help_formatter(self) -> HelpFormatter:
        if not self.help_formatter:
            self.help_formatter = HelpFormatter()

        return self.help_formatter

    def set_help_formatter(self, help_formatter: HelpFormatter):
        self.help_formatter = help_formatter

    def initialize(self, rules: dict, default_rule: dict = None, flexible: bool = False, require_all: bool = False, ignore_unknown: bool = False):
        self.set_default(default_rule)

        self.set_options(flexible, require_all, ignore_unknown)

        self.set_rules(rules)

        return self

    def set_options(self, flexible: bool = False, require_all: bool = False, ignore_unknown: bool = False):
        self.flexible = flexible
        self.require_all = require_all
        self.ignore_unknown = ignore_unknown

    def set_default(self, default_rule: dict = None):
        self.default_rule = default_rule

    def set_rules(self, rules: dict):
        self.rules = {}

        for name, rule in rules.items():
            self.set_rule(name, rule)

        return self

    def set_rule(self, name: str, rule: dict):
        if self.default_rule is None:
            self.rules[name] = rule
        else:
            item = self.default_rule.copy()
            item.update(rule)
            self.rules[name] = item

        for key in rule:
            if key not in self.RULE:
                raise EvArgsException('Unknown rule option.({})'.format(key), EvArgsException.ERROR_GENERAL)

        return self

    def parse(self, assigns: str):
        self.reset_params()

        readline = io.StringIO(assigns).readline
        tokens = tokenize.generate_tokens(readline)

        name = None
        operator = 0
        values = []
        value_list = False

        for tok in tokens:
            if tok.type == tokenize.NAME:
                if name is None:
                    name = tok.string
                else:
                    values.append(tok.string)
            elif tok.type == tokenize.OP:
                if Operator.is_evaluate(tok.string):
                    if operator == 0:
                        operator = Operator.parse_operator(tok.string)
                    else:
                        self._raise_parse_error('Illegal operator; {}'.format(name))
                elif tok.string == Operator.LIST_SPLIT:
                    value_list = True
                elif tok.string == Operator.VALUE_SPLIT:
                    self._add_param(name, operator, values, value_list)
                    name = None
                    operator = 0
                    values = []
                    value_list = False
                else:
                    values.append(tok.string)
            elif tok.type == tokenize.NUMBER:
                values.append(tok.string)
            elif tok.type == tokenize.STRING:
                m = re.search(r'^["\'](.+)["\']$', tok.string)

                v = tok.string if m is None else m.group(1)

                values.append(v)
            elif tok.type == tokenize.NEWLINE or tok.type == tokenize.ENDMARKER:
                continue

        if name and operator:
            self._add_param(name, operator, values, value_list)
            name = None
            operator = 0

        if name or operator:
            self._raise_parse_error('End expression')

        self._parse_not_assigned()

    def _parse_not_assigned(self):
        for name in self.rules.keys():
            rule = self.get_rule(name)

            param = self.params.get(name)

            if param is None and rule is not None:
                self._add_param_by_rule(rule, name, None, [])

    def _add_param(self, name: str, operator: int, values: list, value_list: bool):
        if name is not None:
            rule = self.get_rule(name)

            if rule is not None:
                if len(values) > 0 and not value_list:
                    values = [''.join(values)]

                try:
                    self._add_param_by_rule(rule, name, operator, values)
                except (EvArgsException, EvValidateException) as e:
                    raise e
                except Exception:
                    self._raise_parse_error('Near "{}"'.format(name))
            else:
                self._raise_unknown_error(name)

    def _add_param_by_rule(self, rule: dict, name: str, operator: int, values: list) -> Param:
        pre_apply_param = rule.get('pre_apply_param')

        if pre_apply_param:
            values = pre_apply_param(values)

        pre_apply = rule.get('pre_apply')

        if pre_apply:
            values = list(map(pre_apply, values))

        value_type = rule.get('type')

        if value_type:
            try:
                if value_type == int or value_type == 'int':
                    values = list(map(self.value_caster.to_int, values))
                elif value_type == float or value_type == 'float':
                    values = list(map(lambda v: float(v), values))
                elif value_type == complex or value_type == 'complex':
                    values = list(map(lambda v: complex(v), values))
                elif value_type == bool or value_type == 'bool':
                    values = list(map(self.value_caster.to_bool, values))
                elif value_type == 'bool_strict':
                    values = list(map(self.value_caster.bool_strict, values))
                elif value_type == str or value_type == 'str':
                    values = list(map(lambda v: str(v), values))
                elif value_type == 'expression':
                    values = list(map(self.value_caster.expression, values))
                elif callable(value_type):
                    values = list(map(value_type, values))
                else:  # raw
                    values = values
            except Exception as e:
                if not rule.get('prevent_error'):
                    raise e
                else:
                    values = [None]

        post_apply = rule.get('post_apply')

        if post_apply:
            values = list(map(post_apply, values))

        post_apply_param = rule.get('post_apply_param')

        if post_apply_param:
            values = post_apply_param(values)

        is_list = isinstance(values, list)

        value = None

        if rule.get('list'):
            if not is_list:
                raise Exception('The value is not list type.({})'.format(name))

            value = values
        else:
            if not is_list:
                value = values
            elif len(values) >= 1:
                value = values[0]

        if value is not None:
            self._validate_value(rule, name, value)

        return self._build_param(name, rule, operator, value)

    def _validate_value(self, rule: dict, name: str, value: any):
        validation = rule.get('validation')

        if validation:
            self._validate(validation, name, value)

        choices = rule.get('choices')

        if choices:
            if value not in choices:
                self.validator.raise_error('Out of choices.({}; {})'.format(name, value), EvValidateException.ERROR_OUT_CHOICES)

    def _validate(self, validation: any, name: str, value: any):
        args = []

        if isinstance(validation, (list, tuple)) and isinstance(validation[0], str):
            [validation, *args] = validation

        if isinstance(validation, str):
            validation_fn = getattr(self.validator, 'validate_' + validation, None)

            if not validation_fn:
                raise EvArgsException('Validation method is not found.({})'.format(validation), EvArgsException.ERROR_PROCESS)

            self._validate_exec(validation_fn, name, value, args)
        elif isinstance(validation, list):
            for v in validation:
                self._validate(v, name, value)
        else:
            error = self._validate_exec(validation, name, value, args)

            if not error:
                self.validator.raise_error('Validation error.({})'.format(name))

    def _validate_exec(self, fn: callable, name: str, value: any, args: list):
        error = False

        try:
            error = fn(name, value, *args)
        except EvValidateException as e:
            raise e
        except Exception:
            self.validator.raise_error('Validation unknown error.({})'.format(name), EvValidateException.ERROR_PROCESS)

        return error

    def _build_param(self, name: str, rule: dict, operator: int, value: any) -> Param:
        if not self.params.get(name):
            item_multiple = True if rule.get('multiple') else False
            value_list = True if rule.get('list') else False

            param = Param(name, item_multiple, value_list)

            self.params[name] = param
        else:
            param = self.params[name]

        param.add(operator, value)

        if param.is_empty():
            if 'default' in rule:
                param.fill_value(rule['default'])
            elif rule.get('require') or self.require_all:
                raise EvValidateException("Require parameter.({})".format(name), EvValidateException.ERROR_REQUIRE)

        return param

    def evaluate(self, name: str, v: any) -> bool:
        rule = self.get_rule(name)

        if rule is None:
            return False

        param = self.get_param(name)

        evaluate_param = rule.get('evaluate_param')

        if evaluate_param:
            pr = evaluate_param(rule, param, v)

            if pr is not None:
                return pr

        if not param.multiple:
            success = self._evaluate_value(rule, param.get_item(0), v)
        else:
            detect = any if rule.get('multiple_or') else all

            success = detect(self._evaluate_value(rule, item, v) for item in param.get_items())

        return success

    def _evaluate_value(self, rule: dict, item: ParamItem, iv: any) -> bool:
        evaluate = rule.get('evaluate')

        if evaluate:
            er = evaluate(item.value, item.operator, iv, rule)

            if er is not None:
                return er

        if not rule.get('list'):
            success = self._evaluate_operator_value(item.operator, item.value, iv)
        else:
            list_or = rule.get('list_or')

            if list_or is None:
                list_or = True if item.operator != Operator.NOT_EQUAL else False

            detect = any if list_or else all

            success = detect(self._evaluate_operator_value(item.operator, v, iv) for v in item.value)

        return success

    def _evaluate_operator_value(self, operator: int, v1: any, v2: any) -> bool:
        success = False

        if operator & Operator.NOT_EQUAL and (v1 != v2):
            success = True
        elif operator & Operator.EQUAL and (v1 == v2):
            success = True
        elif operator & Operator.GREATER and (v1 < v2):
            success = True
        elif operator & Operator.LESS and (v1 > v2):
            success = True

        return success

    def get_rule(self, name: str) -> dict:
        rule = self.rules.get(name)

        if rule is None and self.flexible:
            rule = self.default_rule

        if rule is None:
            self._raise_unknown_error(name)

        return rule

    def get(self, name: str, index: int = -1) -> any:
        rule = self.get_rule(name)

        if rule is None:
            return None

        param = self.get_param(name)

        if param is None:
            param = self._add_param_by_rule(rule, name, 0, [])

        return param.get(index)

    def get_values(self) -> dict:
        values = {}

        for name in self.params:
            values[name] = self.get(name)

        return values

    def put(self, name: str, value: any, operator: int = Operator.EQUAL, reset: bool = False):
        if reset:
            self.reset(name)

        rule = self.get_rule(name)

        if rule is None:
            return None

        values = value if rule.get('list') else [value]

        self._add_param_by_rule(rule, name, operator, values)

    def put_values(self, values: dict, operator: int = Operator.EQUAL, reset: bool = False):
        for name, value in values.items():
            self.put(name, value, operator, reset)

    def reset(self, name: str):
        del self.params[name]

    def reset_params(self):
        self.params = {}

    def has_param(self, name: str) -> bool:
        return (name in self.params)

    def get_param(self, name: str) -> Param:
        param = self.params.get(name)

        rule = self.get_rule(name)

        if rule is None:
            return None

        if param is None and self.flexible:
            param = self._add_param_by_rule(rule, name, None, [])

        return param

    def get_params(self) -> dict:
        return self.params

    def count_params(self) -> int:
        return len(self.params)

    def make_help(self, params: list = None, append_example: bool = False, skip_headers: bool = False):
        help_formatter = self.get_help_formatter()

        if append_example:
            help_formatter.enable_example()

        return help_formatter.make(self.rules, params, skip_headers)

    def _raise_parse_error(self, msg: str):
        raise EvArgsException("Parse error.({})".format(msg), EvArgsException.ERROR_PARSE)

    def _raise_unknown_error(self, name: str):
        if not self.ignore_unknown:
            raise EvValidateException("Unknown parameter.({})".format(name), EvValidateException.ERROR_UNKNOWN_PARAM)
