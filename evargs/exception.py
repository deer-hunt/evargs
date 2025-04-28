class EvArgsException(Exception):
    ERROR_PROCESS = 1
    ERROR_GENERAL = 2
    ERROR_PARSE = 3

    def __init__(self, message, error_code=ERROR_PROCESS):
        super().__init__(message)
        self.error_code = error_code
        self.name = None

    def set_name(self, name):
        self.name = name

    def __str__(self):
        msg = super().__str__()

        if self.name is not None:
            msg += f' - {self.name}'

        return msg


class ValidateException(Exception):
    ERROR_PROCESS = 1
    ERROR_GENERAL = 2
    ERROR_REQUIRED = 3
    ERROR_CAST = 4
    ERROR_UNKNOWN_PARAM = 5
    ERROR_OUT_CHOICES = 6

    def __init__(self, message, error_code=ERROR_PROCESS):
        super().__init__(message)
        self.error_code = error_code
        self.name = None

    def set_name(self, name):
        self.name = name

    def __str__(self):
        msg = super().__str__()

        if self.name is not None:
            msg += f' - {self.name}'

        return msg
