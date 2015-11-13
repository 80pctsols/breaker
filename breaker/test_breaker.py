from .breaker import (
    CircuitBreaker,
    CircuitBreakerException
)

import datetime
import time

def func(a, b, c=10):
    return a + b + c

def error_func():
    l = []
    return l[10]

def error2_func():
    raise Exception

def test_call():
    cb = CircuitBreaker(func)
    assert cb.call(1, 2) == func(1, 2)
    assert cb.call(10, 20, 30) == func(10, 20, 30)

def test_reset():
    cb = CircuitBreaker(func)
    cb.num_failures = 10
    cb.reset()
    assert cb.num_failures == 0

def test_failure():
    cb = CircuitBreaker(func)
    old_failures = cb.num_failures
    cb.failure()
    assert old_failures + 1 == cb.num_failures

def test_closed_breaker():
    cb = CircuitBreaker(func)
    cb.num_failures = cb.failures_allowed + 1
    try:
        cb.call(1, 2)
        assert False
    except CircuitBreakerException:
        assert True

def test_error_functions():
    cb = CircuitBreaker(error_func)
    for i in range(12):
        try:
            cb.call()
        except CircuitBreakerException:
            assert i > 10
        except IndexError:
            assert i <= 10

def test_not_half_open():
    cb = CircuitBreaker(func)
    assert cb.is_half_open() is False

def test_half_open():
    cb = CircuitBreaker(error_func)
    cb.num_failures = 20
    double_ago = past(2 * cb.timeout)
    cb.last_failure = double_ago
    assert cb.is_half_open() is True

def test_half_open_close():
    cb = CircuitBreaker(error_func, 1, .5)
    for i in range(2):
        try:
            cb.call()
            assert False
        except Exception:
            assert True

    time.sleep(1)
    assert cb.is_half_open() is True

    # Should try the call again if its half open
    try:
        cb.call()
        assert False
    except IndexError:
        assert True
    except CircuitBreakerException:
        assert False

    assert cb.state() == cb.OPEN
    assert cb.is_half_open() is False

def past(seconds):
    return datetime.datetime.now() - datetime.timedelta(seconds=seconds)
