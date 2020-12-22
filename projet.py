import sys

# file src = sys.argv[1]
# file dst = sys.argv[2]

# Test si on peut ouvrir le fichier donné dans l'executable
try:
	f = open(sys.argv[1], "r")
except:
    print("Erreur: Le fichier source n'existe pas.")
    exit()

d = open(sys.argv[2], "w") # Ouverture fichier dans lequel on va écrire

L = list() # Contient les données de la trame
Lres = list() # Test

# Collecte les données contenues dans le fichier et les insère dans une liste : fonctionne avec ou sans saut à la ligne
for line in f:
	L.extend(line.split())

print(L)

def LStrToInt(L):
	""" list[str] -> str : Transforme une liste d'hexa en liste d'entier"""
	res = list()
	for e in L:
		res.append(int("0x"+e, base=16))
	return res

def LStrToIp(L):
	""" list[str] -> str : Transforme une liste d'hexa en adresse ip en str"""
	L = LStrToInt(L)
	res = ""
	for e in L:
		res += str(e)+"."
	res = res[:len(res)-1]
	return  res

def LStrToMac(L):
	""" list[str] -> str : Transforme une liste d'hexa en adresse MAC en str"""
	res = ""
	for e in L:
		res += str(e)+":"
	res = res[:len(res)-1]
	return  res

def LStrToPort(L):
	""" list[str] -> str : Transforme une liste d'hexa en numéro de port en str"""
	res = 0
	tmp = LStrToInt(L)
	for e in tmp:
		res += e
	return res

def LStrToStr(L):
	""" list[str] -> str : Transforme une liste d'hexa en un mot Ox"""
	res = "0x"
	for e in L:
		res+=e
	return res

def LStrToBin(L):
	res=list()
	tmp=LStrToInt(L)
	for e in tmp:
		b=bin(e)
		if len(b[2:]) < 8:
			for i in range(8-len(b[2:])):
				res.append(0)
		for i in range(len(b[2:])):
			res.append(b[2+i])
	return res

#Adresse MAC :
macsrc = LStrToMac(L[6:12])
macdst = LStrToMac(L[0:6])
print(macsrc, "        ", macdst)

#Adresse ip :
ipsrc = LStrToIp(L[26:30])
ipdst = LStrToIp(L[30:34])
print(ipsrc, "        ", ipdst)

#Num port :
portsrc = LStrToPort(L[34:36])
portdst = LStrToPort(L[36:38])
print(portsrc, "        ", portdst)
