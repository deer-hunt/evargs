class EvArgsException(Exception):
    ERROR_PROCESS = 1
    ERROR_GENERAL = 2
    ERROR_PARSE = 3


class EvValidateException(Exception):
    ERROR_PROCESS = 1
    ERROR_GENERAL = 2
    ERROR_REQUIRE = 3
    ERROR_UNKNOWN_PARAM = 4
    ERROR_OUT_CHOICES = 5
