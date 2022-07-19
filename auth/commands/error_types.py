from enum import Enum


class UltimateServerErrorType(str, Enum):
    """
    Types of errors that can exist within Superset.

    Keep in sync with superset-frontend/src/components/ErrorMessage/types.ts
    and docs/src/pages/docs/Miscellaneous/issue_codes.mdx
    """

    # Frontend errors
    USER_ALREADY_EXISTS = "USER_ALREADY_EXISTS"
