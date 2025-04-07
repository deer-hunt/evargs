import re


class Operator:
    EQUAL = 1
    NOT_EQUAL = 2
    GREATER = 4
    LESS = 8

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


class ParamItem:
    def __init__(self, operator: int, value: any):
        self.operator = operator
        self.value = value

    @staticmethod
    def is_empty(value: any) -> bool:
        return True if value is None or value == '' or value == [] else False


class Param:
    def __init__(self, name: str, item_multiple: bool = False, value_list: bool = False):
        self.name = name
        self.multiple = item_multiple
        self.list = value_list
        self.items = []

    def add(self, operator: int, value: any):
        item = ParamItem(operator, value)

        if not self.multiple:
            if len(self.items) == 0:
                self.items.append(item)

            self.items[0] = item
        else:
            self.items.append(item)

    def get_item(self, index: int = 0) -> any:
        if index >= len(self.items):
            return None

        return self.items[index]

    def get_items(self) -> list:
        return self.items

    def get_length(self) -> int:
        return 1 if not self.multiple else len(self.items)

    def reset(self):
        self.items = []

    def set_item(self, operator: int, value: any, index: int = 0):
        item = self.items[index]

        if operator:
            item.operator = operator

        item.value = value

    def get(self, index: int = -1) -> any:
        if index >= len(self.items):
            return None

        if index == -1:
            if self.multiple:
                return [item.value for item in self.items]
            else:
                index = 0

        return self.items[index].value

    def get_list(self) -> list:
        values = []

        for item in self.items:
            if self.list:
                values.extend(item.value)
            else:
                values.append(item.value)

        return values

    def get_size(self, index: int) -> int:
        return 1 if not self.list else len(self.get(index))

    def is_empty(self) -> bool:
        is_empty = False

        if not self.multiple:
            value = self.get(0)

            is_empty = ParamItem.is_empty(value)
        else:
            if len(self.items) == 0:
                is_empty = True
            else:
                for item in self.items:
                    if ParamItem.is_empty(item.value):
                        is_empty = True
                        break

        return is_empty

    def fill_value(self, value: any, operator: int = Operator.EQUAL):
        if len(self.items) == 0:
            self.add(operator, value)
        else:
            if self.multiple:
                for index, item in enumerate(self.items):
                    if ParamItem.is_empty(item.value):
                        item.value = value
            else:
                item = self.items[0]

                if ParamItem.is_empty(item.value):
                    item.value = value
