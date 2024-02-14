from dice import (
    expand_dice_tuple,
    _get_combinations,
    _get_combos_cache,
    get_combinations,
    throw,
    throw_sum,
    get_unique_throw_sums,
    get_unique_throw_sums_dict,
)
from primes import (
    is_prime,
    _sieve,
    _sieve_numpy,
    get_primes,
    generate_primes,
    timefunc,
)

from game import game_run
import pandas as pd

def primeNumber(x):
    return is_prime(x)


def evenNumber(x):
    return x % 2 == 0


def oddNumber(x):
    return x % 2 != 0


def oddPrimeNumber(x):
    return oddNumber(x) and primeNumber(x)


def logicX():
    results = []
    for i in range(100):
        results.append(game_run(13, primeNumber, evenNumber))

    df = pd.DataFrame(results, columns=["Winner", "Throws"])
    # group by winner and average throws
    print(df.groupby("Winner").mean())

logicX()

