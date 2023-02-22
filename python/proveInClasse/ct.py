import random
import time

n = 1000000
tIniz = time.time()
l = [random.uniform(0, 1) for _ in range(n)]

nMax = -1
for n in l:
    if n > nMax:
        nMax = n
#maxN = max(l)
tFine = time.time()

print(nMax)
print(f"n = {n}")
print(f"tempo impiegato: {tFine - tIniz}")