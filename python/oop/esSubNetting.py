from math import log2, ceil

def dec2bin(ip):
    l = ip.split('.')
    l_bin = [str(bin(int(n)))[2:] for n in l]
    return '.'.join(['0' * (8 - len(num)) + num for num in l_bin])

def bin2dec(ip):
    return ".".join([str(int(n, 2)) for n in ip.split(".")])

def insPunti(ip):
    for k in range(1, 4):
        i = k * 9 - 1
        ip = ip[:i] + "." + ip[i:]
    return ip

def getStrIpSuccessivo(ip):
    ipTemp = ''.join(dec2bin(ip).split('.'))
    ind = -1
    while(ipTemp[ind] != '0'):
        ind = ind - 1
    
    nCifreFinali = -ind - 1
    nextIp = ipTemp[:(len(ipTemp) - nCifreFinali - 1)] + '1' + '0' * nCifreFinali

    return bin2dec(insPunti(nextIp))

class IPaddress():
    def __init__(self, ip, subnetmask = 24):
        self.ip = ip
        self.subnet = subnetmask
        self.setIpRete()
        self.setIpBroadcast()

    def setIpRete(self):
        n = 32 - self.subnet
        ipTemp = ''.join(dec2bin(self.ip).split('.'))
        _ipT = insPunti(ipTemp[:self.subnet] + '0' * n)
        self.ipRete = bin2dec(_ipT)
    
    def setIpBroadcast(self):
        n = 32 - self.subnet
        ipTemp = ''.join(dec2bin(self.ip).split('.'))
        _ipT = insPunti(ipTemp[:self.subnet] + '1' * n)
        self.ipBroadcast = bin2dec(_ipT)
    
    def getIpSuccessivo(self):
        ipTemp = ''.join(dec2bin(self.ipBroadcast).split('.'))
        ind = -1
        while(ipTemp[ind] != '0'):
            ind = ind - 1
        
        nCifreFinali = -ind - 1
        nextIp = ipTemp[:(len(ipTemp) - nCifreFinali - 1)] + '1' + '0' * nCifreFinali

        return IPaddress(bin2dec(insPunti(nextIp)), self.subnet)
    
    def getSottoReti(self, nSottoReti):
        lista = []
        newSubnet = self.subnet + ceil(log2(nSottoReti))
        ipAtt = IPaddress(self.ipRete, newSubnet)
        for _ in range(nSottoReti):
            lista.append(ipAtt)
            ipAtt = ipAtt.getIpSuccessivo()

        return lista


def main():
    ip = input('indirizzo ip: ')
    submask = int(input('subnetmask: /'))
    ipStarter = IPaddress(ip, submask)

    nSottoReti = int(input('sottoreti: '))
    l = ipStarter.getSottoReti(nSottoReti)

    for i, ip in enumerate(l):
        print(f"sottorete {i + 1}:")
        print(f"- ip di rete: {ip.ipRete}")
        print(f"- ip di broadcast: {ip.ipBroadcast}")
        print(f"- subnetmask: /{ip.subnet}")

if __name__ == '__main__':
    main()