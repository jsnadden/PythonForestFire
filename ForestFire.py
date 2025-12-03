from enum import IntEnum
from random import random
from Graph import Graph

class Status(IntEnum):
	empty = 0
	tree = 1
	burning = 2

class ForestFireModel:
	def __init__(self, graph: Graph, growthRate: float = 0.0, ignitionRate: float = 0.0):
		self.graph = graph
		self.growthRate = growthRate
		self.ignitionRate = ignitionRate
		self.state = {vertex : Status.empty for vertex in graph.vertices}

	def Step(self):
		# cache previous state
		previousState = dict(self.state)

		for vertex in self.state:
			match previousState[vertex]:
				case Status.empty:
					# spawn trees at random
					if random() < self.growthRate:
						self.state[vertex] = Status.tree

				case Status.tree:
					# fire spreads from neighbours
					for neighbour in self.graph.vertices[vertex]:
						if previousState[neighbour] == Status.burning:
							self.state[vertex] = Status.burning
					# trees can spontaneously combust
					if random() < self.ignitionRate:
						self.state[vertex] = Status.burning

				case Status.burning:
					# trees burn away
					self.state[vertex] = Status.empty

				case _:
					print(f"invalid cell status {previousState[vertex]}")
					# TODO: throw exception?





