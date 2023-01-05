class Quadrato():
    def __init__(self, x, y, lung):
        self.punto_1 = {'x': x, 'y': y} #punto alto sinistra
        self.l = lung
    
    def getPerimetro(self):
        return self.l * 4
    
    def getArea(self):
        return self.l ** 2

    def isPuntoInQuad(self, x, y):
        return self.punto_1['x'] <= x <= self.punto_1['x'] + self.l and self.punto_1['y'] - self.l <= y <= self.punto_1['y'] 

def main():
    q = Quadrato(1, 3, 3)

    print(f'perimetro: {q.getPerimetro()}')
    print(f'area: {q.getArea()}')

    if(q.isPuntoInQuad(2, 2)):
        print('il punto è nel quadrato')
    else:
        print('il punto non è nel quadrato')

if __name__ == '__main__':
    main()
