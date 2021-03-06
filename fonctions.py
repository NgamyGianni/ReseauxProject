import convertions

# Indique qu'il y a une erreur et sa position
def erreur(pos):
	i = len(pos)-1
	while i>=0:
		if formatValideOffset(pos[i]):
			print("erreur ", pos[i])
			exit()
		i-=1

# Valide le format des offset de la trame
def formatValideOffset(x):
	return len(x) == 4 and formatValideByte(x[:2]) and formatValideByte(x[2:])

# Valide le format des octets de la trame
def formatValideByte(x):
	if len(x) != 2:
		return False

	for e in x:
		if not("a" <= e.lower() <= "f" or "0" <= e <= "9"):
			return False

	return True

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
			for x in range(int(L[i+1][0], base=16)-int(L[i][0], base=16)+1):
				if formatValideByte(L[i][x]) or formatValideOffset(L[i][x]):
					tmp.append(L[i][x])
			if len(tmp) != int(L[i+1][0], base=16)+j:
				print(len(tmp), int(L[i+1][0], base=16)+j)
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

# Renvoie un str représentant l'entête ETHERNET
def analyseETHERNET(L):
	res = "\tETHERNET :\n"
	macDst=convertions.LStrToMac(L[0:6])
	macSrc=convertions.LStrToMac(L[6:12])
	if L[12:14] == ["08","00"]:
		etherType="IPv4"

	res += "		Adresse Mac Destination : "+macDst+"\n"
	res += "		Adresse Mac Source : "+macSrc+"\n"
	res += "		Type : "+convertions.LStrToStr(L[12:14])+" "+etherType+"\n"
	return res

# Renvoie un str représentant l'entête IP
def analyseIP(L):
	res = "\tIP : \n"
	res += "		Version : 0x"+str(L[14][0])+" ("+str(L[14][0])+")"+"\n"
	res += "		Header length : 0x"+str(L[14][1])+" ("+str(int(L[14][1])*4)+")"+"\n"
	res += "		Type of service : "+convertions.LStrToStr(L[15])+"\n"
	res += "		Total Length : "+convertions.LStrToStr(L[16:18])+" ("+convertions.LStrToPort(L[16:18])+")"+"\n"
	res += "		Identifier : "+convertions.LStrToStr(L[18:20])+"\n"
	res += "		Flags : "+convertions.LStrToStr(L[20:22])+"\n"
	Lb = convertions.LStrToBin(L[20:22])
	res += "			Reserve : "+Lb[0]+"\n"
	res += "			DF : "+Lb[1]+"\n"
	res += "			MF : "+Lb[2]+"\n"
	res += "			Fragment offset : "
	for i in range(3,len(Lb)):
		res+= Lb[i]
	res += "\n"
	res += "		Time To Live : "+convertions.LStrToStr(L[22])+"("+convertions.LStrToPort([L[22]])+")"+"\n"
	res += "		Protocol : "+convertions.LStrToStr(L[23])+"("+convertions.LStrToPort([L[23]])+")"+"\n"
	res += "		Header checksum : "+convertions.LStrToStr(L[24:26])+"\n"
	res += "		Adresse IP Source : "+convertions.LStrToStr(L[26:30])+"("+convertions.LStrToIp(L[26:30])+")"+"\n"
	res += "		Adresse IP Destination : "+convertions.LStrToStr(L[30:34])+"("+convertions.LStrToIp(L[30:34])+")"+"\n"
	
	return res,int(L[14][1])*4+14

# Renvoie un str représentant l'entête TCP
def analyseTCP(L):
	a,i=analyseIP(L)
	res = "\tTCP : \n"
	res += "		Source port number : "+convertions.LStrToStr(L[i:i+2])+"("+convertions.LStrToPort(L[i:i+2])+")"+"\n"
	res += "		Destination port number : "+convertions.LStrToStr(L[i+2:i+4])+"("+convertions.LStrToPort(L[i+2:i+4])+")"+"\n"
	res += "		Sequence Number : "+convertions.LStrToStr(L[i+4:i+8])+"("+convertions.LStrToPort(L[i+4:i+8])+")"+"\n"
	res += "		Acknowledgment number : "+convertions.LStrToStr(L[i+8:i+12])+" ("+convertions.LStrToPort(L[i+8:i+12])+")"+"\n"
	Lb = convertions.LStrToBin(L[i+12:i+14])
	res += "		Transport Header Length: "+Lb[0]+Lb[1]+Lb[2]+Lb[3]+"("+str(int("0b"+Lb[0]+Lb[1]+Lb[2]+Lb[3], base=2)*4)+")"+"\n"
	res += "		Flags : 0x"+L[i+12][1]+L[i+13]+"\n"
	res += "			Reserved : "
	for j in range(4,10):
		res+= Lb[j]
	res += "\n"
	res += "			URG : "+Lb[10]+"\n"
	res += "			ACK : "+Lb[11]+"\n"
	res += "			PSH : "+Lb[12]+"\n"
	res += "			RST : "+Lb[13]+"\n"
	res += "			SYN : "+Lb[14]+"\n"
	res += "			FIN : "+Lb[15]+"\n"
	res += "		Window : "+convertions.LStrToStr(L[i+14:i+16])+"("+convertions.LStrToPort(L[i+14:i+16])+")"+"\n"
	res += "		Checksum : "+convertions.LStrToStr(L[i+16:i+18])+"("+convertions.LStrToPort(L[i+16:i+18])+")"+"\n"
	res += "		Urgent Pointer : "+convertions.LStrToStr(L[i+18:i+20])+"("+convertions.LStrToPort(L[i+18:i+20])+")"+"\n"
	return res,int("0b"+Lb[0]+Lb[1]+Lb[2]+Lb[3], base=2)*4+i

# Renvoie un str représentant l'entête HTTP
def analyseHTTP(L):
	a,i=analyseTCP(L)
	tmp=list()
	res = "\tHTTP : \n"
	tmp.append("09")
	tmp.append("09")
	while not(L[i] == "0d" and L[i+1] == "0a" and L[i+2] == "0d" and L[i+3] == "0a"):
		if L[i] == "0a":
			tmp.append(L[i])
			tmp.append("09")
			tmp.append("09")
		else:
			tmp.append(L[i])
		i+=1

	bytes_object=bytes.fromhex(convertions.LStrToStr(tmp)[2:])

	res+=bytes_object.decode("ASCII")
	return res

