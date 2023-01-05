def isPrimo(n):
    for k in range(2, int(n ** 0.5) + 1):
        if not n % k:
            return False
    return True

l = []
for i in range(1, 100):
    if(isPrimo(i)):
        l.append(i)     
print(l)

l = [i for i in range(1, 100) if isPrimo(i)]
print(l)