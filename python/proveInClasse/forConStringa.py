stringa = input("stringa: ")

strAlf = "abcdefghilmnopqrstuvz"
codif = {}
for i in range(-1, len(strAlf) - 1):
    codif[strAlf[i]] = strAlf[i + 1]
codif[' '] = ' '

newCodif = {}
for key, value in codif.items():
    newCodif[value] = key

newStr = ''

for let in stringa:
    newStr += newCodif[let]
print(newStr)