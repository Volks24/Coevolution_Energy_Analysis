import re
import statistics
import numpy as np
import operator;


########## Herramientas #########

######## Range con Float ######

def frange(start, stop, step):
	i = start
	while i < stop:
		yield i
		i += step
	return()



########## Generar Distancias #########

def distancias(input_distancias,input_fasta):
	dist_dic ={}
	dist_dic_aa = {}
	dist_file = open (input_distancias , "r")
	fasta_file = open (input_fasta , "r")
	posiciones = fasta_file.readlines()
	for linea in dist_file:
		datos_dis=linea.split(" ")
		dist_dic[str(datos_dis[0])+" "+str(datos_dis[1])] = datos_dis[2]
		dist_dic_aa[str(datos_dis[0])+" "+str(datos_dis[1])] = datos_dis[3]+"_"+datos_dis[4]
	print(dist_dic)
	return(dist_dic, dist_dic_aa)
	

########## Contar Gaps #########
def contar_gaps(pos_actual,msa_gaps):
	huecos = 0
	for i in range (1,pos_actual):
		if "-" in msa_gaps[i]:
			huecos = huecos + 1
	return(huecos)

######### Armado de MSA ########

def msa(input_fasta):
	fasta = open (input_fasta , "r")
	posiciones = fasta.readlines()
	msa = {}
	gaps = []
	posicion = 0
	for j in range(1,len(posiciones)):
		if ">" in posiciones[j]:
			break
		else:
			for k in range(0,len(posiciones[j])):
				if "\n" in posiciones[j][k]:
					next
				else:
					posicion = posicion + 1
					msa[posicion]=posiciones[j][k]
					if posiciones[j][k] == "-":
						gaps.append(posicion)

	return(msa,gaps)

######### Estadisticas - Z ########
 
def calcular_z(diccionarios,media,std):
	Z_dicc = {}
	for keys in diccionarios:
		Z = round(((float(diccionarios[keys]) - media) / std),4)
		Z_dicc[keys] = Z
	return(Z_dicc)
	
######### Armado Archivo Z ########

def archivo_z(Diccionario_Z,archivo,caso):
	salida = open(archivo+caso+"_Z.txt" , "w")
	Ordenados_Z = sorted(Diccionario_Z.items(), key=operator.itemgetter(0))
	salida.write("Total Daatos "+str(caso)+" "+str(len(Ordenados_Z))+"\n")
	for i in range (0,len(Ordenados_Z)):
		salida.write(str(Ordenados_Z[i][0])+"\t"+str(Ordenados_Z[i][1])+"\n")
	salida.close()
	return()
