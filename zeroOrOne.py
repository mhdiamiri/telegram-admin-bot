import random

ones = 0
N = 10000
for i in range(1, N):
    if random.randrange(0,2) == 1:
        ones += 1
print((ones/N)*100)