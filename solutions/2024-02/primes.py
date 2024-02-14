from typing import List, Dict, Tuple, Any, Generator
import timeit

import numpy as np
from numba import jit
from itertools import permutations
import pandas as pd
import time
from functools import lru_cache


# sieve of eratosthenes
@lru_cache(maxsize=None)
def is_prime(n):
    """
    Check if a number is prime.

    Args:
        n (int): The number to check.

    Returns:
        bool: True if the number is prime, False otherwise.
    """
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


from typing import List


def _sieve(n: int) -> List[int]:
    """
    Sieve of Eratosthenes algorithm to find all prime numbers up to n.

    Args:
        n (int): The upper limit for finding prime numbers.

    Returns:
        List[int]: A list of prime numbers up to n.
    """
    primes = []
    sieve = [True] * (n + 1)
    for p in range(2, n + 1):
        if sieve[p]:
            primes.append(p)
            for i in range(p, n + 1, p):
                sieve[i] = False
    return primes


@jit(nopython=True)
def _sieve_numpy(n: int) -> np.ndarray:
    """
    Sieve of Eratosthenes algorithm implemented using numpy.

    Args:
        n (int): The upper limit of the range to generate prime numbers.

    Returns:
        np.ndarray: An array containing all the prime numbers up to `n`.
    """
    sieve: np.ndarray = np.ones(n + 1)
    sieve[0:2] = 1
    for p in range(2, n + 1):
        if sieve[p]:
            sieve[p * p : n + 1 : p] = 1
    return np.flatnonzero(sieve)


@lru_cache(maxsize=None)
def get_primes(n: int) -> List[int]:
    """
    Get all prime numbers up to `n`.

    Args:
        n (int): The upper limit for finding prime numbers.

    Returns:
        List[int]: A list of prime numbers up to `n`.
    """
    return _sieve_numpy(n).tolist()


def generate_primes(n: int = -1) -> Generator[int, Any, Any]:
    """Generate an infinite sequence of prime numbers using a cached primality check.

    Args:
        n (int, optional): The number of primes to generate. Defaults to -1.

    Yields:
        Generator[int, Any, Any]: A generator for prime numbers.
    """

    q = 2  # Starting number
    # n<0 means infinite sequence, so while (n<0) is always True
    # q<n means we stop after n primes, and isn't going to trigger if n<0
    while (n < 0) or (q < n):
        if is_prime(q):
            yield q
        q += 1


## Test the speed of the different implementations


def timefunc(func, n):
    istr = f"Testing {func.__name__} with n={n}"
    print("=" * len(istr))
    print(istr)
    print(" > ", timeit.timeit(lambda: func(n), number=1), "seconds")
    print("=" * len(istr))


if __name__ == "__main__":
    import argparse

    N_INPUT = 10000

    parser = argparse.ArgumentParser(description="Run the prime number functions.")
    parser.add_argument(
        "--n",
        type=int,
        default=N_INPUT,
        help="The upper limit for finding prime numbers.",
    )

    _print_str = f"Running examples - with `n` set to {N_INPUT}"
    print(_print_str)
    print("-" * len(_print_str))
    for func in [_sieve, _sieve_numpy, is_prime, get_primes]:
        timefunc(func, N_INPUT)
        print()
