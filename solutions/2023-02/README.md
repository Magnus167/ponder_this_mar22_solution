This problem is based on a suggestion by Frank Mayer - thanks Frank!


Alice and Bob play the following weird dice game using a standard set of 6 D&D dice, i.e., dice with values


- 1, . . . , 4

- 1, . . . , 6

- 1, . . . , 8

- 0, . . . , 9

- 1, . . . , 12

- 1, . . . , 20

At each round, they throw the dice and sum their values. All six dice need to be rolled once each round, and it doesn’t matter who rolls the dice. What matters in deciding who wins is the sum.


Alice wins if the result is a prime number, and Bob wins if the result is a nonprime even number. Otherwise, the result of the round is a draw.


The winner of the game is the first player to reach N consecutive wins.


Your goal: For N=13 , find the probability that Alice wins the game.

A Bonus "*" will be given for finding the probability that Alice wins given that N=300 but the rules have changed and Bob now wins if the result is a nonprime odd number.