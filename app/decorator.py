from functools import wraps


def login_required(func):
    @wraps(func)
    def decorate(*args, **kwargs):
        return func(*args, **kwargs)

    return decorate
