import statistics
import Herramientas

def generar_datos(MI,Final):
	dicionario = {}
	n = 0
	sumatoria = []
	Final.write("Pos1"+"\t"+"AA1"+"\t"+"Pos2"+"\t"+"AA2"+"\t"+"MI"+"\n")
	for line in MI:
		if "#" in line:
			next 
		else:
			datos = line.split("\t")
			if (float(datos[4])) > 0.1:
				Final.write(line)
				dicionario[datos[0]+" "+datos[2]]=float(datos[4])
				sumatoria.append(float(datos[4])) 
				n = n + 1
	MI.close()
	Final.close()
	media_mistic =(statistics.mean(sumatoria))
	stdev_mistic =(statistics.stdev(sumatoria))
	MI_Z=Herramientas.calcular_z(dicionario,media_mistic,stdev_mistic)
	return(MI_Z,dicionario)
