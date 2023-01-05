def readFile(name):
    file = open(name, 'r')
    dizMat = {'id': [], 'nomi': []}
    lista_righe = file.readlines()

    for line in lista_righe[1:]:
        arr = line[:-1].split(',')
        dizMat['id'].append(int(arr[0]))
        dizMat['nomi'].append(arr[1][1:])

    file.close()
    return dizMat

def main():
    diz = readFile('dati.csv')
    print(diz)

    def namePerId(id, diz):
        for i, e in enumerate(diz['id']):
            if e == id:
                return diz['nomi'][i]

    id = int(input('id: '))

    print(f"matematico: {namePerId(id, diz)}")


if __name__ == '__main__':
    main()
