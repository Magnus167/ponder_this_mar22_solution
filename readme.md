# Read Me
## Introduction

A program to solve the [March 2022 Ponder This challenge](https://research.ibm.com/haifa/ponderthis/challenges/March2022.html) [(alt link)](https://web.archive.org/web/20220518044959/https://research.ibm.com/haifa/ponderthis/challenges/March2022.html).
Uses python

The challenge is a modified version of Wordle, which uses prime numbers instead of english words; and slightly modified rules.

example call:

`python solver.py <num_digits> <reduce_set>`

`num_digits` : for the number of digits in each prime

`reduce_set` : passing any character as an arg here will remove any primes/words that have duplicate digits/characters.


## Original Problem Statement

In the popular game Wordle, players attempt to guess a five-letter word. After each guess, the colors of the letter tiles change to reflect the guess. Green tiles represent a letter in the correct place; yellow tiles represent a letter present in the solution, but not in that place; and gray tiles represent a letter not present in the word at all. The submitted word has to be present in the game's dictionary; one cannot simply choose arbitrary letters.

We discuss a similar game, where instead of guessing a five-letter word, we attempt to guess an `n` digit prime number (in the decimal system). As in the original Wordle, the guess must be a prime number. For this game, we want to pick a "good" initial guess. While there can be several ways to define "good" in this context, we choose the following: After the first guess, we obtain some pattern of green/yellow/gray connected to the digits in our guess. This pattern excludes some of the possible `n` digit prime numbers. Let `f(p, q)` be the number of remaining possible solutions after the first guess, given that `p` was the guess and `q` is the solution.

For example, if the solution is the four-digit prime number 4733 and our initial guess was 3637, the resulting pattern will be yellow-gray-green-yellow, and the possible remaining solutions are 1733, 2731, 4733, 7039, 7331, 7333, 7433, 7933, 8731, 9733, 9739.

Note the following exclusions from the possible solution set of the example:
* 6733 is excluded since 6 was gray, and so 6 is guaranteed not to be part of the solution.
* 3733 is excluded since the first '3' was yellow, and so 3 is guaranteed not to be the first digit.
* 2239 is excluded since 7 was yellow, but is not present at all in 2239.
So in this case, `f(3637, 4733)=11`. An even better initial guess would have been 8731, which would have resulted in `f(8731, 4733)=8` .

For `n` digits, we wish to find a prime number `p` which minimizes the expected value of `f(p,q)` for a uniformly generated prime `q` . 
That is, we wish to minimize 

![image](https://user-images.githubusercontent.com/23239946/169637697-e5ccecd1-1df7-433c-be8e-5503b93e40d5.png)


E[p]\triangleq\sum_{q\in P}\frac{f(p,q)}{|P|} 

where `p` is the set of `n`digit primes.

Your goal: Find this p for `n=5` and compute E[p] . Return those two values as the solution.

