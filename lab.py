f = open("testLab.txt", "r")
L = list()

for line in f:
	L.extend(line.split("\t"))

def erreur(pos):
	i = len(pos)-1
	while i>=0:
		if formatValideOffset(pos[i]):
			print("erreur ", pos[i])
			exit()
		i-=1

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
#print(L)
#print(LL)
# Créer la structure générale des trames : créer une liste composée de listes et chaque liste est une trame
def LtoLL(L):
	LL = []
	tmp = []
	for i in range(len(L)):
		if L[i][0] == "0x00":
			LL.append(tmp)
			tmp = []
		
		if i < len(L)-1 and L[i+1][0] != "0x00":
			for x in range(int(L[i+1][0], base=16)-int(L[i][0], base=16)+1):
				if formatValideByte(L[i][x]) or formatValideOffset(L[i][x]):
					tmp.append(L[i][x])
			if len(tmp) != int(L[i+1][0], base=16)-int(L[i][0], base=16)+1:
				erreur(tmp)
		else:
			for x in range(len(L[i])):
				if formatValideByte(L[i][x]) or formatValideOffset(L[i][x]):
					tmp.append(L[i][x])

		if i == len(L)-1:
			LL.append(tmp)
	del LL[0]
	return LL

print(LtoLL(LL))

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

#print(LLtoLLclean(LtoLL(LL)))
#print(len(LLtoLLclean(LtoLL(LL))))

def analyseEthernet(L):
	macDst=LStrToMac(L[0:6])
	macSrc=LStrToMac(L[6:12])
	if L[12:14] == ["08","00"]:
		etherType="IPv4"
	"""elif L[12:14] == ["86","DD"]:
		etherType="IPv6"""
	"""elif L[12:14] == ["08","06"]:
		etherType="ARP"""
	"""elif L[12:14] == ["80","35"]:
		etherType="RARP"
	elif L[12:14] == ["80","9B"]:
		etherType="AppleTalk"""
	"""else:
		print("Erreur : Champ Ethernet Type non reconnu")
		quit()
	print("Champ Ethernet Adresse Mac Destination : ",macDst)
	print("Champ Ethernet Adresse Mac Source : ",macSrc)
	print("Champ Ethernet Type : 0x",L[12],L[13],etherType)
	return etherType"""
