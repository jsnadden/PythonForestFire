

class Graph:
	def __init__(self, vertices: list = [], edges: list[tuple] = []):
		# start with empty graph
		self.vertices = {}

		# add supplied vertices
		for v in vertices:
			self.vertices[v] = set()
		
		for e in edges:
			# handle invalid data
			if len(e) != 2:
				print("provided edge list contains an invalid element (not a pair)")
				print("defaulting to empty graph")
				self.vertices = {}
				return
			
			# add adjacencies
			self.vertices[e[0]].add(e[1])
			self.vertices[e[1]].add(e[0])

	def Adjacent(self, vertex0, vertex1):
		# if the supplied vertices actually belong to the graph, check adjacency
		if vertex0 in self.vertices and vertex1 in self.vertices:
			return vertex1 in self.vertices[vertex0]

		# otherwise
		return False

	def AddVertex(self, vertex):
		# early exit if already present
		if vertex in self.vertices:
			return

		# otherwise add it
		self.vertices[vertex] = {}

	def RemoveVertex(self, vertex):
		# remove this vertex, if present
		self.vertices.remove[vertex]

		# now remove any attached edges
		for v in self.vertices:
			self.vertices[v].remove(vertex)

	def AddEdge(self, vertex0, vertex1):
		# add one endpoint
		if vertex0 in self.vertices:
			self.vertices[vertex0].add(vertex1)
		else:
			self.vertices[vertex0] = {vertex1}

		# add the other endpoint
		if vertex1 in self.vertices:
			self.vertices[vertex1].add(vertex0)
		else:
			self.vertices[vertex1] = {vertex0}

	def RemoveEdge(self, vertex0, vertex1):
		# simple: remove adjacency if present
		self.vertices[vertex0].remove(vertex1)
		self.vertices[vertex1].remove(vertex0)

class Grid(Graph):
	def __init__(self, width: int, height: int):
		# TODO: check width and height positive
		
		# grid points
		vertices = [(x,y) for x in range(width) for y in range(height)]
		# horizontal edges
		edges = [((x,y),(x+1,y)) for x in range(width-1) for y in range(height)]
		# vertical edges
		edges += [((x,y),(x,y+1)) for x in range(width) for y in range(height-1)]

		Graph.__init__(self, vertices, edges)