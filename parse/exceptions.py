from functools import wraps


class ParseException(Exception):
    """Parse sent back an error"""
    pass


def raises_parse_error(func):
    @wraps(func)
    def checked_for_parse_error(*args, **kwargs):
        result = func(*args, **kwargs)
        if (
                result is not None and not isinstance(result, int)
                and 'error' in result):
            raise ParseException(result)
        else:
            return result

    return checked_for_parse_error
