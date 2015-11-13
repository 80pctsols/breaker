import datetime

class CircuitBreaker(object):
    """A circuit breaker which handles requests, timeouts
    and other failures to help with resiliency.

    Attributes:
      failures_allowed: number of failures in a row to trip circuit
      timeout: time in milliseconds before a request times out
    """
    OPEN = "open"
    CLOSED = "closed"

    def __init__(self, func, failures_allowed=10, timeout=10):
        """ Create a CircuitBreaker that has a default of 10
        failures in a row to be tripped, and a timeout of 1s
        for each request.

        Timeout is measured in seconds

        It accepts a function to test as call.
        """
        self.failures_allowed = failures_allowed
        self.timeout = timeout
        self.num_failures = 0
        self.last_failure = None
        self.func = func

    def call(self, *args, **kwargs):
        if self.state() == self.OPEN and not self.is_half_open():
            raise CircuitBreakerException("Circuit breaker tripped")

        try:
            result = self.func(*args, **kwargs)
            self.reset()
            return result
        except Exception as error:
            self.failure()
            raise error

    def state(self):
        """ Current state of ciruit breaker system """
        if self.num_failures > self.failures_allowed:
            return self.OPEN
        else:
            return self.CLOSED

    def is_half_open(self):
        """ Check to see if we should test the connection again """
        if self.last_failure:
            now = datetime.datetime.now()
            difference = now - self.last_failure
            return difference.seconds > self.timeout
        return False

    def reset(self):
        """ Reset the failure counters because a request was a
        success."""
        self.num_failures = 0

    def failure(self):
        """ Increments the failure count and checks to see
        if the circuit breaker needs tripped."""
        self.num_failures += 1
        self.last_failure = datetime.datetime.now()


class CircuitBreakerException(Exception):
    pass
