NLINE = 10

fp = open("file_p73es20.txt", 'w')

mat = [[n * i for n in range(NLINE)] for i in range(NLINE)]

for l in mat:
    for c in l:
        print(c, end='\t')
        fp.write(f"{c}\t")
    print('')
    fp.write('\n')

fp.close()