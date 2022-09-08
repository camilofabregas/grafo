import random
from grafo import *
from netstats import *
from collections import deque
MAX_RANGO = 20


def bfs(grafo, origen):
	"""
	Realiza un recorrido BFS (Breath First Search), a partir del vértice de origen.
	Pre: recibe el grafo y el vértice de origen.
	Post: devuelve los diccionarios de padre y orden (padre de cada vértice, y orden
	de cada vértice respecto del vértice de origen).
	"""
	orden = {}
	padre = {}
	orden[origen] = 0
	padre[origen] = None
	q = deque()
	q.append(origen)
	while q:
		v = q.popleft()
		for w in grafo.obtener_adyacentes(v):
			if w in padre: continue # También sirve chequear en 'orden'
			padre[w] = v
			orden[w] = orden[v] + 1
			q.append(w)
	return padre, orden


# ---------------------------------- #
# ------------ COMANDOS ------------ #
# ---------------------------------- # 

def camino(grafo, origen, destino):
	"""
	Comando CAMINO.
	Muestra una lista con las páginas con las cuales se navega de la página
	origen a la página destino, navegando lo menos posible.
	Pre: recibe el grafo, el vértice de origen y el vértice de destino.
	Post: devuelve el camino (lista) y el costo de dicho camino (orden del destino).
	"""
	padre, orden = bfs(grafo, origen)
	camino = generar_camino(padre, destino)
	if not camino:
		return [], -1
	camino.reverse()
	return camino, orden[destino]

def diametro(grafo):
	"""
	Comando DIAMETRO.
	Obtiene el diámetro de toda el grafo (camino mínimo más grande). Puede haber varios,
	pero todos tienen el mismo largo.
	Pre: recibe el grafo.
	Post: devuelve el camino mínimo más grande y el diametro del mismo.
	"""
	diametro = 0
	camino = []
	vertice_diam_max = None
	padre_diam_max = {}
	for v in grafo.obtener_vertices():
		padre, orden = bfs(grafo, v)
		for w in orden:
			if orden[w] <= diametro: continue
			vertice_diam_max = w
			padre_diam_max = padre
			diametro = orden[w]
	camino = generar_camino(padre_diam_max, vertice_diam_max)
	camino.reverse()
	return camino, diametro

def rango(grafo, pagina, n):
	"""
	Comando RANGO.
	Obtiene la cantidad de vértices que se encuenten a exactamente n saltos desde 
	el vértice pasado por parámetro.
	Pre: recibe el grafo, el vértice en cuestión y n (cant. de saltos)
	Post: devuelve el numero de vértices que cumplen.
	"""
	padre, orden = bfs(grafo, pagina)
	pags_a_rango_n = 0
	for w in orden:
		if orden[w] == n:
			pags_a_rango_n += 1
	return pags_a_rango_n

def navegacion(grafo, origen):
	"""
	Comando NAVEGACION.
	Obtiene una lista con el camino hecho desde el vértice origen hasta un máximo de n vértices,
	accediendo siempre al primer adyacente de cada uno.
	Pre: recibe el grafo, el vértice de origen y n (máx. de vértices a visitar).
	Post: devuelve el camino formado.
	"""
	camino = []
	camino.append(origen)
	primer_link = list(grafo.obtener_adyacentes(origen).keys())
	for i in range(MAX_RANGO):
		if not primer_link:
			return camino 
		camino.append(primer_link[0])
		primer_link = list(grafo.obtener_adyacentes(primer_link[0]).keys())
	return camino 

def lectura(grafo, parametros):
	"""
	Comando LECTURA.
	Obtiene un orden en el que es válido leer los vértices recibidos. Para que sea válido, si v tiene 
	de adyacente a w, entonces es necesario primero visitar a w. Si hay un ciclo, no hay camino válido. 
	Pre: recibe el grafo y todos los vértices para los que se quiere obtener el
	camino indicado.
	Post: devuelve el camino formado (lista vacía si no hay camino posible).
	"""
	n_parametros = len(parametros)
	camino = []
	nuevo_grafo = Grafo()
	for v in parametros:
		nuevo_grafo.agregar_vertice(v)
		for w in grafo.obtener_adyacentes(v):
			if w in parametros:
				nuevo_grafo.agregar_vertice(w)
				nuevo_grafo.agregar_arista(v, w, 0)

	hijos, grados_salida = obtener_grados_salida(nuevo_grafo)
	
	cola = deque()
	for v in nuevo_grafo.obtener_vertices():
		if grados_salida[v] == 0:
			cola.append(v)
	while cola:
		v = cola.popleft()
		camino.append(v)
		for h in hijos:
			if v in hijos[h]:
				grados_salida[h] -= 1
				if grados_salida[h] == 0:
					cola.append(h)
		del hijos[v]
	if(n_parametros != len(camino)):
		camino = []
	return camino

def coeficiente_clustering(grafo, v):
	"""
	Calcula el coeficiente de Clustering del vértice recibido.
	Revisa si los adyacentes de v, son adyacentes entre sí.
	Además, chequea que no haya bucles (no los cuenta).
	Pre: recibe el grafo y el vértice para calcularle el coeficiente.
	Post: devuelve el coeficiente de Clustering calculado.
	"""
	adyacentes = grafo.obtener_adyacentes(v)
	grado_salida = len(adyacentes)
	clustering = 0
	if grado_salida < 2: return clustering
	for w in adyacentes:
		for x in grafo.obtener_adyacentes(w):
			if w != v and x != w and x in adyacentes:
				clustering += 1
	return clustering / (grado_salida * (grado_salida - 1))

def clustering(grafo, pagina):
	"""
	Comando CLUSTERING
	Calcula el coeficiente de Clustering, que indica qué tal agrupados se encuentran
	los vértices de un grafo. Es decir, "cuántos de mis adyacentes son adyacentes entre sí".
	Pre: recibe el grafo y la página a la que calcularle el coeficiente. Sipágina es 
	False, significa que se quiere el coeficiente de todo el grafo.
	Post: devuelve el coeficiente de Clustering calculado.
	"""
	if pagina:
		clustering = coeficiente_clustering(grafo, pagina)
		return clustering
	clustering_grafo = 0
	for v in grafo.obtener_vertices():
		clustering_grafo += coeficiente_clustering(grafo, v)
	clustering_grafo /= len(grafo.obtener_vertices())
	return clustering_grafo

def _ciclo(grafo, origen, largo, actual, camino, visitados):
	"""
	Wrapper del comando 'ciclo'.
	Intenta obtener un camino posible llamándose a sí misma y, en caso de no encontrar,
	devuelve False podando en el arbol de recursividad.
	Pre: recibe el grafo, el vertice de origen, la longitud del ciclo, el vertice actual,
	el camino posible y los vertices visitados.
	Post: devuelve si encontró un camino (True) o no (False).
	"""
	largo_camino = len(camino)
	if(largo_camino == largo):
		return actual == origen
	if(largo_camino > largo):
		return False
	if(actual in visitados):
		return False
	camino.append(actual)
	visitados[actual] = None
	for v in grafo.obtener_adyacentes(actual):
		if _ciclo(grafo, origen, largo, v, camino, visitados):
			return True
	del camino[len(camino) - 1]
	return False

def ciclo(grafo, origen, largo):
	"""
	Comando CICLO.
	Obtiene un camino de longitud n que comience en el vertice indicado, y que contenga
	como último paso ese mismo vertice, es decir un ciclo de longitud n.
	Pre: recibe el grafo, el vértice de origen y el largo del ciclo deseado.
	Post: devuelve el camino formado.
	"""
	camino = []
	visitados = {}
	if(_ciclo(grafo, origen, largo, origen, camino, visitados)):
		camino.append(origen)
	return camino