DIZ_NUCL = {'adenina': 'A', 'timina': 'T', 'guanina': 'G', 'citosina': 'C'}  # dizionario con i nucleotidi e la lettera che li rappresenta
SEQ_SPIKE = 'ATGTTTGTTTTT' # sequenza della proteina spike

def main():
    f = open('covid-19_gen1.txt', 'r')
    stringCompleta = ''.join(''.join(f.readlines()).split('\n')) # unione di una lista = a stringa unione della lista delle righe del file divisa ad ogni '\n
    print(f"sequenza: {stringCompleta}")
    f.close()

    for k, v in DIZ_NUCL.items():
        print(f"il nucleotide {k} è contenuto {stringCompleta.count(v)} volte")     # utilizzo di count perchè ritorna il numero delle occorrenze

    if SEQ_SPIKE in stringCompleta: # controlla se c'è la stringa
        print(f"nel file la sequenza '{SEQ_SPIKE}' è all'indice {stringCompleta.index(SEQ_SPIKE)}")
    else:
        print(f"nel file non è presente la sequenza '{SEQ_SPIKE}'")


if __name__ == '__main__':
    main()
