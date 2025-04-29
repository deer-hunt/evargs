import io
import re
import tokenize
from types import SimpleNamespace
from typing import Union, overload

from evargs.evargs import EvArgs
from evargs.exception import EvArgsException, ValidateException
from evargs.modules import Operator, ParamValue, ExpParamValue, MultipleParam
from evargs.validator import Validator

'''
ExpEvArgs
'''


class ExpEvArgs(EvArgs):
    def __init__(self, validator: Validator = None):
        super().__init__(validator)

        self.defined_rule.update({
            'evaluation': None, 'evaluation_apply': None, 'allowed_operator': -1,
            'multiple_or': False, 'list_or': None
        })

    def parse(self, expression: str, reset: bool = True):
        """Parse the expression."""

        if reset:
            self.reset()

        readline = io.StringIO(expression).readline
        tokens = tokenize.generate_tokens(readline)

        ns = SimpleNamespace()

        ns.name = None
        ns.operator = 0
        ns.values = []

        try:
            self._parse_expression(tokens, ns)

            self._parse_not_assigned()
        except (EvArgsException, ValidateException) as e:
            e.set_name(ns.name)
            raise e
        except Exception:
            self._raise_parse_error('Illegal expression.', ns.name)

    def _build_param(self, name: str, rule: dict) -> ParamValue:
        param = ExpParamValue()
        param.operator = Operator.EQUAL

        return param

    def _add_param(self, name: str, operator: int, v: list):
        if name is not None:
            rule = self._get_rule(name)

            if rule is not None:
                allowed_operator = rule.get('allowed_operator')

                if allowed_operator > -1:
                    if not ((operator & ~allowed_operator) == 0):
                        raise EvArgsException('Not allowed operator.', EvArgsException.ERROR_PARSE)

                if not rule.get('list'):
                    v = ''.join(v)

                param = self._add_by_rule(rule, name, v)
                param.operator = operator
            else:
                self._raise_unknown_param(name)

    def _parse_expression(self, tokens, ns: SimpleNamespace):
        for tok in tokens:
            if tok.type == tokenize.NAME:
                if ns.name is None:
                    ns.name = tok.string
                else:
                    ns.values.append(tok.string)
            elif tok.type == tokenize.OP:
                if Operator.is_evaluate(tok.string):
                    if ns.operator == 0:
                        ns.operator = Operator.parse_operator(tok.string)
                    else:
                        self._raise_parse_error('Illegal operator.')
                elif tok.string == Operator.LIST_SPLIT:
                    pass
                elif tok.string == Operator.VALUE_SPLIT:
                    self._add_param(ns.name, ns.operator, ns.values)
                    ns.name = None
                    ns.operator = 0
                    ns.values = []
                else:
                    ns.values.append(tok.string)
            elif tok.type == tokenize.NUMBER:
                ns.values.append(tok.string)
            elif tok.type == tokenize.STRING:
                m = re.search(r'^["\'](.+)["\']$', tok.string)

                v = tok.string if m is None else m.group(1)

                ns.values.append(v)
            elif tok.type == tokenize.NEWLINE or tok.type == tokenize.ENDMARKER:
                continue

        if ns.name and ns.operator:
            self._add_param(ns.name, ns.operator, ns.values)
            ns.name = None
            ns.operator = 0

        if ns.name or ns.operator:
            self._raise_parse_error('End expression.')

    def _parse_not_assigned(self):
        for name in self.rules.keys():
            rule = self._get_rule(name)

            param = self.params.get(name)

            if param is None and rule is not None:
                self._add_by_rule(rule, name, None)

    def evaluate(self, name: str, v: any) -> bool:
        """Evaluate a value against a rule and parameter configuration."""
        rule = self._get_rule(name)

        if rule is None:
            return False

        param = self.get_param(name)

        evaluation_apply = rule.get('evaluation_apply')

        if evaluation_apply:
            pr = evaluation_apply(rule, param, v)

            if pr is not None:
                return pr

        if not isinstance(param, MultipleParam):
            success = self._evaluate_value(rule, param, v)
        else:
            detect = any if rule.get('multiple_or') else all

            success = detect(self._evaluate_value(rule, exp_param, v) for exp_param in param.params)

        return success

    def _evaluate_value(self, rule: dict, param: ExpParamValue, iv: any) -> bool:
        evaluation = rule.get('evaluation')

        if evaluation:
            er = evaluation(param.value, param.operator, iv, rule)

            if er is not None:
                return er

        if not rule.get('list'):
            success = self._evaluate_operator_value(param.operator, param.value, iv)
        else:
            list_or = rule.get('list_or')

            if list_or is None:
                list_or = True if param.operator != Operator.NOT_EQUAL else False

            detect = any if list_or else all

            success = detect(self._evaluate_operator_value(param.operator, v, iv) for v in param.value)

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

    @overload
    def get_param(self, name: str) -> Union[ExpParamValue, MultipleParam]:
        """Get a parameter by name."""
        ...

    def get_param(self, name: str) -> Union[ParamValue, MultipleParam]:
        return super().get_param(name)

    def _raise_parse_error(self, msg: str, name: str = None):
        e = EvArgsException(f'Parse error. {msg}', EvArgsException.ERROR_PARSE)

        if name is not None:
            e.set_name(name)

        raise e
