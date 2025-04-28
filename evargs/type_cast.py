from decimal import Decimal, ROUND_HALF_UP
from distutils.util import strtobool
from enum import Enum
from typing import Optional, Type

"""
TypeCast

This class provides flexible type conversion capabilities for casting to `int`, `float`, `complex`, `bool`, `Enum class`.
"""


class TypeCast:
    ERROR_CANCEL = 0
    ERROR_DEFAULT_NONE = 1
    ERROR_ALL = 2

    @classmethod
    def to_int(cls, v: any, default: int = None, nullable: bool = False, raise_error: int = ERROR_DEFAULT_NONE) -> int:
        """
        Cast to int.

        :param v: Source value.
        :param default: The default value to return if casting fails.
        :param nullable: Allows `None` if value is empty.
        :param raise_error: Raises an error when casting fails.
        :rtype: Optional[int]
        """
        try:
            value = int(float(v))
        except (ValueError, TypeError):
            if default is not None and raise_error != TypeCast.ERROR_ALL:
                value = default
            else:
                value = None

                if raise_error and not (nullable and cls.is_empty(v)):
                    cls._raise_error('Casting to int failed.', v)

        return value

    @classmethod
    def to_round_int(cls, v: any, default: int = None, nullable: bool = False, raise_error: int = ERROR_DEFAULT_NONE) -> int:
        """
        Cast to int with round.

        :param v: Source value.
        :param default: The default value to return if casting fails.
        :param nullable: Allows `None` if value is empty.
        :param raise_error: Raises an error when casting fails.
        :rtype: Optional[int]
        """
        try:
            value = int(Decimal(v).quantize(Decimal('0'), rounding=ROUND_HALF_UP))
        except Exception:
            if default is not None and raise_error != TypeCast.ERROR_ALL:
                value = default
            else:
                value = None

                if raise_error and not (nullable and cls.is_empty(v)):
                    cls._raise_error('Casting to int failed.', v)

        return value

    @classmethod
    def to_float(cls, v: any, default: float = None, nullable: bool = False, raise_error: int = ERROR_DEFAULT_NONE) -> float:
        """
        Cast to float.

        :param v: Source value.
        :param default: The default value to return if casting fails.
        :param nullable: Allows `None` if value is empty.
        :param raise_error: Raises an error when casting fails.
        :rtype: Optional[float]
        """
        try:
            value = float(v)
        except (ValueError, TypeError):
            if default is not None and raise_error != TypeCast.ERROR_ALL:
                value = default
            else:
                value = None

                if raise_error and not (nullable and cls.is_empty(v)):
                    cls._raise_error('Casting to float failed.', v)

        return value

    @classmethod
    def to_complex(cls, v: any, default: complex = None, nullable: bool = False, raise_error: int = ERROR_DEFAULT_NONE) -> complex:
        """
        Cast to complex.

        :param v: Source value.
        :param default: The default value to return if casting fails.
        :param nullable: Allows `None` if value is empty.
        :param raise_error: Raises an error when casting fails.
        :rtype: Optional[complex]
        """
        try:
            value = complex(v)
        except (ValueError, TypeError):
            if default is not None and raise_error != TypeCast.ERROR_ALL:
                value = default
            else:
                value = None

                if raise_error and not (nullable and cls.is_empty(v)):
                    cls._raise_error('Casting to complex failed.', v)

        return value

    @classmethod
    def to_str(cls, v: any, default: str = None, nullable: bool = False, raise_error: int = ERROR_DEFAULT_NONE) -> str:
        """
        Cast to str.

        :param v: Source value.
        :param default: The default value to return if casting fails.
        :param nullable: Allows `None` if value is empty.
        :param raise_error: Raises an error when casting fails.
        :rtype: str
        """
        if not cls.is_empty(v):
            v = str(v)
        else:
            if default is not None and raise_error != TypeCast.ERROR_ALL:
                v = default
            elif v is None:
                if raise_error and not nullable:
                    cls._raise_error('Casting to str failed.', v)

        return v

    @classmethod
    def to_bool(cls, v: any, default: bool = None, nullable: bool = False, raise_error: int = ERROR_DEFAULT_NONE, none_cast: bool = False) -> Optional[bool]:
        """
        Cast to bool.

        :param v: Source value.
        :param default: The default value to return if casting fails.
        :param nullable: Allows `None` if value is empty.
        :param raise_error: Raises an error when casting fails.
        :param none_cast: Whether to convert None to False.
        :rtype: bool
        """
        try:
            if isinstance(v, str):
                v = v.strip()

                value = True if strtobool(v) else False
            elif v is None:
                if none_cast:
                    value = False
                else:
                    raise Exception()
            else:
                value = True if v > 0 else False
        except Exception:
            if default is not None and raise_error != TypeCast.ERROR_ALL:
                value = default
            else:
                value = None

                if raise_error and not (nullable and cls.is_empty(v)):
                    cls._raise_error('Casting to bool failed.', v)

        return value

    @classmethod
    def bool_strict(cls, v: any, default: bool = None, nullable: bool = False, raise_error: int = ERROR_DEFAULT_NONE, none_cast: bool = False) -> Optional[bool]:
        """
        Cast to bool strictly. Converting only `'1', '0', 1, 0`.

        :param v: Source value.
        :param default: The default value to return if casting fails.
        :param nullable: Allows `None` if value is empty.
        :param raise_error: Raises an error when casting fails.
        :param none_cast: Whether to convert None to False.
        :rtype: bool
        """
        try:
            if isinstance(v, str):
                v = v.strip()

                if v == '1':
                    value = True
                elif v == '0':
                    value = False
                else:
                    raise Exception()

            elif v is None:
                if none_cast:
                    value = False
                else:
                    raise Exception()
            else:
                if v == 1:
                    value = True
                elif v == 0:
                    value = False
                else:
                    raise Exception()
        except Exception:
            if default is not None and raise_error != TypeCast.ERROR_ALL:
                value = default
            else:
                value = None

                if raise_error and not (nullable and cls.is_empty(v)):
                    cls._raise_error('Casting to bool failed.', v)

        return value

    @classmethod
    def bool_loose(cls, v: any, default: bool = None) -> bool:
        """
        Cast to bool loosely. Always return `True` or `False`.

        :param v: Source value.
        :param default: The default value to return if casting fails.
        :rtype: bool
        """
        v = cls.to_bool(v, default, raise_error=0, none_cast=True)

        return True if v is True else False

    @classmethod
    def to_enum(cls, enum_class: Type[Enum], v: any, default: Enum = None, is_value: bool = True, is_name: bool = False, nullable: bool = False, raise_error: int = ERROR_DEFAULT_NONE) -> Enum:
        """
        Cast to enum.

        :param enum_class: Enum class.
        :param v: Source value.
        :param default: The default value to return if casting fails.
        :param is_value: Conversion by using the enum's value.
        :param is_name: Conversion by using the enum's name.
        :param nullable: Allows `None` if value is empty.
        :param raise_error: Raises an error when casting fails.
        :rtype: Enum
        """
        value = None

        for v_enum in enum_class:
            if is_value and v_enum.value == v:
                value = v_enum
                break
            elif is_name and v_enum.name == v:
                value = v_enum
                break

        if value is None:
            if default is not None and raise_error != TypeCast.ERROR_ALL:
                value = default
            else:
                if raise_error and not (nullable and cls.is_empty(v)):
                    cls._raise_error('Casting to enum failed.', v)

        return value

    @classmethod
    def to_enum_loose(cls, enum_class: Type[Enum], v: any, default: Enum = None, is_value: bool = True, is_name: bool = False, nullable: bool = False, raise_error: int = ERROR_DEFAULT_NONE) -> Enum:
        """
        Cast to enum loosely.

        :param enum_class: Enum class.
        :param v: Source value.
        :param default: The default value to return if casting fails.
        :param is_value: Conversion by using the enum's value.
        :param is_name: Conversion by using the enum's name.
        :param nullable: Allows `None` if value is empty.
        :param raise_error: Raises an error when casting fails.
        :rtype: Enum
        """
        value = cls.to_enum(enum_class, v, default, is_value, is_name, raise_error=0)

        try:
            if value is None:
                v_numeric = cls.to_float(v, raise_error=False)

                value = cls.to_enum(enum_class, v_numeric, default, is_value, is_name, nullable=nullable, raise_error=raise_error)
        except Exception:
            if raise_error:
                cls._raise_error('Casting to enum failed.', v)

        return value

    @classmethod
    def noop(cls, v: any, default: any = None, nullable: bool = False, raise_error: int = ERROR_DEFAULT_NONE) -> any:
        """
        Noop.

        :param v: Source value.
        :param default: The default value to return if casting fails.
        :param nullable: Allows `None` if value is empty.
        :param raise_error: Raises an error when casting fails.
        :rtype: any
        """
        if v is None:
            if default is not None and raise_error != TypeCast.ERROR_ALL:
                v = default
            else:
                v = None

                if raise_error and not nullable:
                    cls._raise_error("'None' is not allowed.", None)

        return v

    @classmethod
    def is_empty(cls, v: any) -> bool:
        """Whether value is empty value."""
        return True if v is None or v == '' else False

    @classmethod
    def _raise_error(cls, msg: str, v: any):
        if isinstance(v, str):
            msg += f'(\'{v}\')'
        else:
            msg += f'({v})'

        raise ValueError(f'{msg}')
