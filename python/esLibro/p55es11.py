x = [0, 1, 2, 3, 5, 6, 7, 8]
l = len(x) // 2
l1 = x[:l]
l2 = x[l:]
l1.append(5)

print(l1)
print(l2)