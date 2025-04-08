class EvArgsException(Exception):
    ERROR_PROCESS = 1
    ERROR_GENERAL = 2
    ERROR_PARSE = 3

    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code


class EvValidateException(Exception):
    ERROR_PROCESS = 1
    ERROR_GENERAL = 2
    ERROR_REQUIRE = 3
    ERROR_UNKNOWN_PARAM = 4
    ERROR_OUT_CHOICES = 5

    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code
