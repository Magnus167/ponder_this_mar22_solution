from typing import List, Union, Any, Generator, Dict, Tuple

from solve.primes import is_prime, get_primes, generate_primes

DICES_FACES = [
    (1, 4),
    (1, 6),
    (1, 8),
    (0, 9),
    (1, 12),
    (1, 20),
]

DICES = [list(range(faces[0], faces[1] + 1)) for faces in DICES_FACES]

