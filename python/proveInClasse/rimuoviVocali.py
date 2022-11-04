vocali = ("a", "e", "i", "o", "u")

stringa = "ciao"
newStr = ""
for c in stringa:
    if not c in vocali:
        newStr += c 
print(newStr)
