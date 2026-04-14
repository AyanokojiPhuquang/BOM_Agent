try:
    _ExceptionGroup = ExceptionGroup
except NameError:
    from exceptiongroup import ExceptionGroup as _ExceptionGroup


class FallbackExceptionGroup(_ExceptionGroup):
    """A group of exceptions raised when all fallback models fail."""
