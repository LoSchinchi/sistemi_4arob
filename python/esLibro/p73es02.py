n = int(input("Numero: "))

nDiv = ""
if n % 2 == 0:
    nDiv += "2 "
if n % 3 == 0:
    nDiv += "3 "
if n % 5 == 0:
    nDiv += "5"

if nDiv == "":
    print("non è divisibile")
else:
    print("divisibile per", nDiv)