def getStrConZeri(n):
    s = str(bin(int(n)))[2:]
    return '0' * (8 - len(s)) + s

ip = input("indirizzo ip: ")
subnetMask = int(input("subnet mask: /"))
POT_N_HOST = 32 - subnetMask

arrIp = "".join([getStrConZeri(n) for n in ip.split(".")])
ipRete = arrIp[:subnetMask] + "0" * POT_N_HOST
ipBroadcast = arrIp[:subnetMask] + "1" * POT_N_HOST

for k in range(1, 4):
    i = k * 9 - 1
    ipRete = ipRete[:i] + "." + ipRete[i:]
    ipBroadcast = ipBroadcast[:i] + "." + ipBroadcast[i:]

ipRete = ".".join([str(int(n, 2)) for n in ipRete.split(".")])
ipBroadcast = ".".join([str(int(n, 2)) for n in ipBroadcast.split(".")])
print(f"ip di rete: {ipRete}\nip di broadcast: {ipBroadcast}")
