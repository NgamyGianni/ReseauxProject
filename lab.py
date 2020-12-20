f = open("testLab.txt", "r")
L = list()

for line in f:
	L.extend(line.split("\t"))

# valide le format des offset de la trame
def formatValideOffset(x):
	return x[:2] == "0x" and formatValideByte(x[2:])

# Valide le format des octets de la trame
def formatValideByte(x):
	# str -> bool
	if len(x) != 2:
		return False

	for e in x:
		if not("a" <= e.lower() <= "f" or "0" <= e <= "9"):
			return False

	return True


# Construit une liste composée de lignes du fichier si l'offset est valide
LL = list()
for e in L:
	if formatValideOffset(e[0:4]):
		LL.append(e.split())

# Créer la structure générale des trames : créer une liste composée de listes et chaque liste est une trame
def LtoLL(L):
	LL = []
	tmp = []
	for i in range(len(L)):
		if L[i][0] == "0x00" or i == len(L)-1:
			LL.append(tmp)
			tmp = []

		if i < len(L)-1:
			tmp.extend(L[i][:int(L[i+1][0], base=16)-int(L[i][0], base=16)+1])
		else:
			tmp.extend(L[i])

	del LL[0]
	return LL

#print(LtoLL(LL))

# Retire les offset de LL : ne garde que les formats valides des octets de la trame
def LLtoLLclean(LL):
	res = [[]]
	tmp = []
	for i in range(len(LL)):
		for j in range(len(LL[i])):
			if formatValideByte(LL[i][j]):
				tmp.append(LL[i][j])
		res.append(tmp)
		tmp = []
	
	del res[0]
	return res

print(LLtoLLclean(LtoLL(LL)))
print(len(LLtoLLclean(LtoLL(LL))))