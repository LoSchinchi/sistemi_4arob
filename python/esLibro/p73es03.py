"""
somma = lambda n1, n2: n1 + n2
sottr = lambda n1, n2: n1 - n2
molt = lambda n1, n2: n1 * n2
div = lambda n1, n2: n1 / n2
"""

op = int(input("operazione: "))
n1 = int(input("numero 1: "))
n2 = int(input("numero 2: "))

diz = { 0: lambda n1, n2: n1 + n2, 
        1: lambda n1, n2: n1 - n2, 
        2: lambda n1, n2: n1 * n2,
        3: lambda n1, n2: n1 / n2}
print(diz[op](n1, n2))
