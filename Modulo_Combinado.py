# encoding: utf-8
import Herramientas
from sklearn import metrics
import matplotlib.pyplot as plt
import operator;
import numpy as np
from matplotlib_venn import venn3 , venn3_circles



######## Ploteo Formato ######
font = {'family': 'serif','color':  'darkred','weight': 'normal','size': 16, } # PAra darle formato a los ejes


def armado_diccionarios(carpetas,FP,TP):
	Zeta = {}
	Dist = {}
	line = TP.readlines()
	for i in range (1,len(line)):
		if "----------" in line[i]:
			break
		else:
			datos = line[i].split(" ")
			Z = round(float(datos[2]),2)
			distan = round(float(datos[3]),2)
			Zeta[datos[0]+" "+datos[1]]= Z
			Dist[datos[0]+" "+datos[1]]= distan
	line = FP.readlines()
	for i in range (1,len(line)):
		if "----------" in line[i]:
			break
		else:
			datos = line[i].split(" ")
			Z = round(float(datos[2]),2)
			distan = round(float(datos[3]),2)
			Zeta[datos[0]+" "+datos[1]]= Z
			Dist[datos[0]+" "+datos[1]]= distan
	return(Zeta,Dist)

####### Curva Roc Comparaciones ########

def roc(Z_Dic,dist_dic,caso,graficos_ruta,temporal,valor_corte_venn,ALL_VENN):
	labely = "TPR (sensibilidad)"
	labelx = "FPR (1-especificidad)"
	venn_file=open(temporal+"venn.txt", "a")
	venn_TP = []
	TPR_Rate = []
	FPR_Rate = []
	datos_auc = open (temporal+"Auc_Comparaciones.txt" , "a") 
	datos_caso = open (temporal+caso+"_casos.txt" , "w")
	for j in Herramientas.frange(-5.0,5.0,0.3):
		J = round(j,3)
		TP = 0 # Zeta Alto y Distancia Corta
		FP = 0 # Zeta Alto y Distancia Grande
		TN = 0 # Zeta Bajo y Distancia Grande
		FN = 0 #  Zeta Bajo y Distancia Corta
		for keys in Z_Dic:
			try:
				Zeta = round(float(Z_Dic[keys]),2)
				Dist = round(float(dist_dic[keys]),3)
			except:
				next
			if (float(Zeta) > float(J)):
				try:
					if float(Dist) < 8:	
						TP = TP + 1
						if ( valor_corte_venn > (J - 0.15) ) and (valor_corte_venn < (J + 0.15))  :
							valor_cort = J
							venn_TP.append(keys)
							ALL_VENN[keys] = 1
							venn_file.write(str(caso)+" "+str(keys)+"\n")
					else:
						FP = FP + 1
				except UnboundLocalError:
					print(keys)
			if float(Zeta) < float(J):
				try:
					if float(Dist) < 8:
						FN = FN + 1
					else:
						TN = TN + 1
				except UnboundLocalError:
					print(keys)	
		if TP + FN > 0:
			TPR = (TP / (TP + FN))
		else:
			TPR = 0
		if FP + TN > 0:
			FPR = (FP / (FP + TN))
		else:
			FPR = 0
		TPR_Rate.append(TPR)
		FPR_Rate.append(FPR)
		datos_caso.write("CORTE\t"+str(J)+"\tTP\t"+str(TP)+"\tFP\t"+str(FP)+"\tTN\t"+str(TN)+"\tFN\t"+str(FN)+"\tTPR\t"+str(round(TPR,4))+"\tFPR\t"+str(round(FPR,4))+"\n")
	AUC=round(metrics.auc(FPR_Rate,TPR_Rate, reorder = True),4)
	datos_auc.write(caso+" "+str(AUC)+"\n")
	datos_caso.write("Total Casos\t"+str(FP+TN+TP+FP)+"\n")
	plt.title("Curva ROC "+str(caso) , fontdict=font)
	plt.grid(True)
	plt.ylabel(labely,fontdict=font)
	plt.xlabel(labelx, fontdict=font)
	plt.plot(FPR_Rate,TPR_Rate,marker='.', linestyle='solid',label="Curva Roc",color = "g", linewidth=0.5)
	plt.plot([0,0.5,1],[0,0.5,1],linestyle='solid',color = "k", linewidth=0.5)
	plt.axis([0,1,0,1]) #establece los valores límites de los ejes a v = [xmin, xmax, ymin, ymax]
	plt.savefig(graficos_ruta+"Curva_Roc_"+str(caso)+".png")
	plt.clf()
	datos_auc.close()
	datos_caso.close()
	venn_file.close()
	return (TPR_Rate,FPR_Rate,venn_TP,ALL_VENN)
	
def roc_resto(Z_Dic,dist_dic,caso,graficos_ruta,temporal):
	labely = "TPR (sensibilidad)"
	labelx = "FPR (1-especificidad)"
	TPR_Rate = []
	FPR_Rate = []
	datos_auc = open (temporal+"Auc_Comparaciones.txt" , "a") 
	datos_caso = open (temporal+caso+"_casos.txt" , "w") 
	for j in Herramientas.frange(-5.0,5.0,0.3):
		J = round(j,3)
		TP = 0 # Zeta Alto y Distancia Corta
		FP = 0 # Zeta Alto y Distancia Grande
		TN = 0 # Zeta Bajo y Distancia Grande
		FN = 0 #  Zeta Bajo y Distancia Corta
		for keys in Z_Dic:
			try:
				Zeta = round(float(Z_Dic[keys]),2)
				Dist = round(float(dist_dic[keys]),3)
			except:
				next
			if (float(Zeta) > float(J)):
				if float(Dist) < 8:	
					TP = TP + 1
				else:
					FP = FP + 1
			if float(Zeta) < float(J):
				if float(Dist) < 8:
					FN = FN + 1
				else:
					TN = TN + 1	
		if TP + FN > 0:
			TPR = (TP / (TP + FN))
		else:
			TPR = 0
		if FP + TN > 0:
			FPR = (FP / (FP + TN))
		else:
			FPR = 0
		TPR_Rate.append(TPR)
		FPR_Rate.append(FPR)
		datos_caso.write("CORTE\t"+str(J)+"\tTP\t"+str(TP)+"\tFP\t"+str(FP)+"\tTN\t"+str(TN)+"\tFN\t"+str(FN)+"\tTPR\t"+str(round(TPR,4))+"\tFPR\t"+str(round(FPR,4))+"\n")
	AUC=round(metrics.auc(FPR_Rate,TPR_Rate, reorder = True),4)
	datos_auc.write(caso+" "+str(AUC)+"\n")
	datos_caso.write("Total Casos\t"+str(FP+TN+TP+FP)+"\n")
	plt.title("Curva ROC "+str(caso) , fontdict=font)
	plt.grid(True)
	plt.ylabel(labely,fontdict=font)
	plt.xlabel(labelx, fontdict=font)
	plt.plot(FPR_Rate,TPR_Rate,marker='.', linestyle='solid',label="Curva Roc",color = "g", linewidth=0.5)
	plt.plot([0,0.5,1],[0,0.5,1],linestyle='solid',color = "k", linewidth=0.5)
	plt.axis([0,1,0,1]) #establece los valores límites de los ejes a v = [xmin, xmax, ymin, ymax]
	plt.savefig(graficos_ruta+"Curva_Roc_"+str(caso)+".png")
	plt.clf()
	datos_auc.close()
	datos_caso.close()
	return (TPR_Rate,FPR_Rate)

####### Curva Roc Comparaciones All ########


def roc_all(TPR_Rate_MI,FPR_Rate_MI,TPR_Rate_DCA,FPR_Rate_DCA,TPR_Rate_C,FPR_Rate_C,caso,graficos_ruta,resultados_ruta):
	labely = "TPR (sensibilidad)"
	labelx = "FPR (1-especificidad)"
	plt.title("Curva ROC " , fontdict=font)
	plt.grid(True)
	plt.ylabel(labely,fontdict=font)
	plt.xlabel(labelx, fontdict=font)
	plt.plot(FPR_Rate_MI,TPR_Rate_MI,marker='.', linestyle='solid',label="Mistic", linewidth=1 , color ='#FF9C90')
	plt.plot(FPR_Rate_DCA,TPR_Rate_DCA,marker='.', linestyle='solid',label="DCA", linewidth=1,color ="#9F90FF")
	plt.plot(FPR_Rate_C,TPR_Rate_C,marker='.', linestyle='solid',label=caso, linewidth=1,color ="#25d366")
	plt.legend(loc='lower right' ,shadow=True,fontsize=10)
	plt.plot([0,0.5,1],[0,0.5,1],linestyle='solid',color = "k", linewidth=0.5)
	plt.axis([0,1,0,1]) #establece los valores límites de los ejes a v = [xmin, xmax, ymin, ymax]
	plt.savefig(graficos_ruta+"Curva_Roc_Comb.png")
	plt.plot([0,0.5,1],[0,0.5,1],linestyle='solid',color = "k", linewidth=0.5)
	plt.axis([0,0.15,0,0.15]) #establece los valores límites de los ejes a v = [xmin, xmax, ymin, ymax]
	plt.savefig(graficos_ruta+"Curva_Roc_Comb_Zoom.png")
	return()
	

def clasificacador_100(Dic_Z,dist_dic,Z_TP, Z_FP ,Zeta_corte,caso,temporal,graficos_ruta,corte):
	salida = open(temporal+caso+"_cada_"+str(corte)+".txt" , "w")
	#### Ordenos los datos en funcion de Z
	Ordenados_Z = sorted(Dic_Z.items(), key=operator.itemgetter(1))
	Ordenados_Z.reverse()
	#### key(Ordenados_Z[0][0])
	Herramientas.archivo_z(Dic_Z,temporal,caso)
	TP = 0
	FP = 0
	salida.write("Par\tZ\tDistancia\n")
	for i in range (0,corte): # Reviso los primeros 100
		if float(Ordenados_Z[i][1]) > Zeta_corte: # Controlo Z
			if float(dist_dic[Ordenados_Z[i][0]]) < 8: # Controlo Distancia
				TP = TP + 1
			else:
				FP = FP + 1
		salida.write(str(Ordenados_Z[i][0])+"\t"+str(Ordenados_Z[i][1])+"\t"+str(dist_dic[Ordenados_Z[i][0]])+"\n")
	Z_TP.append(TP)
	Z_FP.append(FP)
	salida.write("Total TP "+str(TP)+" Total FP "+str(FP))
	salida.close()
	return(Z_TP,Z_FP)

def clasificacador_5(Dic_Z,dist_dic,Z_TP, Z_FP ,Zeta_corte,caso,temporal,graficos_ruta,corte):
	#### Ordenos los datos en funcion de Z
	Ordenados_Z = sorted(Dic_Z.items(), key=operator.itemgetter(1))
	Ordenados_Z.reverse()
	#### key(Ordenados_Z[0][0])
	TP = 0
	FP = 0
	for i in range (0,len(Dic_Z)): # Reviso los primeros 100
		if float(Ordenados_Z[i][1]) > Zeta_corte: # Controlo Distancia
			if float(dist_dic[Ordenados_Z[i][0]]) < 8: # Controlo Distancia:
				TP = TP + 1
			else:
				FP = FP + 1
			if TP == corte:
				break
	Z_TP.append(int(TP))
	Z_FP.append(int(FP))
	return(Z_TP,Z_FP)



def graficos_cada_100(Z_TP, temporal,graficos_ruta,casos,corte):
	width = 0.2  # the width of the bars
	ind = np.arange(1, 4) # Columnas                                                 
	fig, ax = plt.subplots()
	ax.bar(ind+0.25,Z_TP, width,align='center', color=['#FF9C90',"#9F90FF","#25d366"] ,label="")
	ax.set_ylabel('N de Casos',font)
	ax.set_title("Casos TP entre "+str(corte)+" primeros",font)
	ax.set_xticks(ind+0.25)
	ax.set_xticklabels(casos,fontsize = 10) # Tiene que coincidir con el numeros de Z!!!! (el largo)
	ax.legend()
	plt.savefig(graficos_ruta+"Comp_Cada_"+str(corte)+".png")
	plt.clf()
	return()

def graficos_contar_FP(Z_TP, temporal,graficos_ruta,num_casos,casos):
	width = 0.2  # the width of the bars
	ind = np.arange(1, 4) # Columnas
	fig, ax = plt.subplots()
	ax.bar(ind+0.25,Z_TP, width,align='center', color=['#FF9C90',"#9F90FF","#25d366"], label="")
	ax.set_ylabel("Casos",font)
	ax.set_title('N° de FP al contar '+str(num_casos)+' TP',font)
	ax.set_xticks(ind+0.25)
	ax.set_xticklabels(casos,fontsize = 10) # Tiene que coincidir con el numeros de Z!!!! (el largo)
	ax.legend()
	plt.savefig(graficos_ruta+"Comp_Cada_"+str(num_casos)+".png")
	plt.clf()
	return()

############## Diagrama de Venn ##########
	
def Class_Venn(dist_dic,Z_Dic,temporal,caso,valor_corte_venn,ALL_VENN):	
	venn_file=open(temporal+"venn.txt", "a")
	valor_corte_venn = int (1) # valor de Z para corte de diagrmas
	venn_TP = []
	TPR_Rate = []
	FPR_Rate = []
	for j in Herramientas.frange(-5.0,5.0,0.3):
		J = round(j,3)
		for keys in Z_Dic:
			try:
				Zeta = round(float(Z_Dic[keys]),2)
				Dist = round(float(dist_dic[keys]),3)
				if (float(Zeta) > float(J)):
					if float(Dist) < 8:	
						if ( valor_corte_venn > (J - 0.15) ) and (valor_corte_venn < (J + 0.15))  :
							valor_cort = J
							venn_TP.append(keys)
							ALL_VENN[keys] = 1
							venn_file.write(str(caso)+" "+str(keys)+"\n")
			except:
				next
	venn_file.close()
	return(venn_TP,ALL_VENN)

def Venn_Unificar(venn_TP_Mult,venn_TP_Para,venn_TP_Comb):
	venn_all = []
	for keys in venn_TP_Mult:
		if keys in venn_all:
			next
		else:	
			venn_all.append(keys)
	for keys in venn_TP_Para:
		if keys in venn_all:
			next
		else:	
			venn_all.append(keys)
	for keys in venn_TP_Comb:
		if keys in venn_all:
			next
		else:	
			venn_all.append(keys)
	return(venn_all)


def Venn_Inter(dist_dic,dunn_dic,dca_pares,mystic_pares,graficos_ruta,caso_venn,ALL_VENN,caso_graf):
	
	# Armo conjuntos entre metodos
	# siguiente orden: Abc, aBc, ABc, abC, AbC, aBC, ABC.
	# DCA , MY , DUNN 
	conj_dca = 0 # Abc
	conj_my = 0 # aBc
	conj_du = 0 # abC
	conj_dca_my = 0 #ABc
	conj_dca_du = 0 # AbC
	conj_my_du = 0 # aBC
	conj_dca_my_du = 0 #ABC
	
	for llaves in ALL_VENN:
		if (llaves in dunn_dic):
			if (llaves in dca_pares) and (llaves in mystic_pares):
				conj_dca_my_du += 1 #ABC
			elif (llaves in dca_pares):
				conj_dca_du += 1 # AbC
			elif (llaves in mystic_pares):
				conj_my_du += 1 # aBC
			else:
				conj_du  += 1 # abC
		else:
			if (llaves in dca_pares) and (llaves in mystic_pares):
				conj_dca_my += 1 #ABc
			elif (llaves in dca_pares):
				conj_dca += 1 # Abc
			elif (llaves in mystic_pares):
				conj_my += 1 # aBc

	subsets= (conj_dca,conj_my,conj_dca_my,conj_du,conj_dca_du,conj_my_du,conj_dca_my_du)

	venn3(subsets,set_labels = ('DCA', 'Mystic', caso_graf))
	venn3_circles(subsets, color="#008000", alpha=1, linestyle="-.", linewidth=3)
	plt.savefig(graficos_ruta+"venn_metodos_"+caso_venn+".png", dpi=720) # ver bien dnd salvar el grafico
	plt.clf()


def Venn_Intra(dist_dic,venn_TP_Comb,venn_TP_Mult,venn_TP_Para,graficos_ruta):
	conj_ad = 0 # Abc
	conj_mu = 0 # aBc
	conj_pa = 0 # abC
	conj_ad_mu = 0 #ABc
	conj_ad_pa = 0 # AbC
	conj_mu_pa = 0 # aBC
	conj_ad_mu_pa = 0 #ABC

	for llaves in dist_dic:
		if (llaves in venn_TP_Comb):
			if (llaves in venn_TP_Mult) and (llaves in venn_TP_Para):
				conj_ad_mu_pa += 1 #ABC
			elif (llaves in venn_TP_Para):
				conj_ad_pa += 1 # AbC
			elif (llaves in venn_TP_Comb):
				conj_ad_mu += 1 # ABc
			else:
				conj_ad  += 1 # Abc
		else:
			if (llaves in venn_TP_Mult) and (llaves in venn_TP_Para):
				conj_mu_pa += 1 #aBC
			elif (llaves in venn_TP_Mult):
				conj_mu += 1 # aBc
			elif (llaves in venn_TP_Para):
				conj_pa += 1 # abC

	subsets= (conj_ad,conj_mu,conj_ad_mu,conj_pa,conj_ad_pa,conj_mu_pa,conj_ad_mu_pa)
	venn3(subsets,set_labels = ('Aditiva', 'Multipli.', 'Para'))
	venn3_circles(subsets, color="#008000", alpha=1, linestyle="-.", linewidth=3)
	plt.savefig(graficos_ruta+"venn_dunn.png", dpi=720) 
	plt.clf()
