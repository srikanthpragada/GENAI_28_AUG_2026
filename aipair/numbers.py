"""Utility functions for checking common number properties.

This module contains helper functions for identifying whether an integer is
prime or perfect.
"""


def isprime(num: int) -> bool:
    """Return True if the given integer is a prime number.

    A prime number is a positive integer greater than 1 that has no divisors
    other than 1 and itself. This function checks possible divisors from 2 up to
    the square root of the value, which makes it efficient for typical inputs.

    Args:
        num: The integer to evaluate.

    Returns:
        True when the value is prime; False otherwise, including for values less
        than or equal to 1 and for composite numbers.

    Examples:
        >>> isprime(2)
        True
        >>> isprime(17)
        True
        >>> isprime(1)
        False
        >>> isprime(12)
        False
    """
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True


def isperfect(num: int) -> bool:
    """Return True if the given integer is a perfect number.

    A perfect number is one whose proper positive divisors sum to the number
    itself. For example, 6 is perfect because 1 + 2 + 3 = 6.

    Args:
        num: The integer to evaluate.

    Returns:
        True if the sum of all positive divisors less than the number equals the
        number; otherwise False.

    Examples:
        >>> isperfect(6)
        True
        >>> isperfect(28)
        True
        >>> isperfect(10)
        False
        >>> isperfect(0)
        False
    """
    if num <= 0:
        return False
    divisors_sum = sum(i for i in range(1, num) if num % i == 0)
    return divisors_sum == num


