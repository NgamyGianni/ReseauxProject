import sys

#file src = sys.argv[1]
#file dst = sys.argv[2]

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

Lres = LStrToInt(L)


print(Lres)

def LStrToIp(L):
	""" list[str] -> str : Transforme une liste d'hexa en adresse ip en str"""
	L = LstrToInt(L)
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

print(LStrToMac(L))