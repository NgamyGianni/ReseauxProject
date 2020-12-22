import projet

f = open("wiretest.txt", "r")
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
	return len(x) == 4 and formatValideByte(x[:2]) and formatValideByte(x[2:])

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
	j = 0
	for i in range(len(L)):
		if L[i][0] == "0000":
			LL.append(tmp)
			tmp = []
			j = 0

		if i < len(L)-1 and L[i+1][0] != "0000":
			j+=1

		if i < len(L)-1 and L[i+1][0] != "0x00":
			for x in range(int(L[i+1][0], base=16)-int(L[i][0], base=16)+1):
				if formatValideByte(L[i][x]) or formatValideOffset(L[i][x]):
					tmp.append(L[i][x])
			if len(tmp) != int(L[i+1][0], base=16)+j:
				print(len(tmp))
				erreur(tmp)
		else:
			j+=1
			for x in range(len(L[i])):
				if formatValideByte(L[i][x]) or formatValideOffset(L[i][x]):
					tmp.append(L[i][x])

		if i == len(L)-1:
			LL.append(tmp)
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

LL = LLtoLLclean(LtoLL(LL))
#print(len(LLtoLLclean(LtoLL(LL))))

def analyseEthernet(L):
	res = "Ethernet :\n"
	macDst=projet.LStrToMac(L[0:6])
	macSrc=projet.LStrToMac(L[6:12])
	if L[12:14] == ["08","00"]:
		etherType="IPv4"
	"""elif L[12:14] == ["08","06"]:
		etherType="ARP"
	else:
		print("Erreur : Champ Ethernet Type non reconnu")
		quit()
	elif L[12:14] == ["86","DD"]:
		etherType="IPv6
	elif L[12:14] == ["80","35"]:
		etherType="RARP
	elif L[12:14] == ["80","9B"]:
		etherType="AppleTalk"""

	res += "	Adresse Mac Destination : "+macDst+"\n"
	res += "	Adresse Mac Source : "+macSrc+"\n"
	res += "	Type : "+projet.LStrToStr(L[12:14])+" "+etherType+"\n"
	return res

print(analyseEthernet(LL[0]))

def analyseIp(L):
	res = "Ip : \n"
	res += "	Version : 0x"+str(L[14][0])+" ("+str(L[14][0])+")"+"\n"
	res += "	Header length : 0x"+str(L[14][1])+" ("+str(L[14][1]*4)+")"+"\n"
	res += "	Type of service : "+projet.LStrToStr(L[15])+"\n"
	res += "	Total Length : "+projet.LStrToStr(L[16:18])+" ("+projet.LStrToPort(L[16:18])+")"+"\n"
	res += "	Identifier : "+projet.LStrToStr(L[18:20])+"\n"
	res += "    Flags : "+projet.LStrToStr(L[20:22])+"\n"
	res += "    	Reserve :"
	return res

print(analyseIp(LL[0]))
