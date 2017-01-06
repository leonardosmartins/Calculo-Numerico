import copy
import time

# Alunos: Leonardo da Silva Martins - 11321BCC032
#		  Diego de Pontes Pasquini	

def fillZero(matrix):
	for i in range(len(matrix)):
		for j in range(len(matrix[i])):
			matrix[i][j] = [None,0]

	return matrix

def start():

	qtdOrigens = int(raw_input('Quandtidade origens: '))
	qtdDestinos = int(raw_input('Quandtidade destinos: '))
	qtdTransbordos = int(raw_input('Quandtidade transbordos: '))

	origens = []
	destinos = []
	ofertas = []
	demandas  = []
	transbordos = []
	capTransbordos = []
	demTransbordos = []

	for i in range(qtdOrigens):
		nome = raw_input("Nome da origem numero %d: " %i)
		valor = int(raw_input("Oferta da origem numero %d: " %i))
		origens.append(nome)
		ofertas.append(valor)

	for i in range(qtdDestinos):
		nome = raw_input("Nome do destino numero %d: " %i)
		valor = int(raw_input("Demanda da origem numero %d: " %i))
		destinos.append(nome)
		demandas.append(valor)	

	for i in range(qtdTransbordos):
		nome = raw_input("Nome do transbordo numero %d: " %i)
		transbordos.append(nome)
		valor = int(raw_input("Informe a capacidade do transbordo numero %d, caso ele tambem seja uma origem (ou 0 caso contrario): " %i))
		capTransbordos.append(valor)
		valor2 = int(raw_input("Informe a demanda do transbordo numero %d, caso ele tambem seja uma demanda (ou 0 caso contrario): " %i))
		demTransbordos.append(valor2)

	if sum(ofertas) > sum(demandas):
		destinos.append("Artificial")
		demandas.append(sum(ofertas)-sum(demandas))
		qtdDestinos = qtdDestinos + 1


	elif sum(ofertas) < sum(demandas):
		origens.append("Artificial")
		ofertas.append(sum(demandas) - sum(ofertas))
		qtdOrigens = qtdOrigens + 1


	matrix = createMatrix((qtdOrigens+qtdTransbordos+1),(qtdDestinos+qtdTransbordos+1))
	matrix = fillZero(matrix)		

	for i in range(len(matrix)-1):
		for j in range(len(matrix[0])-1):
			if i < qtdOrigens and j < qtdTransbordos: 
				valor = int(raw_input("Custo de %s para %s: " %(origens[i],transbordos[j])))
				matrix[i][j][1] = valor
			elif i < qtdOrigens and j >= qtdTransbordos:	
				valor = int(raw_input("Custo de %s para %s: " %(origens[i],destinos[j-qtdTransbordos])))
				matrix[i][j][1] = valor
			elif i >= qtdOrigens and j < qtdTransbordos: 
				valor = int(raw_input("Custo de %s para %s: " %(transbordos[i-qtdOrigens],transbordos[j])))
				matrix[i][j][1] = valor
			elif i >= qtdOrigens and j >= qtdTransbordos:	
				valor = int(raw_input("Custo de %s para %s: " %(transbordos[i-qtdOrigens],destinos[j-qtdTransbordos])))
				matrix[i][j][1] = valor	

	for i in range(qtdOrigens):
		matrix[i][len(matrix[0])-1][1] = ofertas[i]

	for i in range(qtdOrigens,len(matrix)-1):
		matrix[i][len(matrix[0])-1][1] = sum(ofertas)+capTransbordos[i-qtdOrigens]

	for i in range(qtdTransbordos):
		matrix[len(matrix)-1][i][1] = sum(demandas)+demTransbordos[i]

	for i in range(qtdTransbordos,len(matrix[0])-1):
		matrix[len(matrix)-1][i][1] = demandas[i - qtdTransbordos]

	return matrix,origens,destinos,transbordos,qtdOrigens,qtdDestinos,qtdTransbordos	

def createMatrix(lin, col):
	matrix = []
	for i in range(lin):
		matrix.append([0] * col)

	return matrix
			
def otimalidade(matrix, val):
	v = range(len(matrix[0])-1)
	u = range(len(matrix)-1)
	
	for i in range(len(v)):
		v[i] = None;

	for i in range(len(u)):
		u[i] = None	
	
	val_original = val%(len(matrix)-1)
	
	while(1):

		if(None in u or None in v):
			i = val%(len(matrix))	
			for j in range(len(matrix[0])-1):
				if (matrix[i][j][0] != None):
					if(u[i] == None and i == val_original):
						u[i] = 0
					elif(u[i] == None and i != val_original):		
						if(v[j]== None):
							continue
						u[i] = matrix[i][j][1] - v[j] 
					
					if(v[j] == None):
						v[j] = matrix[i][j][1] - u[i]	
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

	print "\nZ = ",z
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
				resposta.remove(resposta[len(resposta)-1])
		

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
	posValorReal = []
	
	for i in range(len(perc)):
		if i%2 != 0 and i != len(perc)-1:
			valorReal.append(m[perc[i][0]][perc[i][1]][0])
			posValorReal.append(perc[i])
				
	menorValor = min(valorReal)
	
	for i in range(len(valorReal)):
		if(valorReal[i] == menorValor):
			posCerto = posValorReal[i]
	
	for i in range(len(perc)):
		if i%2 == 0 and i != 0 and i != len(perc)-1:
			matrixNova[perc[i][0]][perc[i][1]][0] = m[perc[i][0]][perc[i][1]][0] + menorValor
		elif i%2 != 0 and i != len(perc)-1:
			matrixNova[perc[i][0]][perc[i][1]][0] = m[perc[i][0]][perc[i][1]][0] - menorValor
		else:
			matrixNova[perc[i][0]][perc[i][1]][0] = menorValor		 

	matrixNova[posCerto[0]][posCerto[1]][0] = None
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

def exibeSolucaoOtima(matrix,origens,destinos,transbordos,qtdOrigens,qtdDestinos,qtdTransbordos):

	for i in range(len(matrix)-1):
		for j in range(len(matrix[0])-1):
			if(m[i][j][0] != None):
				if i < qtdOrigens and j < qtdTransbordos: 
					print "Envia %d unidades de %s para %s" %(m[i][j][0],origens[i],transbordos[j])
				elif i < qtdOrigens and j >= qtdTransbordos:
					print "Envia %d unidades de %s para %s" %(m[i][j][0],origens[i],destinos[j-qtdTransbordos])
				elif i >= qtdOrigens and j < qtdTransbordos:
					print "Envia %d unidades de %s para %s" %(m[i][j][0],transbordos[i-qtdOrigens],transbordos[j])
				elif i >= qtdOrigens and j >= qtdTransbordos:
					print "Envia %d unidades de %s para %s" %(m[i][j][0],transbordos[i-qtdOrigens],destinos[j-qtdTransbordos])	


#comeca o programa pegando as informacoes do usuario
m,origens,destinos,transbordos,qtdOrigens,qtdDestinos,qtdTransbordos, = start()
#faz uma copia da matriz original
mOriginal = copy.deepcopy(m)
#aplica o canto noroeste
cam = cantoNoroeste(m)
start_valor = 0

while(1):
	
	#cria um vetor p com as posicoes das variaves basicas
	p = pegaPrincipais(m)
	#aplica a otimalidade, calculando os vetores U e V
	u,v = otimalidade(m,start_valor)
	#preenche a matriz com as variaveis nao basicas a partir dos vetores U e V
	end_val,valor = fill(m,u,v)
	#verifica se chegou na solucao otima
	if (valor == 0):
		print("\nSolucao Otima\n")
		mNova = exibeResultado(p,m)
		print(mNova)
		print "\n"
		exibeSolucaoOtima(mNova,origens,destinos,transbordos,qtdOrigens,qtdDestinos,qtdTransbordos)
		break	
	
	caminho_copia = list(p)
	resposta = []
	resposta.append(end_val)
	val = copy.deepcopy(end_val)
	#cria um vetor com as posicoes do caminho de ajuste encontrado
	i,perc = percurso2(resposta,caminho_copia,end_val,val,1)
	#ajusta os valores do caminho de ajuste, somando e subtraindo o valor encontrado
	m = ajustaCaminho(m, perc, mOriginal, p)
	start_valor = start_valor + 1
	