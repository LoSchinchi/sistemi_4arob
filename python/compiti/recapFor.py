lista1 = ['a', 'b', 'c', 'd']
lista2 = [1, 2, 3, 4]

print('for su', lista1, 'C-style:')
for k in range(len(lista1)):
    print(f"lista1[{k}] = '{lista1[k]}'")

print('\nfor su', lista1, 'python-style:')
for e in lista1:
    print(f"e = '{e}'")

print('\nfor su', lista1, 'con enumerate:')
for i, e in enumerate(lista1):
    print(f"i = {i}, e = '{e}'")

print('\nfor su', lista1, 'e', lista2, 'Python-style (zip):')
for e1, e2 in zip(lista1, lista2):
    print(f"e1 = '{e1}', e2 = {e2}")

print('\nfor su', lista1, 'e', lista2, 'C-style (range):')
for i in range(len(lista1)):
    print(f"lista1[{i}] = '{lista1[i]}', lista2[{i}] = {lista2[i]}")

diz = {}
for e1, e2 in zip(lista1, lista2):
    diz[e2] = e1

print('\nfor su', diz, 'usando items():')
for k, v in diz.items():
    print(f"k = {k}, v = '{v}'")

print('\nfor su', diz, 'senza usare items():')
for k in diz:
    print(f"k = {k}, diz[{k}] = '{diz[k]}'")
