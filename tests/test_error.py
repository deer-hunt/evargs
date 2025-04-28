from evargs import EvArgs, EvArgsException, ValidateException, TypeCast
import pytest
import re


# Document: https://github.com/deer-hunt/evargs/
class TestError:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_raise_error(self):
        evargs = EvArgs()

        # raise_error=TypeCast.ERROR_DEFAULT_NONE
        assert evargs.assign(' a ', cast=int, default=1) == 1

        with pytest.raises(ValidateException):
            assert evargs.assign('', cast=int, nullable=False) is None

        with pytest.raises(ValidateException):
            assert evargs.assign(None, cast=int, nullable=False) is None

        assert evargs.assign('', cast=int, default=1, raise_error=TypeCast.ERROR_DEFAULT_NONE) == 1
        assert evargs.assign(None, cast=int, default=1, raise_error=TypeCast.ERROR_DEFAULT_NONE) == 1

        assert evargs.assign(' ', cast=int, trim=True, default=1, raise_error=TypeCast.ERROR_DEFAULT_NONE) == 1

        with pytest.raises(ValidateException):
            evargs.assign(' a ', cast=int, raise_error=TypeCast.ERROR_DEFAULT_NONE)

        with pytest.raises(ValidateException):
            evargs.assign('', cast=int, nullable=False, raise_error=TypeCast.ERROR_DEFAULT_NONE)

        assert evargs.assign(' a ', cast=int, raise_error=0) is None
        assert evargs.assign(' a ', cast=int, raise_error=TypeCast.ERROR_CANCEL) is None
        assert evargs.assign('', cast=int, raise_error=TypeCast.ERROR_CANCEL) is None

        with pytest.raises(ValidateException):
            evargs.assign(' a ', cast=int, default=1, nullable=False, raise_error=TypeCast.ERROR_ALL)

        with pytest.raises(ValidateException):
            evargs.assign('', cast=int, default=1, nullable=False, raise_error=TypeCast.ERROR_ALL)

    def test_unknown_rule_options(self):
        evargs = EvArgs()

        with pytest.raises(EvArgsException):
            evargs.initialize({
                'a': {'cast': int, 'unknown': True}
            })

        with pytest.raises(EvArgsException):
            assert evargs.assign(' a ', cast=int, unknown=None)
