import lab
import projet
import sys

if len(sys.argv) != 3: # Si il y a bien 2 arguments, correspondant aux fichiers source et destination
	print("Erreur : Usage : <nom du fichier source> <nom du fichier destination>")
	exit()

# Vérifie l'existence du fichier source
try:
	f = open(sys.argv[1], "r")
except:
    print("Erreur: Le fichier source n'existe pas.")
    exit()

d = open(sys.argv[2], "w")
L = list()

for line in f:
	L.extend(line.split("\t"))

LL = list()
for e in L:
	if lab.formatValideOffset(e[0:4]):
		LL.append(e.split())

LL = lab.LLtoLLclean(lab.LtoLL(LL))
res = ""

for i in range(len(LL)):
	res += "\nTrame "+str(i)+" :\n"
	if len(LL[i]) < 14:
		print("")
		exit()
	res += "\n"+lab.analyseETHERNET(LL[i])
	if len(LL[i]) > 14:
		res += ""+lab.analyseIP(LL[i])[0]
	if len(LL[i]) > 34:
		res += ""+lab.analyseTCP(LL[i])[0]
	if len(LL[i]) > 54:
		res += ""+lab.analyseHTTP(LL[i])

d.write(res+"\n")

d.close()
f.close()
