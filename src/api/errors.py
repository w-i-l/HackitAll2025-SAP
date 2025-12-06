class SessionAlreadyStartedError(Exception):
    """Exception raised when trying to start a session that is already started."""

    def __init__(
        self,
        message: str = "SessionAlreadyStartedError([409]) - Session is already started",
    ):
        self.message = message
        super().__init__(self.message)


class NoActiveSessionError(Exception):
    """Exception raised when trying to stop a session that is not active."""

    def __init__(
        self,
        message: str = "NoActiveSessionError([404]) - No active session found for the given API key",
    ):
        self.message = message
        super().__init__(self.message)


class SessionAlreadyEndedError(Exception):
    """Exception raised when trying to stop a session that has already ended."""

    def __init__(
        self, message: str = "SessionAlreadyEndedError([400]) - Session already ended"
    ):
        self.message = message
        super().__init__(self.message)


class APIError(Exception):
    def __init__(self, status_code: int, message: str = "API Error"):
        self.status_code = status_code
        self.message = message
        super().__init__(f"APIError([{status_code}]) - {message}")
