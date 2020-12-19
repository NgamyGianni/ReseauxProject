f = open("testLab.txt", "r")
L = list()

for line in f:
	L.extend(line.split("\t"))

#print([L[i] for i in range(len(L)) if i%17==0])
#rint(L)
LL = list()
for e in L:
	LL.append(e.split())


"""
print(int(LL[1][0], base=16))
print(LL[0][1:int(LL[1][0], base=16)+1])
"""

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

#for e in LL:
#	print(e)

# Retire les indices de LL
def LLtoLLclean(LL):
	tmp = []
	for i in range(len(LL)):
		for j in range(len(LL[i])):
			if len(LL[i][j]) > 2 and LL[i][j][:2] == "0x":
				tmp.append((i, j))
	for e in tmp:
		i, j = e
		del LL[i][j]
	return LL

print(LLtoLLclean(LtoLL(LL)))