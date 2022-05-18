# %%
from typing import *
from collections import defaultdict
import random 
import functools
import numpy as np
from tqdm import tqdm
from joblib import Parallel, delayed
import sys
import time

cache = functools.lru_cache(None)

Word  = str # A word is a lower-case string of five different letters
Reply = str # A reply is five characters taken from 'GY.': Green, Yellow, Miss
Green, Yellow, Miss = 'GY.'

''' digits from args'''

start_time = time.time()
digits = 4
reducedOnly = len(sys.argv)>2
try:
    digits = int(sys.argv[1])
    # reducedOnly = len(sys.argv)>2
except:
    digits = 4


# digits = 7



# %%

def prime_gen(digits):
    """
    Generate a list of prime numbers in the range [low, high]
    """
    low = 10**(digits-1)
    high = low*10
    primes = []
    composites = set()
    k = 2
    while k <= high:
        if k not in composites:
            primes.append(k) # yield k, 
            for j in range(k * k, high + 1, k):
                composites.add(j)
        k += 1
    i=0
    while primes[i]<low:
        i+=1
    return primes[i:]

def reduced_primes_gen(digits):
    reduced_primes = []
    prx = prime_gen(digits)
    for prime in prx:
        if len(set(str(prime))) == len(str(prime)):
            reduced_primes.append(prime)

    return reduced_primes

def save_primes(digits):
    primes = prime_gen(digits)
    with open('primes{}Nums.txt'.format(digits), 'w') as f:
        f.write('\n'.join(map(str, primes)))

def save_reduced_primes(digits):
    primes = prime_gen(digits)
    reduced_primes = reduced_primes_gen(digits)
    with open('primes{}Reduced.txt'.format(digits), 'w') as f:
        f.write('\n'.join(map(str, reduced_primes)))


save_primes(digits)
save_reduced_primes(digits)

words = open('primes{}Nums.txt'.format(digits)).read().upper().split()
reducedWords = open('primes{}Reduced.txt'.format(digits)).read().upper().split()
csset = range(digits)






# %%
@cache
def reply_forOld(guess, target) -> Reply: 
    "The five-character reply for this guess on this target in Wordle."
    # We'll start by having each reply be either Green or Miss ...
    reply = [Green if guess[i] == target[i] else Miss for i in csset]
    # ... then we'll change the replies that should be yellow
    counts = Counter(target[i] for i in csset if guess[i] != target[i])
    for i in csset:
        if reply[i] == Miss and counts[guess[i]] > 0:
            counts[guess[i]] -= 1
            reply[i] = Yellow
    return ''.join(reply)

@cache
def reply_for(guess, target) -> Reply:    
    reply = [Yellow if guess[i] in target else Miss for i in csset]
    reply = [Green if guess[i] == target[i] else reply[i] for i in csset]
    return ''.join(reply)



@cache
def isAt(charx, index) -> List[bool]:
    "Is charx at index in the word?"
    return [charx == word[index] for word in words]

@cache
def isNotAt(charx, index) -> List[bool]:
    "Is charx not at index in the word?"
    return np.invert(isAt(charx, index))

@cache
def isIn(char) -> List[bool]:
    "Is char in the word?"
    return [char in word for word in words]

@cache
def isNotIn(char) -> List[bool]:
    "Is char not in the word?"
    return np.invert(isIn(char))



@cache
def meta_reply(guess, guess_reply) -> int:
    if guess_reply.count(Green) == len(guess_reply):
        return 0     
    andArr = np.ones(len(words), dtype=bool)
    
    yellowFilter    = np.ones(  len(words) , dtype=bool)
    grayFilter      = np.zeros( len(words) , dtype=bool)
    greenMask       = np.ones(  (len(words), len(guess))  , dtype=bool)
    grayNums        = list(set([guess[n] for n in csset if guess_reply[n] == Miss]))
    yellowNums      = list(set([guess[n] for n in csset if guess_reply[n] == Yellow]))

    while len(yellowNums) > 0:
        yNum = yellowNums.pop()
        yellowFilter = np.logical_and(yellowFilter, isIn(yNum))
    while len(grayNums) > 0:
        grayNum = grayNums.pop()
        grayFilter = np.logical_or(grayFilter, isIn(grayNum))


    for I in (csset):
        if guess_reply[I] == Green: 
            greenMask[:, I] = isAt(guess[I], I)
        else:
            greenMask[:, I] = isNotAt(guess[I], I)
    # greenFilter = np.all(greenMask, axis=1)      
    # print(type(~grayFilter & yellowFilter & np.all(greenMask, axis=1)))
    return np.sum(~grayFilter & yellowFilter & np.all(greenMask, axis=1))




# %%
# load cache

def rForC(guess):
    for t in words:
        reply_for(guess, t)


print('caching in/at conditions')
u = []
for I in tqdm(range(0, 10)):
    u = isIn(str(I)), isNotIn(str(I))
    for J in csset:
        u = isAt(str(I), J), isNotAt(str(I), J)


print('caching reply_for')

# Parallel(n_jobs=-1, prefer="threads")(delayed(rForC)(guess) for guess in tqdm(words))
# for guess in tqdm(words):
#     for t in words:
#         reply_for(guess, t)



print('cache done')



# %%
@cache
def bin_sizes(guess) -> List[int]: 
    """Sizes of the bins when `words` are partitioned by `guess`."""
    ctr = Counter(reply_for(guess, target) for target in words)
    return list(ctr.values())

def top(n, items, key=None) -> dict:
    """Top (best) `n` {item: key(item)} pairs, as ranked by `key`."""
    return {item: key(item) for item in sorted(items, key=key, reverse=True)[:n]}

def bot(n, items, key=None) -> dict:
    """Bottom (worst) `n` {item: key(item)} pairs, as ranked by `key`."""
    return {item: key(item) for item in sorted(items, key=key)[:n]}

def wins(guess) -> int: 
    """The number of guaranteed wins on the 2nd guess (after `guess` first)."""
    return bin_sizes(guess).count(1)

def expected_wins(guess):
    """The expected number of wins on the 2nd guess (after `guess` first).
    With n words in a bin, you have a 1 / n chance of guessing the right one."""
    return sum(1 / n for n in bin_sizes(guess))

@cache 
def reply_cache(guess):
    for target in words:
        meta_reply(guess, reply_for(guess, target))

# @cache
def sum_replies(guess):
    """The expected number of wins on the 2nd guess (after `guess` first).
    With n words in a bin, you have a 1 / n chance of guessing the right one."""
    return sum(meta_reply(guess, reply_for(guess, target)) for target in words)


# %%

print('building reply cache')
wordSet = words
if reducedOnly:    
    wordSet = reducedWords
dispatch_all = False
preDispatch = 'all' if dispatch_all else 'n_jobs'

res_arr = Parallel(n_jobs=-1, prefer="threads", pre_dispatch=preDispatch  )(delayed(sum_replies)(guess) for guess in tqdm(wordSet))


# %%
finRes= []
i = 0
for guess in tqdm(wordSet):
    finRes.append([wordSet[i] ,sum_replies(guess)])
    i += 1

''' sort by second element '''
finRes.sort(key=lambda x: x[1])

with open('outFile{}.txt'.format(digits), 'w') as f:
    for u in finRes:
        f.write('{} \t {}\n'.format(u[0], u[1]))
        print(u)


print('Save outfile')
print('Running Time = ', time.time() - start_time)


