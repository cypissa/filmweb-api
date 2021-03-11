""" Exceptions """


class LoginFailedException(Exception):
    pass


class NoActiveUserSessionException(Exception):
    pass


class WrongArgumentException(Exception):
    pass
