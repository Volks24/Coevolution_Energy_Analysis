# encoding: utf-8
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import operator;
import numpy as np
from sklearn import metrics


######## Ploteo Formato ######
font = {'family': 'serif','color':  'darkred','weight': 'normal','size': 16, } # PAra darle formato a los ejes

######## Range con Float ######

def frange(start, stop, step):
	i = start
	while i < stop:
		yield i
		i += step
	return


######## Distribuciones #######

def grafico_distribuciones(archivos,contacto,no_contacto,graficos_ruta):
	contacto_x = []
	contacto_y = []
	no_contacto_x = []
	no_contacto_y = []
	for datos in contacto:
		valores = datos.split(" ")
		contacto_x.append(round((float(valores[0])),3))
		contacto_y.append(round((float(valores[1])),2))
	for datos in no_contacto:
		valores = datos.split(" ")
		no_contacto_x.append(round((float(valores[0])),3))
		no_contacto_y.append(round((float(valores[1])),3))
	fig, ax = plt.subplots()
	ax.plot(contacto_x,contacto_y,label="Contacto",color = "g" ,linewidth = 0.5 ,antialiased = "True")
	ax.plot(no_contacto_x,no_contacto_y,label="No Contacto",color = "r",linewidth = 0.5,antialiased = "True")
	plt.ylabel("Pares",fontdict=font)
	plt.xlabel("Z ("+str(archivos)+")", fontdict=font)
	plt.title('Distribución '+archivos , fontdict=font)
	ax.axvline(x=3)
	ax.grid(linestyle='--', linewidth=0.2)
	plt.legend()	
	plt.savefig(graficos_ruta+"Distribucion_"+str(archivos)+".png")
	plt.clf()
	return()

######## Diccionarios #######

def armado_diccionarios(carpetas,FP,TP):
	pares = []
	line = TP.readlines()
	for i in range (1,len(line)):
		if "----------" in line[i]:
			break
		else:
			datos = line[i].split(" ")
			Z = round(float(datos[2]),2)
			dist = round(float(datos[3]),2)
			pares.append(datos[0]+"\t"+datos[1]+"\t"+str(Z)+"\t"+str(dist))
	line = FP.readlines()
	for i in range (1,len(line)):
		if "----------" in line[i]:
			break
		else:
			datos = line[i].split(" ")
			Z = round(float(datos[2]),2)
			dist = round(float(datos[3]),2)
			pares.append(datos[0]+"\t"+datos[1]+"\t"+str(Z)+"\t"+str(dist))
	return(pares)
	
######## Roc #######

def grafico_roc(datos,caso,roc_all_TP,roc_all_FP,datos_auc,graficos_ruta):
	labely = "TPR (sensibilidad)"
	labelx = "FPR (1-especificidad)"
	TPR_Rate = []
	FPR_Rate = []
	for j in frange(-5.0,5.0,0.3):
		J = round(j,3)
		TP = 0 # Zeta Alto y Distancia Corta
		FP = 0 # Zeta Alto y Distancia Grande
		TN = 0 # Zeta Bajo y Distancia Grande
		FN = 0 # 
		for i in range (0,len(datos)):
			valores = datos[i].split("\t")
			Zeta = round(float(valores[2]),2)
			Dist = round(float(valores[3]),3)
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
	AUC=round(metrics.auc(FPR_Rate,TPR_Rate, reorder = True),4)
	datos_auc.write(caso+" "+str(AUC)+"\n")
	roc_all_TP[caso] = TPR_Rate
	roc_all_FP[caso] = FPR_Rate
	plt.title("Curva ROC "+str(caso) , fontdict=font)
	plt.grid(True)
	plt.ylabel(labely,fontdict=font)
	plt.xlabel(labelx, fontdict=font)
	plt.plot(FPR_Rate,TPR_Rate,marker='.', linestyle='solid',label="Curva Roc",color = "g", linewidth=0.5)
	plt.plot([0,0.5,1],[0,0.5,1],linestyle='solid',color = "k", linewidth=0.5)
	plt.axis([0,1,0,1]) #establece los valores límites de los ejes a v = [xmin, xmax, ymin, ymax]
	plt.savefig(graficos_ruta+"Curva_Roc_"+str(caso)+".png")
	#plt.show()
	plt.clf()
	return (roc_all_TP,roc_all_FP)
	
def grafico_roc_all(roc_all,roc_all_FP,roc_all_TP,datos_auc,graficos_ruta):
	labely = "TPR (sensibilidad)"
	labelx = "FPR (1-especificidad)"
	plt.title("Curva ROC " , fontdict=font)
	plt.grid(True)
	plt.ylabel(labely,fontdict=font)
	plt.xlabel(labelx, fontdict=font)
	for casos in roc_all:	
		plt.plot(roc_all_FP[casos],roc_all_TP[casos],marker='.', linestyle='solid',label=casos, linewidth=0.5)
	plt.legend(loc='lower right' ,shadow=True,fontsize=10)
	plt.plot([0,0.5,1],[0,0.5,1],linestyle='solid',color = "k", linewidth=0.5)
	plt.axis([0,1,0,1]) #establece los valores límites de los ejes a v = [xmin, xmax, ymin, ymax]
	plt.savefig(graficos_ruta+"Curva_Roc_all.png")
	plt.plot([0,0.5,1],[0,0.5,1],linestyle='solid',color = "k", linewidth=0.5)
	plt.axis([0,0.15,0,0.15]) #establece los valores límites de los ejes a v = [xmin, xmax, ymin, ymax]
	plt.savefig(graficos_ruta+"Curva_Roc_all_zoom.png")
	return()
	

######## Cada 100  ##########

def clasificacador(diccionarios,casos,cada_100,z,temporal,graficos_ruta):
	dicc_Z = {}
	dicc_D = {}
	salida = open(temporal+casos+"_casos_ordenados_Z"+str(z)+".txt","w")
	salida2 = open(temporal+"casos_TP_cada_5_TN_"+str(z)+".txt","a")
	for i in range (0,len(diccionarios)):
		datos = diccionarios[i].split("\t")
		dicc_Z[datos[0]+" "+datos[1]]=datos[2]
		dicc_D[datos[0]+" "+datos[1]]=datos[3]
	#### Ordenos los datos en funcion de Z
	Ordenados_Z = sorted(dicc_Z.items(), key=operator.itemgetter(1))
	Ordenados_Z.reverse()
	TP = 0
	FP = 0
	for i in range (0,101): # Reviso los primeros 100
		salida.write(str(Ordenados_Z[i][0])+"\t"+str(dicc_Z[Ordenados_Z[i][0]])+"\t"+str(dicc_D[Ordenados_Z[i][0]])+"\n")
		if float(dicc_Z[Ordenados_Z[i][0]]) > z: # Controlo Z
			if float(dicc_D[Ordenados_Z[i][0]]) < 8: # Controlo Distancia
				TP = TP + 1
			else:
				FP = FP + 1
	cada_100[casos]=str(TP)+"\t"+str(FP)+"\n"
	TP = 0
	FP = 0
	for i in range (0,len(dicc_D)): # Reviso los primeros 100
		if float(dicc_Z[Ordenados_Z[i][0]]) > z: # Controlo Distancia
			if float(dicc_D[Ordenados_Z[i][0]]) < 8:
				TP = TP + 1
			else:
				FP = FP + 1
			if TP == 5:
				break
	salida2.write(str(casos)+"\t"+str(TP)+"\t"+str(FP)+"\n")
	salida.close()
	salida2.close()
	return(cada_100)
	
def graficos_cada_100(cada_100_z_a,cada_100_z_b,z_a,z_b,temporal,graficos_ruta):
	salida_za = open(temporal+"Cada_100_Z_"+str(z_a)+".txt","w")
	salida_zb = open(temporal+"Cada_100_Z_"+str(z_b)+".txt","w")
	salida_za.write("Caso\tTP\tFP\n")
	salida_zb.write("Caso\tTP\tFP\n")
	TP = []
	FP = []
	TP_2 = []
	FP_2= []
	casos_tratado = []
	width = 0.2  # the width of the bars
	for llaves in cada_100_z_a:
		datos = cada_100_z_a[llaves].split("\t")
		TP.append(int(datos[0]))
		FP.append(int(datos[1]))
		casos_tratado.append(llaves)
		salida_za.write(llaves+"\t"+str(datos[0])+"\t"+str(datos[1]))
	for llaves in cada_100_z_b:
		datos = cada_100_z_b[llaves].split("\t")
		TP_2.append(int(datos[0]))
		FP_2.append(int(datos[1]))
		salida_zb.write(llaves+"\t"+str(datos[0])+"\t"+str(datos[1]))
	ind = np.arange(len(TP)) # Numero de columnas
	fig, ax = plt.subplots()
	rects1 = ax.bar(ind - 0.40, TP, width, color='#25d366', label='TP Z='+str(z_a))
	rects2 = ax.bar(ind - 0.2, FP, width, color='#FFF290', label='FP Z='+str(z_a))
	rects3 = ax.bar(ind , TP_2, width, color='#9F90FF', label='TP Z='+str(z_b))
	rects4 = ax.bar(ind + 0.2, FP_2, width, color='#FF9C90', label='FP Z='+str(z_b))
	ax.set_ylabel('N de Casos',font)
	ax.set_title("Casos",font)
	ax.set_xticks(ind)
	ax.set_xticklabels(casos_tratado,fontsize = 10) # Tiene que coincidir con el numeros de Z!!!! (el largo)
	ax.legend()
	plt.savefig(graficos_ruta+"Cada_100.png")
	plt.clf()
	salida_za.close()
	salida_zb.close()
	return()

def graficos_cada_5(Z,temporal,graficos_ruta):
	entrada = open(temporal+"casos_TP_cada_5_TN_"+str(Z)+".txt","r")
	archivo =entrada.readlines()
	ref = []
	tp = []
	fp = []
	for i in range (0,len(archivo)):
		datos = archivo[i].split("\t")
		ref.append(datos[0])
		tp.append(int(datos[1]))
		fp.append(int(datos[2]))
	width = 0.2  # the width of the bars
	ind = np.arange(len(ref)) # Numero de columnas
	fig, ax = plt.subplots()
	rects1 = ax.bar(ind  , fp, width, color='#25d366', label='FP')
	rects2 = ax.bar(ind + 0.2, tp, width, color='#9F90FF', label='TP') # activo / desactivo TP
	ax.set_ylabel('N de Casos',font)
	ax.set_title("Casos FP cada 5 TP",font)
	ax.set_xticks(ind)
	ax.set_xticklabels(ref,fontsize = 10) # Tiene que coincidir con el numeros de Z!!!! (el largo)
	ax.legend()
	plt.savefig(graficos_ruta+"Cada_5.png")
	plt.clf()
	
	





