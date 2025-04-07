from distutils.util import strtobool
import ast
import operator as op
from typing import Optional, Union


class ValueCaster:
    @staticmethod
    def to_int(v: any) -> int:
        return int(float(v))

    @staticmethod
    def bool_strict(v: any) -> int:
        return ValueCaster.to_bool(v, True)

    @staticmethod
    def to_bool(v: any, strict: bool = False) -> Optional[bool]:
        v = str(v).strip()

        try:
            if len(v) > 0 and strtobool(v):
                return True
        except Exception:
            if strict:
                return None

        return False

    @staticmethod
    def expression(v: str) -> Union[int, float]:
        return ExpressionParser.parse(v)


class ExpressionParser:
    OPERATORS = {
        ast.Add: op.add,
        ast.Sub: op.sub,
        ast.Mult: op.mul,
        ast.Div: op.truediv,
        ast.Pow: op.pow,
        ast.BitXor: op.xor,
        ast.USub: op.neg
    }

    @classmethod
    def parse(cls, expr: str):
        parsed = ast.parse(expr, mode='eval')

        return cls.safe_eval(parsed.body)

    @classmethod
    def safe_eval(cls, node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        elif isinstance(node, ast.BinOp):
            return cls.OPERATORS[type(node.op)](cls.safe_eval(node.left), cls.safe_eval(node.right))
        elif isinstance(node, ast.UnaryOp):
            return cls.OPERATORS[type(node.op)](cls.safe_eval(node.operand))
        else:
            raise TypeError(f"Unsupported type: {type(node)}")
