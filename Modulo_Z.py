########### Instruciones 
########### Colocar archivos *.MIp.txt de energia y mip en carpetras corres pondientes 
########### Ejectutar generar_mip_reduce A o M o o (P y alpha) (alpha entre 0 y 1)  
########### Seleciona el tipo de combinacion Aditiva ,  Multiplicativa  o Parametrica (A/M/P)

import os;
import os.path;
import sys;
import math;

def Z_Mip(familia,ruta_Mip):
	#Var     
	Mip_pares_z = {}
	#Parte 1 busco en las lista de Mip
	file_Mip = open (ruta_Mip+familia, "r")
	for line in file_Mip:
				if "c	d	" in line:
					continue
				else:
					valores = line.split("\t")
					par = (valores[0]+" "+valores[1]) # pos 1 y 2
					Z = float(valores[12]) #Valor Z para clasificar
					Mip_pares_z[par] = Z
	file_Mip.close()
	return(Mip_pares_z)






def new_Z_comb(familia,Mip_pares_z,ruta_Ene,resultados_ruta_aditiva,resultados_ruta_multi,resultados_ruta_para,alpha): 
	salidaresultados_aditivo = resultados_ruta_aditiva+familia[:-7]+"reduced.txt"
	salidaresultados_parametrica = resultados_ruta_para+familia[:-7]+"reduced.txt"
	salidaresultados_multiplicativa = resultados_ruta_multi+familia[:-7]+"reduced.txt"
	file_energy = open (ruta_Ene+familia, "r")
	file_ad = open(salidaresultados_aditivo, "w")
	file_mu = open(salidaresultados_multiplicativa, "w")
	file_pa = open(salidaresultados_parametrica, "w")

	#header = "c[0]	d[1]	Hc[2]	Hd[3]	Hcd[4]	MIcd[5]	aa_c[6]	aa_d{7}	energy[8]	MIe[9]	mean_MI[10]	stdev[11]	Zcomb[12]	Zmi[13]\n"
	#header = "c[0]	d[1]	Hc[2]	Hd[3]	Hcd[4]	MIcd[5]	aa_c[6]	aa_d[7]	energy[8]	MIe[9]	mean_MI[10]	stdev[11]	Z[12]	Zmi[13]\n"

	print ("Generado Reduce de "+familia[:-8])
	for line in file_energy:
			if "c	d	" in line:
				continue
			else:
				valores = line.split("\t")
				par = (valores[0]+" "+valores[1]) # pos 1 y 2 
				if par in Mip_pares_z: # Grupo1
						z_aditivo = str("%.5f" %((float(Mip_pares_z[par])+float(valores[12]))/2))
						z_multi = str("%.5f" %((float(Mip_pares_z[par]))*(float(valores[12]))))
						z_para = str("%.5f" %((alpha*(float(Mip_pares_z[par]))) + ((1-alpha) * (float(valores[12])))))
						file_ad.write(str(valores[0])+"\t"+str(valores[1])+"\t"+str(valores[8])+"\t"+str(z_aditivo)+"\t"+str(valores[6])+"\t"+str(valores[7])+"\t"+str(valores[5])+"\n")
						file_mu.write(str(valores[0])+"\t"+str(valores[1])+"\t"+str(valores[8])+"\t"+str(z_multi)+"\t"+str(valores[6])+"\t"+str(valores[7])+"\t"+str(valores[5])+"\n")
						file_pa.write(str(valores[0])+"\t"+str(valores[1])+"\t"+str(valores[8])+"\t"+str(z_para)+"\t"+str(valores[6])+"\t"+str(valores[7])+"\t"+str(valores[5])+"\n")
				else:
					continue
	return

##### Formato del reduce de salida = Pos1   Pos2   MIp/Ene.    Zeta      aa1  aa2   MIcd
