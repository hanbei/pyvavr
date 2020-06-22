class ValueException(Exception):

    def __init__(self, message=None):
        super().__init__(message)


class CantCurryVarArgException(Exception):

    def __init__(self, message=None):
        super().__init__(message)
