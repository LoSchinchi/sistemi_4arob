def bin2dec(ipBin):
    return ".".join([str(int(n, 2)) for n in ipBin.split(".")])

def dec2bin(ipDec):
    l = ipDec.split('.')
    l_bin = [str(bin(int(n)))[2:] for n in l]
    l_bin = '.'.join(['0' * (8 - len(num)) + num for num in l_bin])

class IPaddress(): # broadcast, primo e ultimo utilizzabili
    def __init__(self, ip_stringa):
        self.ip_notazione_dec = ip_stringa
        self.ip_notazione_bin = None
        self.ip_binario = None
    
    def dec2bin(self):
        l = self.ip_notazione_dec.split('.')
        l_bin = [str(bin(int(n)))[2:] for n in l]
        self.ip_notazione_bin = '.'.join(['0' * (8 - len(num)) + num for num in l_bin])
        self.ip_binario = ''.join(self.ip_notazione_bin.split('.'))

    def toList(self):
        return [int(n) for n in self.ip_notazione_dec.split(".")]

    def getIpBroadcast(self, subnetMask='/24'):
        s = int(subnetMask[1:])
        
        self.dec2bin()
        ipBroadcast = self.ip_binario[:s] + '1' * s
        for k in range(1, 4):
            i = k * 9 - 1
            ipBroadcast = ipBroadcast[:i] + "." + ipBroadcast[i:]
        return bin2dec(ipBroadcast)
    
    def getIpRete(self, subnetMask='/24'):
        s = int(subnetMask[1:])
        
        self.dec2bin()
        ipBroadcast = self.ip_binario[:s] + '0' * s
        for k in range(1, 4):
            i = k * 9 - 1
            ipBroadcast = ipBroadcast[:i] + "." + ipBroadcast[i:]
        return bin2dec(ipBroadcast)


def main():
    #inp_subnetMask = int(input("subnet mask: /"))

    ip = IPaddress('192.168.0.123')
    print(ip.ip_notazione_dec)
    print(ip.toList())
    ip.dec2bin()
    print(ip.ip_notazione_bin)
    print(ip.getIpBroadcast('/26'))

if __name__ == '__main__':
    main()