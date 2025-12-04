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
		self.state = [{vertex : Status.empty for vertex in graph.vertices} for _ in range(2)]
		self.bufferIndex = 0
		self.treeCount = 0

	def CurrentState(self):
		return self.state[self.bufferIndex]

	def TreeCount(self):
		return self.treeCount

	def Step(self):
		# swap state buffers
		previousState = self.state[self.bufferIndex]
		self.bufferIndex = (self.bufferIndex + 1) % 2
		nextState = self.state[self.bufferIndex]

		for vertex in nextState:
			match previousState[vertex]:
				case Status.empty:
					# spawn trees at random
					if random() < self.growthRate:
						nextState[vertex] = Status.tree
						self.treeCount += 1
					else:
						nextState[vertex] = Status.empty

				case Status.tree:
					ignite = False

					# fire spreads from neighbours
					for neighbour in self.graph.vertices[vertex]:
						ignite |= previousState[neighbour] == Status.burning

					# trees can spontaneously combust
					ignite |= random() < self.ignitionRate

					nextState[vertex] = Status.burning if ignite else Status.tree

				case Status.burning:
					# trees burn away
					nextState[vertex] = Status.empty
					self.treeCount -= 1

				case _:
					print(f"invalid cell status {previousState[vertex]}")
					# TODO: throw exception?





