
class CircuitBreaker(object):
    """A circuit breaker which handles requests, timeouts
    and other failures to help with resiliency.

    Attributes:
      failures_allowed: number of failures in a row to trip circuit
      timeout: time in milliseconds before a request times out
    """
    OPEN = "open"
    CLOSED = "closed"
    HALF_OPEN = "half_open"

    def __init__(self, func, failures_allowed=10, timeout=1000):
        """ Create a CircuitBreaker that has a default of 10
        failures in a row to be tripped, and a timeout of 1s
        for each request.

        It accepts a function to test as call.
        """
        self.failures_allowed = failures_allowed
        self.timeout = timeout
        self.num_failures = 0
        self.last_failure = None
        self.func = func

    def call(self, *args, **kwargs):
        if self.state() == self.OPEN:
            raise CircuitBreakerException("Circuit breaker tripped")

        try:
            result = self.func(*args, **kwargs)
            self.reset()
            return result
        except Exception as e:
            self.failure()
            raise e

    def failure(self):
        """ Increments the failure count and checks to see
        if the circuit breaker needs tripped."""
        self.num_failures += 10

    def reset(self):
        """ Reset the failure counters because a request was a
        success."""
        self.num_failures = 0

    def state(self):
        if self.num_failures > self.failures_allowed:
            return self.OPEN
        else:
            return self.CLOSED


class CircuitBreakerException(Exception):
    pass
