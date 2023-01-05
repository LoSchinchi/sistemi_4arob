from random import randint

def addizione(a, b):
    return a + b
def sottrazione(a, b):
    return a - b
def moltiplicazione(a, b):
    return a * b
def divisione(a, b):
    return a / b

n1 = int(input("numero 1: "))
n2 = int(input("numero 2: "))

diz = { 0: addizione, 1: sottrazione, 2: moltiplicazione, 3: divisione}

print(diz[randint(0, 3)](n1, n2))
