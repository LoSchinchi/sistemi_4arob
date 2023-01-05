PATH_FILE_READER = "./4AROB_GITA.csv"
QUOTA = 100
MAX_INC = 2200
NOME_DA_CERCARE = "Barale"

def readFile():
    fp = open(PATH_FILE_READER, 'r')
    diz = {'nomi': [], 'quota': []}

    for l in fp.readlines():
        _list = l[:-1].split(';')
        diz['nomi'].append(_list[1])
        diz['quota'].append(int(_list[2]))

    fp.close()
    return diz

def printIncassi(diz):
    n = 0
    for e in diz['quota']:
        n += e

    if n == MAX_INC:
        print(f"incasso: {n}")
    elif n < MAX_INC:
        print(f"mancano ancora {MAX_INC - n} euro a {MAX_INC} ({n})")
    else:
        print(f"ci sono {n - MAX_INC} euro in più di {MAX_INC} ({n})")

def ricercaNome(diz):
    qGen = 0
    for i, e in enumerate(diz['nomi']):
        if e == NOME_DA_CERCARE:
            qGen += diz['quota'][i]
    
    if qGen > QUOTA :
        print(f"l'alunno {NOME_DA_CERCARE} ha pagato {qGen - QUOTA}in più della quota prevista di {QUOTA}")
    elif qGen == QUOTA :
        print(f"l'alunno {NOME_DA_CERCARE} ha pagato la quota prevista di {QUOTA}")
    else:
        print(f"l'alunno {NOME_DA_CERCARE} ha pagato {QUOTA - qGen} in meno della quota prevista di {QUOTA}")

def indAlunno(arr, nome):
    for i, n in enumerate(arr):
        if n == nome:
            return i

def setAlunni_2(diz):
    diz_2 = {'nomi': [], 'quota': []}

    for i, nome in enumerate(diz['nomi']):
        if nome in diz_2['nomi']:
            diz_2['quota'][indAlunno(diz_2['nomi'], nome)] += diz['quota'][i]
        else:
            diz_2['nomi'].append(nome)
            diz_2['quota'].append(diz['quota'][i])
    return diz_2

def printAlunni(diz):
    for i, n in enumerate(diz['nomi']):
        if diz['quota'][i] == QUOTA:
            print(f"alunno {n} -> quota pagata: {diz['quota'][i]}")
        else:
            print(f"alunno {n} -> quota pagata: {diz['quota'][i]} --- da controllare")

def main():
    diz = readFile()
    printIncassi(diz)
    ricercaNome(diz)
    newDiz = setAlunni_2(diz)
    printAlunni(newDiz)

if __name__ == '__main__':
    main()
