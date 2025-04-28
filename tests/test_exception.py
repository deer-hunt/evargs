import pytest

from evargs import EvArgsException, ValidateException
import re


# Document: https://github.com/deer-hunt/evargs/
class TestException:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_ev_args_exception(self):
        e = EvArgsException('Test')

        e.set_name('param1')

        assert re.search('param1', str(e))

        with pytest.raises(EvArgsException):
            raise e

    def test_ev_validate_exception(self):
        e = ValidateException('Test')

        e.set_name('param1')

        assert re.search('param1', str(e))

        with pytest.raises(ValidateException):
            raise e
