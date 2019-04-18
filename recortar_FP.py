
##### Para resumir el archivo FP
import os
input_FP =open('all_FP.dat' , "r")
salida_FP = open('all_FP_recortado.dat' , "w")
for linea in input_FP:
		if "---------- TP" in linea:
			salida_FP.write(linea)
			break
		else:
			salida_FP.write(linea)
salida_FP.close()
os.remove("all_FP.dat")
os.rename('all_FP_recortado.dat','all_FP.dat')

