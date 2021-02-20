import enum
import re


class AccountErrorMessages(enum.Enum):
    TOO_LONG_EMAIL_ERROR = "TOO_LONG_EMAIL_ERROR"
    NON_UNIQUE_EMAIL_ERROR = "NON_UNIQUE_EMAIL_ERROR"
    INCORRECT_PASSWORD_SCHEME_ERROR = "INCORRECT_PASSWORD_SCHEME_ERROR"

    DISABLED_ACCOUNT_ERROR = "DISABLED_ACCOUNT_ERROR"
    CREDENTIALS_ERROR = "CREDENTIALS_ERROR"
    REQUEST_FIELDS_ERROR = "REQUEST_FIELDS_ERROR"


def new_password_is_correct(password: str) -> bool:
    return re.fullmatch(r'[A-Za-z0-9@#$%^&_+=]{8,}', password)
