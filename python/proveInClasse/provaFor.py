lista = [110, 12, 405, 23, 66]
min, max = lista[0], lista[0]

for el in lista[1:]:
    if el < min:
        min = el
    elif el > max:
        max = el
    else:
        pass
    

print(f"min: {min}, max: {max}")