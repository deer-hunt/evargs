from distutils.util import strtobool
from enum import Enum
from typing import Optional, Type

"""
ValueCaster

This class provides flexible type conversion capabilities for casting to `int`, `float`, `complex`, `bool`, `Enum class`.
"""


class ValueCaster:
    @classmethod
    def to_int(cls, v: any, ignore_error: bool = False) -> int:
        try:
            value = int(float(v))
        except (ValueError, TypeError):
            value = None

            if not ignore_error:
                raise Exception(f'Casting to int failed.({v})')

        return value

    @classmethod
    def to_float(cls, v: any, ignore_error: bool = False) -> float:
        try:
            value = float(v)
        except (ValueError, TypeError):
            value = None

            if not ignore_error:
                raise Exception(f'Casting to float failed.({v})')

        return value

    @classmethod
    def to_complex(cls, v: any, ignore_error: bool = False) -> complex:
        try:
            value = complex(v)
        except (ValueError, TypeError):
            value = None

            if not ignore_error:
                raise Exception(f'Casting to complex failed.({v})')

        return value

    @classmethod
    def to_bool(cls, v: any, strict: bool = False) -> Optional[bool]:
        v = str(v).strip()

        try:
            if len(v) > 0 and strtobool(v):
                return True
        except Exception:
            if strict:
                return None

        return False

    @classmethod
    def bool_strict(cls, v: any) -> int:
        return cls.to_bool(v, True)

    @classmethod
    def to_enum(cls, enum_class: Type[Enum], v: any, illegal_value: Enum = None, is_value: bool = True, is_name: bool = False) -> Enum:
        value = None

        for v_enum in enum_class:
            if is_value and v_enum.value == v:
                value = v_enum
                break
            elif is_name and v_enum.name == v:
                value = v_enum
                break

        if value is None and illegal_value is not None:
            value = illegal_value

        return value

    @classmethod
    def to_enum_loose(cls, enum_class: Type[Enum], v: any, illegal_value: Enum = None, is_value: bool = True, is_name: bool = False) -> Enum:
        value = cls.to_enum(enum_class, v, illegal_value, is_value, is_name)

        if value is None:
            v_numeric = cls.to_float(v, ignore_error=True)
            value = cls.to_enum(enum_class, v_numeric, illegal_value, is_value, is_name)

        return value
