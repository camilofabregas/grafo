# Implementacion del TDA Grafo
class Grafo:
	# Constructor del grafo
	def __init__(self, es_dirigido = True):
		self.vertices = {}
		self.es_dirigido = es_dirigido

	# Devuelve el diccionario de vertices
	def obtener_vertices(self):
		return dict(self.vertices)

	# Agrega un vertice al grafo
	def agregar_vertice(self, v):
		if v not in self.vertices:
			self.vertices[v] = {}

	# Conecta un vertice con otro, junto con su peso indicado
	# Si es no dirigido, se agregan mutuamente
	def agregar_arista(self, v, w, peso):
		if v not in self.vertices or w not in self.vertices:
			return
		self.vertices[v][w] = peso
		if not self.es_dirigido:
			self.vertices[w][v] = peso

	# Elimina el vertice indicado
	def borrar_vertice(self, v):
		if v not in self.vertices:
			return
		self.vertices.pop(v)
		for w in self.vertices:
			if v in self.vertices[w]:
				self.vertices[w].pop(v)

	# Elimina una conexion entre dos vertices indicados
	def borrar_arista(self, v, w):
		if v not in self.vertices or w not in self.vertices:
			return
		if w not in self.vertices[v]:
			return
		self.vertices[v].pop(w)
		if not self.es_dirigido:
			self.vertices[w].pop(v)

	# Devuelve el diccionario de adyacentes de un vertice
	def obtener_adyacentes(self, v):
		if v not in self.vertices:
			return {}
		return dict(self.vertices[v])

	# Devuelve True si el primer vertice se conecta con el segundo
	# Devuelve False en caso contrario
	def estan_conectados(self, v, w):
		if v not in self.vertices:
			return False
		return w in self.vertices[v]
