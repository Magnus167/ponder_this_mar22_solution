from typing import List, Tuple, Union, Any, overload, Callable, Optional

from primes import is_prime
from dice import get_unique_throw_sums_dict, DICES_FACES, throw_sum


def primeNumber(x):
    return is_prime(x)


def evenNumber(x):
    return x % 2 == 0


def oddNumber(x):
    return x % 2 != 0


def oddPrimeNumber(x):
    return oddNumber(x) and primeNumber(x)

def game_run(nwins: int, playerAWins: Callable, playerBWins: Callable):
    throw_sums: List[int] = []
    winner: Optional[bool] = None
    while winner is None:
        throw_sums.append(throw_sum(DICES_FACES))
        if len(throw_sums) >= nwins:
            if all(playerAWins(x) for x in throw_sums[-nwins:]):
                winner = True
            elif all(playerBWins(x) for x in throw_sums[-nwins:]):
                winner = False
    return [['A', 'B'][winner], len(throw_sums)] 

def gameX(nwins: int, playerAWins: Callable, playerBWins: Callable):
    gameResults = get_unique_throw_sums_dict(DICES_FACES)

    pAWinsCount = 0
    pBWinsCount = 0
    totalThrows = 0
    for valx, sumx in gameResults.items():
        totalThrows += sumx
        if playerAWins(valx):
            pAWinsCount += sumx
        elif playerBWins(valx):
            pBWinsCount += sumx

    # print the results/totals
    print(f"Player A wins: {pAWinsCount} ({pAWinsCount/totalThrows:.2%})")
    print(f"Player B wins: {pBWinsCount} ({pBWinsCount/totalThrows:.2%})")
    print(f"Total throws: {totalThrows}")

gameX(13, primeNumber, evenNumber)