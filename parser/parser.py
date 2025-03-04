from collections import deque
from functools import partial

class Parser:
	def __init__(self, world: "World"):
		self.world = world
		self.graph = {}

	def parse(self):
		queue = deque([self.world.get_first_block()])
		visited = set()

		while queue:
			block = queue.popleft()

			if block.uuid in visited:
				continue
			visited.add(block.uuid)

			block_inputs, block_outputs = [], []
			for neighbor in self.world.get_neighbors(block):
				if neighbor.is_input_of(block): block_inputs.append(neighbor)
				if neighbor.is_output_of(block): block_outputs.append(neighbor)
				queue.append(neighbor)

			self.graph[block.uuid] = {"block": block, "inputs": block_inputs, "outputs": block_outputs}

		return self.graph
