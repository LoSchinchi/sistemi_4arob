from random import randint
NLANCI = 10

def main():
    fp = open('file_p73es19.txt', 'w')

    lAlice = [randint(1, 6) for _ in range(NLANCI)]
    lBob = [randint(1, 6) for _ in range(NLANCI)]

    fp.write('Alice\tBob\n')

    for a, b in zip(lAlice, lBob):
        fp.write(f"{a}\t\t{b}\n")
        print(f"Alice: {a}, Bob: {b}")

    fp.close()

if __name__ == '__main__':
    main()