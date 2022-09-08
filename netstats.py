#!/usr/bin/python3
import sys
import csv
from grafo import *
from grafo_operaciones import *
COMANDO_INVALIDO = "[ERROR] COMANDO INVALIDO"


# ---------------------------------- #
# ------ FUNCIONES AUXILIARES ------ #
# ---------------------------------- #

def generar_camino(padre, inicio):
	"""
	Genera el camino a través del diccionario de padres, desde el vértice de inicio.
	Pre: recibe el diccionario de padres y el vértice de inicio.
	Post: devuelve el camino formado (lista vacía si no hay camino).
	"""
	camino = []
	act = inicio
	while act != None:
		camino.append(act)
		if act not in padre:
			return []
		act = padre[act]
	return camino

def imprimir_camino(camino, costo):
	"""
	Imprime el camino en el orden deseado, y el costo (o largo) del mismo. Si
	sentido_inverso es True, se imprime el camino de atrás para adelante.
	Pre: recibe el camino, su costo, y el booleano sentido_inverso.
	"""
	largo = len(camino)
	if largo == 1:
		print("{}".format(camino[0]))
	for i in camino[0:largo - 1]:
		print("{} ->".format(i), end = " ")
	print("{}".format(camino[largo - 1]))
	if costo != -1:
		print("Costo: {}".format(costo))

def obtener_grados_salida(grafo):
	"""
	Funcion que obtiene los hijos de cada vertice del grafo y su grado de salida 
	Pre: recibe un grafo
	Post: devuelve los hijos y el grado de salida de cada vertice
	"""
	hijos = {}
	grados_salida = {}
	for v in grafo.obtener_vertices():
		grados_salida[v] = 0
		hijos[v] = {}
		for w in grafo.obtener_adyacentes(v):
			grados_salida[v] += 1
			hijos[v][w] = None
	return hijos, grados_salida

def listar_operaciones():
	"""
	Comando LISTAR_OPERACIONES.
	Muestra las operaciones disponibles. Imprime una línea por cada
	comando implementado. 
	"""
	print("camino")
	print("diametro")
	print("rango")
	print("navegacion")
	print("lectura")
	print("clustering")
	print("ciclo")


# ---------------------------------- #
# -------------- MAIN -------------- #
# ---------------------------------- #

def leer_archivo(ruta_archivo):
	"""
	Carga la wikipedia línea por línea a partir de la ruta recibida.
	Pre: recibe la ruta del archivo.
	Post: devuelve el grafo wikipedia.
	"""
	wiki = Grafo(True)
	with open(ruta_archivo) as tsvfile:
		tsvreader = csv.reader(tsvfile, delimiter="\t")
		for line in tsvreader:
			wiki.agregar_vertice(line[0])
			for i in range(1, len(line)):
				wiki.agregar_vertice(line[i])
				wiki.agregar_arista(line[0], line[i], 0)
	return wiki

def ejecutar_netstats(ruta_archivo):
	"""
	Ejecuta los comandos implementados e imprime los resultados de los mismos.
	Pre: recibe la ruta del archivo.
	"""
	wiki = leer_archivo(ruta_archivo)
	for linea in sys.stdin:
		linea_aux = linea[:]
		linea = linea[:-1]
		lista_stdin = linea.split(" ", 1)
		if( 1 < len(lista_stdin) ):
			parametros = lista_stdin[1].split(",")
			n_parametros = len(parametros)
			
		if lista_stdin[0] == "listar_operaciones":
			listar_operaciones()
		elif lista_stdin[0] == "diametro":
			resultado, diam = diametro(wiki)
			imprimir_camino(resultado, diam)
		elif lista_stdin[0] == "camino":
			if(n_parametros != 2):
				print(COMANDO_INVALIDO)
				continue
			resultado, n = camino(wiki, parametros[0], parametros[1]) 
			if resultado:
				imprimir_camino(resultado, n)
			else: 
				print("No se encontro recorrido")
		elif lista_stdin[0] == "rango":
			if(n_parametros != 2):
				print(COMANDO_INVALIDO)
				continue
			if parametros[1] == "":
				lista_stdin_aux = linea_aux.split(" ", 1)
				parametros = lista_stdin_aux[1].split(",")
			print(rango(wiki, parametros[0], int(parametros[1])))
		elif lista_stdin[0] == "navegacion":
			if(n_parametros != 1):
				print(COMANDO_INVALIDO)
				continue
			imprimir_camino(navegacion(wiki, parametros[0]), -1)
		elif lista_stdin[0] == "lectura":
			if(n_parametros == 0):
				print(COMANDO_INVALIDO)
				continue
			resultado = lectura(wiki, parametros)
			if resultado:
				print(", ".join(resultado))
			else: 
				print("No existe forma de leer las paginas en orden")
		elif lista_stdin[0] == "clustering":
			if (len(lista_stdin) == 1):
				resultado = clustering(wiki, None)
			elif(n_parametros > 1):
				print(COMANDO_INVALIDO)
				continue
			else: resultado = clustering(wiki, parametros[0])
			print("%.3f" % resultado)
		elif lista_stdin[0] == "ciclo":
			if(n_parametros != 2):
				print(COMANDO_INVALIDO)
			resultado = ciclo(wiki, parametros[0], int(parametros[1]))
			if resultado: 
				imprimir_camino(resultado, -1)
			else: 
				print("No se encontro recorrido")
		else:
			print(COMANDO_INVALIDO)

if __name__ == "__main__":
	ejecutar_netstats(sys.argv[1])