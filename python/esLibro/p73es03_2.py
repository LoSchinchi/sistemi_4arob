from random import randint

n1 = int(input("numero 1: "))
n2 = int(input("numero 2: "))

diz = { 0: lambda n1, n2: n1 + n2, 
        1: lambda n1, n2: n1 - n2, 
        2: lambda n1, n2: n1 * n2,
        3: lambda n1, n2: n1 / n2}

print(diz[randint(0, 3)](n1, n2))
