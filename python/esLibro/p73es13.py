class Robot():
    def __init__(self, name, massa, isUmanoide):
        self.name = name
        self.massa = massa
        self.isUmanoide = isUmanoide
    
    def printName(self):
        print(f'nome del robot: {self.name}')
    
    def isPericoloso(self):
        return self.massa > 100 and self.isUmanoide
    
def main():
    rob = Robot("gallo", 90, True)
    rob.printName()
    print(rob.isPericoloso())

if __name__ == '__main__':
    main()