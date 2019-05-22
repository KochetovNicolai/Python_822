from enum import Enum
from flask import redirect
from urllib.parse import urlencode


class Errors(Enum):
    COMPANIES_OVERFLOW = 1
    WRONG_COMPANY = 2
    PLOT_ERROR = 3
    UNKNOWN_ERROR = 4


def error_redirect(error_code):
    print('/error/?' + urlencode({'type': error_code}))

    return redirect('/error/?' + urlencode({'type': error_code}))
