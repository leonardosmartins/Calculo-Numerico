import copy

def readFile(fileName):
	file = open ( '../Inputs/secondInput.txt' , 'r')
	matrix = []
	matrix = [ line.split() for line in file]
	for i in range(len(matrix)):
		for j in range(len(matrix[i])):
			matrix[i][j] = [None,int(matrix[i][j])]

	return matrix

def createMatrix(lin, col):
	matrix = []
	for i in range(lin):
		matrix.append([0] * col)

	return matrix

def verifica(vetor):
	cont = 0
	for i in range(len(vetor)):
		if vetor[i] == None:
			cont = -1

	return cont			
def otimalidade(matrix, val):
	# valor = val % len(matrix)
	
	v = range(len(matrix[0])-1)
	u = range(len(matrix)-1)
	
	for i in range(len(v)):
		v[i] = None;

	for i in range(len(u)):
		u[i] = None	
	
	teste = 0

	val_original = val%(len(matrix)-1)
	tam = 8

	print "\n$$$$$$$$  VAL:",val

	while(1):

		if(None in u or None in v):
			i = val%(len(matrix))	
			for j in range(len(matrix[0])-1):
				if (matrix[i][j][0] != None):
					print "\ni: ", i
		 			print "\nj: ", j
		 			print "\nTAM: ", tam
		 			print "\nVAL: ", val
		 			print "\nVAL_ORIGINAL: ",val_original
					if(u[i] == None and i == val_original):
						u[i] = 0
						print "\nu[i]: ", u[i]
					elif(u[i] == None and i != val_original):			
						if(v[j]== None):
							continue
						u[i] = matrix[i][j][1] - v[j]
						print "\nu[i]: ", u[i] 
					
					if(v[j] == None):
						v[j] = matrix[i][j][1] - u[i]
						print "\nv[j]: ", v[j]	
			val = val + 1

		else:
			break
	
	return u,v				

def cantoNoroeste(matrix):
	z = 0
	cam = []
	colunas = range(len(matrix[0])-1)
	col_usadas = []


	for i in range(len(matrix)-1):
		count=0
		for j in colunas:
			
			count=count+1
			matrix[i][j][0] = min(   matrix[len(matrix)-1][j][1]   ,  matrix[i][len(matrix[i])-1][1]   )
			matrix[len(matrix)-1][j][1] = matrix[len(matrix)-1][j][1] - matrix[i][j][0]
			matrix[i][len(matrix[i])-1][1] = matrix[i][len(matrix[i])-1][1] - matrix[i][j][0]
			
			if(matrix[i][len(matrix[i])-1][1] == 0):
				break;
			else:
				col_usadas.append(j)
			
		for c in col_usadas:
				colunas.remove(c);
		col_usadas = [];


	for i in range (len(matrix)):
		for j in range (len(matrix[i])):
			if(matrix[i][j][0] != None):
				z = z + matrix[i][j][0] * matrix[i][j][1]
				cam.append([i,j])

	print (z)
	return cam

def caminho(matrix):
	
	matrixNova = matrix
	for i in range(len(matrix)):
		for j in range(len(matrix[i])):
			matrixNova[i][j] = [None,int(matrix[i][j][1])]


	return matrixNova		

def fill(matrix, u, v):
	teste = [0,0]
	valor = 0
	for i in range(len(matrix)-1):
		for j in range(len(matrix[0])-1):
			if(matrix[i][j][0] == None):
				matrix[i][j][0] = matrix[i][j][1] - u[i] - v[j]
				if (matrix[i][j][0] < valor):
					valor = matrix[i][j][0]
					teste = [i,j]

	print("FILL: ", matrix)
	print ("\n")				
	return teste, valor				


def get_na_linha(caminho,val):
	elem_da_linha = []
	for i in caminho:
		if(i[0]==val[0]):
			elem_da_linha.append([i,abs(i[1]-val[1])])
	elem_da_linha.sort(key=lambda x: x[1],reverse = True)
	return elem_da_linha

def get_na_coluna(caminho,val):
	elem_da_linha = []
	for i in caminho:
		if(i[1]==val[1]):
			elem_da_linha.append([i,abs(i[0]-val[0])])
	elem_da_linha.sort(key=lambda x: x[1],reverse = True)
	return elem_da_linha

def percurso2(resposta,caminho_copia,end_val,val,onde):
	if(onde == 1):
		firstcount = 0
		elem_da_linha = get_na_linha(caminho_copia,val)	
		if len(elem_da_linha)==0: # NAO HA ELEMENTO NENHUM NA LINHA
			return 0,0;
		
		for j in elem_da_linha:
			if(j[0][0]==end_val[0] and j[0][1]==end_val[1]):# PROXIMO ELEMENTO EH O MINIMO
				resposta.append(end_val)
				return 1,reposta
		
		#agora adiciona-se o elemento minimo ao caminho
		for i in caminho_copia:
			if(i == end_val):
				firstcount = 1
		if(firstcount==0):
			caminho_copia.append(end_val)

		for i in elem_da_linha:
			copia_aux = list(caminho_copia)
			copia_aux.remove(i[0])
			resposta.append(i[0])
			x, flag = percurso2(resposta,copia_aux,end_val,i[0],0)
			if(x!=0):
				if(flag!=0):
					
					return 1,resposta
				return 1,0
			elif(x==0):
				#print "x = 0: deletando ultimo da resposta.."
				resposta.remove(resposta[len(resposta)-1])
		

	#print "\nPROCURANDO AGORA NA COLUNA\n"
	elem_da_col = get_na_coluna(caminho_copia,val)
	if len(elem_da_col)==0: # NAO HA ELEMENTO NENHUM NA COLUNA
		return 0,0;
	
	for j in elem_da_col:
		if(j[0][0]==end_val[0] and j[0][1]==end_val[1]):# PROXIMO ELEMENTO EH O MINIMO
			resposta.append(end_val)
			return 1,resposta

	for i in elem_da_col:
		copia_aux = list(caminho_copia)
		copia_aux.remove(i[0])
		resposta.append(i[0])
		x, flag = percurso2(resposta,copia_aux,end_val,i[0],1)
		if(x!=0):
			
			if(flag!=0):
				return 1,resposta
			return 1,0
		elif(x==0):
			resposta.remove(resposta[len(resposta)-1])

	return 0,0

def pegaPrincipais(m):
	principais = []
	for i in range(len(m)):
		for j in range(len(m[i])):
			if m[i][j][0] != None:
				principais.append([i,j])
	
	return principais
				
def ajustaCaminho(m, perc, mOriginal,p):
	matrixNova = createMatrix(len(m), len(m[0]))
	for i in range(len(m)):
		for j in range(len(m[i])):
			if i == (len(m) - 1) or j == (len(m[0]) - 1):
				matrixNova[i][j] = [None,mOriginal[i][j][1]]	
			else:
				matrixNova[i][j] = [None,m[i][j][1]]

	for i in range(len(m)):
		for j in range(len(m[i])):
			for k in range(len(p)):
				if(i == p[k][0] and j == p[k][1]):
					matrixNova[i][j][0] = m[i][j][0]			
	
	valor = 0
	valorReal = []
	for i in range(len(perc)):
		if i%2 != 0 and i != len(perc)-1:
			valorReal.append(m[perc[i][0]][perc[i][1]][0])
				
	menorValor = min(valorReal)
	
	for i in range(len(perc)):
		if i%2 == 0 and i != 0 and i != len(perc)-1:
			matrixNova[perc[i][0]][perc[i][1]][0] = m[perc[i][0]][perc[i][1]][0] + menorValor
		elif i%2 != 0 and i != len(perc)-1:
			matrixNova[perc[i][0]][perc[i][1]][0] = m[perc[i][0]][perc[i][1]][0] - menorValor
		else:
			matrixNova[perc[i][0]][perc[i][1]][0] = menorValor		 

	for i in range(len(m)):
		for j in range(len(m[i])):
			if matrixNova[i][j][0] == 0:
				matrixNova[i][j][0] = None

	return matrixNova

def exibeResultado(p,matrix):	
	teste = copy.deepcopy(matrix)
	matrixNova = matrix
	for i in range(len(matrix)):
		for j in range(len(matrix[i])):
			matrixNova[i][j] = [None,int(matrix[i][j][1])]
	
	for i in range(len(p)):
		matrixNova[p[i][0]][p[i][1]][0] = teste[p[i][0]][p[i][1]][0]


	return matrixNova




m = readFile("input.txt")
mOriginal = readFile("input.txt")
cam = cantoNoroeste(m)
start_valor = 0

while(1):
	
	print("MATRIZ:    ")
	print(m) 
	p = pegaPrincipais(m)
	u,v = otimalidade(m,start_valor)
	print "\nU: ",u
	print "\nV: ",v
	
	end_val,valor = fill(m,u,v)
	print(valor)
	if (valor == 0):
		print("Solucao Otima")
		print(exibeResultado(p,m))
		break	
	
	caminho_copia = list(p)
	print "\nPega principais: ", p
	print "\nCaminho copia: ", caminho_copia 
	resposta = []
	resposta.append(end_val)
	val = copy.deepcopy(end_val)
	i,perc = percurso2(resposta,caminho_copia,end_val,val,1)

	print "\nPerc: ", perc
	m = ajustaCaminho(m, perc, mOriginal, p)
	print "\n"
	print(m)
	start_valor = start_valor + 1
	print("\n\n------------------FIMMM-------------------------")
