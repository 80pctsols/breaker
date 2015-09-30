from .breaker import (
    CircuitBreaker,
    CircuitBreakerException
)

def func(a, b, c=10):
    return a + b + c

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
    cb.failure()
    assert cb.num_failures > 0

def test_closed_breaker():
    cb = CircuitBreaker(func)
    cb.num_failures = cb.failures_allowed + 1
    try:
        cb.call(1, 2)
        assert False
    except CircuitBreakerException:
        assert True
