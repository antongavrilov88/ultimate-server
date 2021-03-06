from commands.exceptions import UltimateServerException


class DAOException(UltimateServerException):
    """
    Base DAO exception class
    """


class DAOCreateFailedError(DAOException):
    """
    DAO Create failed
    """

    message = "Create failed"


class DAOGetFailedError(DAOException):
    """
    DAO Get failed
    """

    message = "Get failed"


class DAOUpdateFailedError(DAOException):
    """
    DAO Update failed
    """

    message = "Updated failed"


class DAODeleteFailedError(DAOException):
    """
    DAO Delete failed
    """

    message = "Delete failed"


class DAOConfigError(DAOException):
    """
    DAO is miss configured
    """

    message = "DAO is not configured correctly missing model definition"