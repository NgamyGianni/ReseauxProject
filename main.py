import fonctions, sys

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

# Construit une liste à partir d'un fichier text, ligne par ligne
for line in f:
	L.extend(line.split("\t"))

# Construit la structure générale du programme, une liste composée de listes, dont chaque représente une trame (sans commentaire)
LL = list()
for e in L:
	if fonctions.formatValideOffset(e[0:4]):
		LL.append(e.split())

# Retire les offset
LL = fonctions.LLtoLLclean(fonctions.LtoLL(LL))
res = ""

# Affiche les trames, et les entêtes qui correspondent
for i in range(len(LL)):
	res += "\nTrame "+str(i)+" :\n"
	if len(LL[i]) < 14:
		print("")
		exit()
	res += "\n"+fonctions.analyseETHERNET(LL[i])
	if len(LL[i]) > 14:
		res += fonctions.analyseIP(LL[i])[0]
	if len(LL[i]) > 34:
		res += fonctions.analyseTCP(LL[i])[0]
	if len(LL[i]) > 54 and LL[i][len(LL[i])-4:len(LL[i])] == ["0d", "0a", "0d", "0a"]:
		res += fonctions.analyseHTTP(LL[i])

# Ecrit le résultat dans le fichier destination
d.write(res+"\n")

# Ferme les fichiers
d.close()
f.close()
