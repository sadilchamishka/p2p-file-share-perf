class MessageLengthError(Exception):
    pass


class ResponseError(Exception):
    pass


class InvalidQueryError(Exception):
    def __init__(self, msg="Invalid Query", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)

class ResourceNotFoundError(Exception):
    def __init__(self, msg="Resource Not Found in the Server", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
