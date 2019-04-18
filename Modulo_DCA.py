import statistics
import numpy as np
import Herramientas
import operator
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def correcion_dca(DCA,msa_gaps,dist_dic,temporal,gaps): ### Funciona ok , falta cargar las dist.
	analisis = open(temporal+"DCA_CHECK.txt" , "w")
	DCA_final = {}
	DCA_Z = {}
	dca_average = []
	for linea in DCA:
		datos_DCA = linea.split(" ")
		pos1 = int(datos_DCA[0])+1 # Numero de posicion
		pos2 = int(datos_DCA[1])+1
		gaps_1 = 0
		gaps_2 = 0
		try:
			if (msa_gaps[pos1]) == ("-"):
				next
			if (msa_gaps[pos2]) == ("-"):
				next
			else:
				for j in range (1,pos1):
					if (msa_gaps[j]) == ("-"):
							gaps_1 = gaps_1 + 1
				for i in range (pos1,pos2+1):
					if (msa_gaps[i]) == ("-"):
						gaps_2 = gaps_2 + 1
				pos1_old = pos1
				pos2_old = pos2
				pos1 = pos1 - gaps_1
				pos2 = pos2 - (gaps_1 + gaps_2)
				if (pos2 - pos1) >4:
					DCA_final[str(pos1)+" "+str(pos2)] = str(datos_DCA[2])
					dca_average.append(float(datos_DCA[2]))
					try:
						datos = dist_dic[str(pos1)+" "+str(pos2)]
						analisis.write(str(pos1_old)+" "+str(pos2_old)+" "+str(pos1)+" "+str(pos2)+" "+str(datos)+" "+str(datos_DCA[2])) # Solo para verificacion de los gaps
					except:
						analisis.write("Key Error "+str(pos1)+" "+str(pos2)+"\n")
		except KeyError:
			next
	dca_mean = float((np.mean(dca_average)))
	dca_std = float((np.std(dca_average)))
	valor_max_dca = (max(dca_average))
	DCA_Z=Herramientas.calcular_z(DCA_final,dca_mean,dca_std)
	return(DCA_Z)
	
	
def distri_DCA(temporal,dist_dic,graficos_ruta):
	contacto_x = []
	contacto_y = []
	no_contacto_x = []
	no_contacto_y = []
	datos =  open(temporal+"DCA_Z.txt" , "r")
	distribucion_contacto = {}
	distribucion_no_contacto = {}
	DCA_lineas = datos.readlines()
	for j in range(1,len(DCA_lineas)):
		Datos = DCA_lineas[j].split("\t")
		key = round(float(Datos[1]),2)
		par = Datos[0]
		if float(dist_dic[par]) < 8:
			try:  
				valor = distribucion_contacto[key]
				distribucion_contacto[key] = valor + 1
			except KeyError:
				distribucion_contacto[key] = 1
		if float(dist_dic[par]) > 8:
			try:  
				valor = distribucion_no_contacto[key]
				distribucion_no_contacto[key] = valor + 1
			except KeyError:
				distribucion_no_contacto[key] = 1
	Ordenados_Z_No_Contac = sorted(distribucion_no_contacto.items(), key=operator.itemgetter(0))
	Ordenados_Z_Contac = sorted(distribucion_contacto.items(), key=operator.itemgetter(0))
	for i in range(0,len(Ordenados_Z_Contac)): ##### Falta separa en contacto y no contacto (hacerlo antes dnd clasifico)
		contacto_x.append(round((float(Ordenados_Z_Contac[i][0])),2))
		contacto_y.append(round((float(Ordenados_Z_Contac[i][1])),2))
	for i in range(0,len(Ordenados_Z_No_Contac)):
		no_contacto_x.append(round((float(Ordenados_Z_No_Contac[i][0])),2))
		no_contacto_y.append(round((float(Ordenados_Z_No_Contac[i][1])),2))
	font = {'family': 'serif','color':  'darkred','weight': 'normal','size': 16, }
	fig, ax = plt.subplots()
	ax.plot(contacto_x,contacto_y,label="Contacto",color = "g" ,linewidth = 0.5 ,antialiased = "True")
	ax.plot(no_contacto_x,no_contacto_y,label="No Contacto",color = "r",linewidth = 0.5,antialiased = "True")
	plt.xlim(0, 5) 
	plt.ylabel("Pares",fontdict=font)
	plt.xlabel("Z DCA", fontdict=font)
	plt.title('Distribución DCA', fontdict=font)
	ax.axvline(x=3)
	ax.grid(linestyle='--', linewidth=0.2)
	plt.legend()	
	plt.savefig(graficos_ruta+"Distribucion_DCA.png")
	plt.clf()
	return()
