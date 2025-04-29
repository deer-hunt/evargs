import re


class ParamValue:
    def __init__(self):
        self.value = None  #: any: None


class ExpParamValue(ParamValue):
    def __init__(self):
        self.value = None  #: any: None
        self.operator = None  #: int: None


class MultipleParam:
    def __init__(self):
        self.params = []  #: list: []

    def get(self, index: int) -> ParamValue:
        return self.params[index]

    def add(self, param: ParamValue):
        self.params.append(param)

    def get_size(self):
        return len(self.params)

    def get_values(self):
        return [param.value for param in self.params]


class Operator:
    EQUAL = 1
    GREATER = 2
    LESS = 4
    NOT_EQUAL = 8

    LIST_SPLIT = ','
    VALUE_SPLIT = ';'

    @staticmethod
    def is_evaluate(v: str) -> bool:
        return True if re.search(r'^[=<>!]+$', v) else False

    @staticmethod
    def parse_operator(value: str) -> int:
        operator = 0

        if re.search(r'!=', value):
            operator |= Operator.NOT_EQUAL
        elif re.search(r'=', value):
            operator |= Operator.EQUAL

        if re.search(r'>', value):
            operator |= Operator.GREATER

        if re.search(r'<', value):
            operator |= Operator.LESS

        return operator
