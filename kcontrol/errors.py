__all__ = [
            'NotFoundError',
            'NotImplementedError',
            'DuplicateError',
            'ModificationError',
            'ValidationError'
           ]

class NotFoundError(Exception):
    pass

class NotImplementedError(Exception):
    pass

class DuplicateError(Exception):
    pass


class ValidationError(Exception):
    pass

class ModificationError(ValidationError):
    def current_access(self):
        return self.args[0]
    def last_access(self):
        return self.args[1]
