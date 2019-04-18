# encoding: utf-8
######## Modulos ######## 
import yaml
import Modulo_All
import Modulo_Mistic
import Herramientas
import Modulo_Combinado
import Modulo_DCA
import os;
import os.path;
import operator;
import sys;
import Modulo_Z;
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from sklearn import metrics


######## Yaml ######## 
document = open('parametros.yml', 'r')
parsed = yaml.load(document)

######## Rutas y Otros ######## 
ruta = os.path.abspath (os.path.curdir)
graficos_ruta =ruta+parsed["directorios"]["plots_dir"]
resultados_ruta =ruta+parsed["directorios"]["output_dir"]
resultados_ruta_aditiva = ruta+parsed["directorios"]["output_aditiva"]
resultados_ruta_multi = ruta+parsed["directorios"]["output_mult"]
resultados_ruta_para = ruta+parsed["directorios"]["output_parame"]
input_distancias = ruta+parsed["directorios"]["input_dis"] ## Archivo de distancias *.dat
dirs_dist = os.listdir( input_distancias )
temporal =ruta+parsed["directorios"]["temporary_dir"]
dirs_temporal = os.listdir( temporal )
dirs = os.listdir( graficos_ruta )
carpetas = ["Aditiva","Multiplicativa","Energia","MIp","Parametrica_25","Parametrica_75","DCA","Mistic"]
dirs_dcat = os.listdir(carpetas[6])

####### Vaciar Carpetas Resultados y Temporales ######## 

for files in dirs_temporal:
	os.remove(temporal+files)

dirs = os.listdir(graficos_ruta)
for files in dirs:
	os.remove(graficos_ruta+files)

dirs = os.listdir(resultados_ruta)
for files in dirs:
	if "Graficos" or "Z" in files:
		next
	else:
		os.remove(resultados_ruta+files)

dirs = os.listdir(resultados_ruta_aditiva)
for files in dirs:
	os.remove(resultados_ruta_aditiva+files)

dirs = os.listdir(resultados_ruta_multi)
for files in dirs:
	os.remove(resultados_ruta_multi+files)

dirs = os.listdir(resultados_ruta_para)
for files in dirs:
	os.remove(resultados_ruta_para+files)


####### Valores #######
##  analisis : C / A / Z
##  C = Analisis Comparativo ; A = Analisis All; Z = Generar Reduce Combinado
##  valor_z_bajo: 2
##  valor_z_alto: 3
##  Z_corte_DCA  Valor de corte para DCA
##  Z_corte_Mis Valor de corte para Mistic
##  Z_corte_Comb Valor de corte para metodo combinado selecinado
##  corte_tp_a Valor para grafico contar FP hasta X Valor TP
##  corte_tp_b Valor para grafico contar FP hasta X Valor TP
##  metodo_comb : Aditiva / Multiplicativa / Parametrica_25 / Parametrica_75

z_b=parsed["parametros"]["valor_z_bajo"] # Valores de Z bajo para cada 100
z_a=parsed["parametros"]["valor_z_alto"] # Valores de Z alto para cada 100


####### Caso Globales ####### Calculos Tratamientos MIP / Energia/ Aditiva / Multiplicativa / Parametrica 25 todas las familias

if parsed["parametros"]["analisis"] == "Z":
	ruta_Mip = ruta+parsed["directorios"]["reduc_mip"]
	ruta_Ene = ruta+parsed["directorios"]["reduc_ener"]
	ruta_Z_ad = ruta+parsed["directorios"]["output_aditiva"]
	ruta_Z_pa = ruta+parsed["directorios"]["output_parame"]
	ruta_Z_mu = ruta+parsed["directorios"]["output_mult"]
	alpha = parsed["parametros"]["z_alpha"]
	
	dirs = os.listdir (ruta_Mip)
	dirs2 = os.listdir (ruta_Ene)
	
	for file in dirs: 
		familia = str(file)
		if familia in dirs2: 
			Mip_pares_z = Modulo_Z.Z_Mip(familia,ruta_Mip)
			Modulo_Z.new_Z_comb(familia,Mip_pares_z,ruta_Ene,ruta_Z_ad,ruta_Z_mu,ruta_Z_pa,alpha)
		else:
			print ("No esta el archivo "+familia+" en carpeta Energy")
		



####### Calculo de Distribuciones ####### Entrada : "all_in_contact_grouped_80.dat" y "all_not_in_contact_grouped_80.dat"

if parsed["parametros"]["analisis"] == "A":   
	dirs = os.listdir(ruta)
	for i in range (0,5):
		ruta_datos = ruta+'//'+carpetas[i]+'/'
		contacto = open(ruta_datos+"all_in_contact_grouped_80.dat","r")
		no_contacto = open(ruta_datos+"all_not_in_contact_grouped_80.dat","r")
		Modulo_All.grafico_distribuciones(carpetas[i],contacto,no_contacto,graficos_ruta)
		contacto.close()
		no_contacto.close()
	
####### Armado de Diccionarios por Caso Para Calculos ####### Entrada : "all_FP.dat" y "all_TP.dat"
	
	diccionarios = {}
	for i in range (0,5): # 6 para incluir la siguiente parametrica
		ruta_datos = ruta+'//'+carpetas[i]+'/'
		dirs = os.listdir(ruta_datos)
		FP = open(ruta_datos+"all_FP.dat","r")
		TP = open(ruta_datos+"all_TP.dat","r")
		diccionarios[carpetas[i]] = Modulo_All.armado_diccionarios(carpetas[i],FP,TP)
		
######### Curva Roc ##########

	roc_all_TP = {}
	roc_all_FP = {}
	roc_all = []
	datos_auc = open(resultados_ruta+"AUC.txt" , "w")

	for keys in diccionarios:
	
		roc_all_TP[keys] = []
		roc_all_FP[keys] = []
		roc_all.append(keys)
		roc_all_TP,roc_all_FP = Modulo_All.grafico_roc(diccionarios[keys],keys,roc_all_TP,roc_all_FP,datos_auc,graficos_ruta) 

	Modulo_All.grafico_roc_all(roc_all,roc_all_FP,roc_all_TP,datos_auc,graficos_ruta)
	datos_auc.close()
	
	######### Cada 100 ##########

	cada_100_z_a = {}
	cada_100_z_b = {}

	for keys in diccionarios:
		cada_100_b=Modulo_All.clasificacador(diccionarios[keys],keys,cada_100_z_b,z_b,temporal,graficos_ruta)

	for keys in diccionarios:
		cada_100_a=Modulo_All.clasificacador(diccionarios[keys],keys,cada_100_z_a,z_a,temporal,graficos_ruta)
	
	############# Ploteo

	Modulo_All.graficos_cada_100(cada_100_z_b,cada_100_z_a,z_b,z_a,temporal,graficos_ruta)

	######### Cada 5 ##########

	Modulo_All.graficos_cada_5(z_a,temporal,graficos_ruta)	

####### Caso Indivuduales ####### Calculos Tratamientos (Mistic / DCA) Entrada: Archivo MI_data

temp = open(temporal+"temp.txt", "w")

if parsed["parametros"]["analisis"] == "C":  
	
	ALL_VENN = {} # Generar Keys para Venn
	
	###### Generar Archivo Distancias ###### Para igualar distancias entre metodos / entrada: Archivo de distancias *.dat
	
	for files in dirs_dist:
		if "dat" in files:
			arc_dist = files
		if "FASTA" in files:
			arc_fasta = files

	dist_dic, dist_dic_aa = Herramientas.distancias(input_distancias+arc_dist,input_distancias+arc_fasta)
	msa_con_gaps,gaps = Herramientas.msa(input_distancias+arc_fasta)
	

	###### Generar Datos desde DCA ######

	DCA = open (ruta+parsed["directorios"]["dca_dir"] , "r")
	DCA_Z  = Modulo_DCA.correcion_dca(DCA,msa_con_gaps,dist_dic,temporal,gaps) ### Algunas dan alrevez ver las correciones de las posiciones
	

	###### Generar Roc DCA #####
	TPR_Rate_DCA,FPR_Rate_DCA,Venn_TP_DCA,ALL_VENN = Modulo_Combinado.roc(DCA_Z,dist_dic,"DCA",graficos_ruta,temporal,parsed["parametros"]["valor_corte_venn"],ALL_VENN)

	###### Generar Datos desde Mistic ######
	
	MI = open (ruta+parsed["directorios"]["mis_dir"], "r")
	Final = open (temporal+"My_final", "w")
	Mis_Z,Dicc_Mis =Modulo_Mistic.generar_datos(MI,Final)
	
	###### Generar Roc Mistic #####
	TPR_Rate_MI,FPR_Rate_MI,Venn_TP_MI,ALL_VENN = Modulo_Combinado.roc(Mis_Z,dist_dic,"Mistic",graficos_ruta,temporal,parsed["parametros"]["valor_corte_venn"],ALL_VENN)

	
	###### Caso A comparar #######
	###### "Aditiva","Multiplicativa","Energia","MIp","Parametrica_25","Parametrica_75","DCA","Mistic"
	
	###### Aditiva
	ruta_datos = ruta+'//'+parsed["parametros"]["metodo_comb"]+'/'
	dirs = os.listdir(ruta_datos)
	FP = open(ruta_datos+parsed["parametros"]["familia_FP"],"r")
	TP = open(ruta_datos+parsed["parametros"]["familia_TP"],"r")
	Comb_Z,Comb_Dist = Modulo_Combinado.armado_diccionarios(carpetas[0],FP,TP)
	
	##### Venn Para los otros metodos ####
	# Venn_1
	ruta_datos = ruta+'//'+parsed["parametros"]["venn_1"]+'/'
	dirs = os.listdir(ruta_datos)
	FP = open(ruta_datos+parsed["parametros"]["familia_FP"],"r")
	TP = open(ruta_datos+parsed["parametros"]["familia_TP"],"r")
	Mult_Z,Mult_Dist = Modulo_Combinado.armado_diccionarios(parsed["parametros"]["venn_1"],FP,TP)
	TPR_Rate_1,FPR_Rate_1 = Modulo_Combinado.roc_resto(Mult_Z,Mult_Dist,parsed["parametros"]["venn_1"],graficos_ruta,temporal)
	# Venn_2
	ruta_datos = ruta+'//'+parsed["parametros"]["venn_2"]+'/'
	dirs = os.listdir(ruta_datos)
	FP = open(ruta_datos+parsed["parametros"]["familia_FP"],"r")
	TP = open(ruta_datos+parsed["parametros"]["familia_TP"],"r")
	Para_Z,Para_Dist = Modulo_Combinado.armado_diccionarios(parsed["parametros"]["venn_2"],FP,TP)
	TPR_Rate_2,FPR_Rate_2 = Modulo_Combinado.roc_resto(Para_Z,Para_Dist,parsed["parametros"]["venn_2"],graficos_ruta,temporal)
		
	
	###### Generar Roc Combinado #####
	TPR_Rate_C,FPR_Rate_C,venn_TP_Comb,ALL_VENN = Modulo_Combinado.roc(Comb_Z,Comb_Dist,parsed["parametros"]["metodo_comb"],graficos_ruta,temporal,parsed["parametros"]["valor_corte_venn"],ALL_VENN)

	#Modulo_Combinado.roc_all_zoom(TPR_Rate_MI,FPR_Rate_MI,TPR_Rate_DCA,FPR_Rate_DCA,TPR_Rate_C,FPR_Rate_C,parsed["parametros"]["metodo_comb"],graficos_ruta,resultados_ruta)
	Modulo_Combinado.roc_all(TPR_Rate_MI,FPR_Rate_MI,TPR_Rate_DCA,FPR_Rate_DCA,TPR_Rate_C,FPR_Rate_C,parsed["parametros"]["metodo_comb"],graficos_ruta,resultados_ruta)
	
	
	
	
	######### Cada 100 ##########
	Z_TP = []
	Z_FP = []
	casos_graf = []
	
	contar_hasta = parsed["parametros"]["contar_hasta"]
	#carpetas = ["Aditiva","Multiplicativa","Energia","MIp","Parametrica_25","Parametrica_75","DCA","Mistic"]
	Zeta_corte = parsed["parametros"]["Z_corte_DCA"] ##### Valor para el corte del grafico
	Z_TP, Z_FP = Modulo_Combinado.clasificacador_100(DCA_Z,dist_dic,Z_TP,Z_FP,Zeta_corte,"DCA",temporal,graficos_ruta,contar_hasta)
	casos_graf.append("DCA")
	
	Zeta_corte = parsed["parametros"]["Z_corte_Mis"]
	Z_TP, Z_FP  = Modulo_Combinado.clasificacador_100(Mis_Z,dist_dic,Z_TP,Z_FP,Zeta_corte,"Mistic",temporal,graficos_ruta,contar_hasta)
	casos_graf.append("Mistic")
	
	Zeta_corte = parsed["parametros"]["Z_corte_Comb"]
	Z_TP, Z_FP  = Modulo_Combinado.clasificacador_100(Comb_Z,Comb_Dist,Z_TP,Z_FP,Zeta_corte,parsed["parametros"]["metodo_comb"],temporal,graficos_ruta,contar_hasta)
	casos_graf.append(parsed["parametros"]["metodo_comb"])
	
	Modulo_Combinado.graficos_cada_100 (Z_TP, temporal,graficos_ruta,casos_graf,contar_hasta)
	
	######### Cada 5 ##########

	Z_TP = []
	Z_FP = []
	Z_TP, Z_FP = Modulo_Combinado.clasificacador_5(DCA_Z,dist_dic,Z_TP,Z_FP,Zeta_corte,"DCA",temporal,graficos_ruta,parsed["parametros"]["corte_tp_a"])
	Z_TP, Z_FP  = Modulo_Combinado.clasificacador_5(Mis_Z,dist_dic,Z_TP,Z_FP,Zeta_corte,"Mistic",temporal,graficos_ruta,parsed["parametros"]["corte_tp_a"])
	Z_TP, Z_FP  = Modulo_Combinado.clasificacador_5(Comb_Z,Comb_Dist,Z_TP,Z_FP,Zeta_corte,parsed["parametros"]["metodo_comb"],temporal,graficos_ruta,parsed["parametros"]["corte_tp_a"])	
	Modulo_Combinado.graficos_contar_FP(Z_TP, temporal,graficos_ruta,parsed["parametros"]["corte_tp_a"],casos_graf)

	
	######### Cada 10 ##########

	Z_TP = []
	Z_FP = []
	Z_TP, Z_FP = Modulo_Combinado.clasificacador_5(DCA_Z,dist_dic,Z_TP,Z_FP,Zeta_corte,"DCA",temporal,graficos_ruta,parsed["parametros"]["corte_tp_b"])
	Z_TP, Z_FP  = Modulo_Combinado.clasificacador_5(Mis_Z,dist_dic,Z_TP,Z_FP,Zeta_corte,"Mistic",temporal,graficos_ruta,parsed["parametros"]["corte_tp_b"])
	Z_TP, Z_FP  = Modulo_Combinado.clasificacador_5(Comb_Z,Comb_Dist,Z_TP,Z_FP,Zeta_corte,parsed["parametros"]["metodo_comb"],temporal,graficos_ruta,parsed["parametros"]["corte_tp_b"])	
	Modulo_Combinado.graficos_contar_FP(Z_TP, temporal,graficos_ruta,parsed["parametros"]["corte_tp_b"],casos_graf)
	
	######### Extras DCA ##########

	Modulo_DCA.distri_DCA(temporal,dist_dic,graficos_ruta)
	
	######### Diagrama Venn #########
	
	
	venn_TP_Venn_1,ALL_VENN= Modulo_Combinado.Class_Venn(dist_dic,Mult_Z,temporal,parsed["parametros"]["venn_1"],parsed["parametros"]["valor_corte_venn"],ALL_VENN)
	venn_TP_Venn_2,ALL_VENN= Modulo_Combinado.Class_Venn(dist_dic,Para_Z,temporal,parsed["parametros"]["venn_2"],parsed["parametros"]["valor_corte_venn"],ALL_VENN)### Corregir dic
	
	Modulo_Combinado.Venn_Inter(dist_dic,venn_TP_Comb,Venn_TP_DCA,Venn_TP_MI,graficos_ruta,"comb",ALL_VENN,parsed["parametros"]["metodo_comb"]) #Genera Venn DCA/Mistic/Metodo_elegido
	
	venn_all_metodos=Modulo_Combinado.Venn_Unificar(venn_TP_Venn_1,venn_TP_Venn_2,venn_TP_Comb) #Unifico los 3 venn
	
	Modulo_Combinado.Venn_Inter(dist_dic,venn_all_metodos,Venn_TP_DCA,Venn_TP_MI,graficos_ruta,"all",ALL_VENN,"Dunn") #Genera Venn DCA/Mistic/Unificado
	
	Modulo_Combinado.Venn_Intra(ALL_VENN,venn_TP_Comb,venn_TP_Venn_1,venn_TP_Venn_2,graficos_ruta) #Genera Venn Aditico/Multi/Parame

if parsed["parametros"]["analisis"] == "D":  #### Debug , para probar msa
	
	ALL_VENN = {} # Generar Keys para Venn
	
	###### Generar Archivo Distancias ###### Para igualar distancias entre metodos / entrada: Archivo de distancias *.dat
	
	for files in dirs_dist:
		if "dat" in files:
			arc_dist = files
		if "FASTA" in files:
			arc_fasta = files

	dist_dic, dist_dic_aa = Herramientas.distancias(input_distancias+arc_dist,input_distancias+arc_fasta)
	msa_con_gaps,gaps = Herramientas.msa(input_distancias+arc_fasta)
	
	print(len(msa_con_gaps))
	print(gaps)
	
	DCA = open (ruta+parsed["directorios"]["dca_dir"] , "r")
	DCA_Z  = Modulo_DCA.correcion_dca(DCA,msa_con_gaps,dist_dic,temporal,gaps)

