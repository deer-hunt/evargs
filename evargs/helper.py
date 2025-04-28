import ast
import operator as op


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
            raise TypeError(f"Unsupported cast-type: {type(node)}")
