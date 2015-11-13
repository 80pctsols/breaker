# breaker

[![Build Status](https://magnum.travis-ci.com/80pctsols/breaker.svg?token=qzJ7x5EP6fzW63bPpZxL&branch=master)](https://magnum.travis-ci.com/80pctsols/breaker)

Small python library to help with serving requests between services.

Currently holds a simple Circuit Breaker which is used to fail fast on services
that are returning errors.

## Usage

```python
from breaker import CircuitBreaker

def my_function(a, b):
    return a + b

cb = CircuitBreaker(my_function, failures_allowed=3, timeout=10)

cb.call(a, b)
```
