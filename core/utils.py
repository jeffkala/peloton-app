#!/usr/bin/env python
"""API support utilities

This module contains classes and functions related to API support functions.
in general no code is hosted here related to specific API calls, most of these
functions and classes are used as decorators to augment existing functionality.

    Todo:
"""

# `========== time_me decorator used to time function/object run time ==========`
import time


def time_me(f):
    """times function execution time
    can be used as a decorator to other functions to time and report execution time

    Returns:
        string: `>>> func1 took 10 ms to run.`
    """
    import time
    from functools import wraps

    def wrapper(*args, **kwargs):
        start = time.time()
        results = f(*args, **kwargs)
        end = time.time()
        print('>>> {} took {((end - start) * 1000) / 1000.0:.1f} seconds to run.'.format(f.__name__))
        return results

    return wrapper


class Retry:
    """Adds reliablitiy to API calls by doing a retry on certain failures

    The decorated function must return response.status_code via the API call
    this class allows flexibility by using class inheritance and allowing us to
    modify certain aspects of the class based on certain server responses.

    Returns:
        Original wrapped function when used as a decorator
    """
    MAX_TRIES = 5

    def is_valid(self, resp):
        return not resp.status_code == 500

    def __call__(self, f):
        def wrapper(*args, **kwargs):
            tries = 0
            try:
                while True:
                    resp = f(*args, **kwargs)
                    if self.is_valid(resp) or tries >= self.MAX_TRIES:
                        break
                    tries += 1
                    time.sleep(tries + 1)
                    print('Server error: {}, retries: {}'.format(resp.status_code, tries))
                return resp
            except Exception as e:
                print(e)
                exit(1)

        return wrapper


class RetryOnAuthError(Retry):
    """clone Retry and make Auth error class"""
    MAX_TRIES = 1

    def is_valid(self, resp):
        return not resp.status_code >= 401


class RetryOnServerError(Retry):
    """clone Retry and make Server error class"""
    MAX_TRIES = 5

    def is_valid(self, resp):
        return not resp.status_code >= 500 and resp.status_code <= 599


class RetryOnServerErrorLogin(Retry):
    """clone Retry and make Server error class"""
    MAX_TRIES = 1

    def is_valid(self, resp):
        return not resp.status_code >= 500 and resp.status_code <= 599


# create callable functions from class to use as decorators
# this functions will be imported at run time by sessions.py
retry_on_auth_failure = RetryOnAuthError()
retry_on_auth_and_error = RetryOnAuthError()
retry_on_server_error = RetryOnServerError()
retry_on_login_error = RetryOnServerErrorLogin()

