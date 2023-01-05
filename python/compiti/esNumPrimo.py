def isPrimo(n):
    for k in range(2, int(n ** 0.5) + 1):
        if not n % k:
            return False
    return True

l = [n for n in range(1, 101) if isPrimo(n)]

print(l)