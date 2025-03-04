from functools import partial
from enum import Enum

class Vec3:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def above(self):
		return Vec3(self.x, self.y + 1, self.z)

	def below(self):
		return Vec3(self.x, self.y - 1, self.z)

	def around(self):
		return [
			Vec3(self.x + 1, self.y, self.z),
			Vec3(self.x - 1, self.y, self.z),
			Vec3(self.x, self.y, self.z + 1),
			Vec3(self.x, self.y, self.z - 1)
		]

	def neighbors(self):
		r = self.around()
		r.append(self.above())
		r.append(self.below())
		return r

	def opposite(self):
		return Vec3(-self.x, -self.y, -self.z)

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y and self.z == other.z

	def __add__(self, other):
		return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
	
	def __sub__(self, other):
		return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

class BlockType(Enum):
    SOLID = 1
    DUST = 2
    REPEATER = 3
    TORCH = 4
    COMPARATOR = 5

class World:
	def __init__(self):
		self.blocks = []

	def get_neighbors(self, block):
		r = []
		for coord in block.props["coords"].neighbors():
			if coord.x < len(self.blocks):
				tmp1 = self.blocks[coord.x]
				if coord.y < len(tmp1):
					tmp2 = tmp1[coord.y]
					if coord.z < len(tmp2):
						r.append(tmp2[coord.z])
		return r

class Block:
	def __init__(self, type: "BlockType", coords: "Vec3", world: "World"):
		self.type = type
		self.coords = coords
		self.world = world
		self.props = {}

	def is_above(self, other):
		self.coords.x == other.coords.x and self.coords.y + 1 == other.coords.y and self.coords.z == other.coords.z

	def is_below(self, other):
		self.coords.x == other.coords.x and self.coords.y - 1 == other.coords.y and self.coords.z == other.coords.z

	def is_on_wall(self):
		return self.props.get("on_wall", None) == True

	def is_on_wall_of(self, other):
		wall_coords = self.props.get("on_wall_of", None)
		return wall_coords != None and wall_coords == other.coords

	def is_facing(self, other):
		facings = self.props.get("facings", None)
		if facings == None:
			return False
		for facing in facings:
			if self.coords + facing == other.coords:
				return True
		return False

	def is_facing_away(self, other):
		facings = self.props.get("facings", None)
		if facings == None:
			return False
		for facing in facings:
			if self.coords - facing == other.coords:
				return True
		return False

	def is_input_of(self, neighbor: "Block"):
		pass
	
	def is_output_of(self, neighbor: "Block"):
		pass

class SolidBlock(Block):
	def __init__(self, coords: "Vec3", world: "World"):
		super(BlockType.SOLID, coords, world)

	def is_input_of(self, neighbor: "Block"):
		match neighbor.type:
			case BlockType.DUST:
				return True
			case BlockType.REPEATER:
			case BlockType.COMPARATOR:
				return neighbor.is_facing_away(self)
			case BlockType.TORCH:
				return (neighbor.is_above(self) and not neighbor.is_on_wall()) or neighbor.is_on_wall_of(self)
		return False

	def is_output_of(self, neighbor: "Block"):
		match neighbor.type:
			case BlockType.DUST:
				return neighbor.is_facing(self)
			case BlockType.REPEATER:
			case BlockType.COMPARATOR:
				return neighbor.is_facing(self)
			case BlockType.TORCH:
				return neighbor.is_below(self)
		return False

class DustBlock(Block):
	def __init__(self, coords: "Vec3", world: "World"):
		super(BlockType.DUST, coords, world)

	def is_input_of(self, neighbor: "Block"):
		match neighbor.type:
			case BlockType.SOLID:
				return self.is_facing(neighbor)
			case BlockType.DUST:
				return True
			case BlockType.REPEATER:
			case BlockType.COMPARATOR:
				return neighbor.is_facing_away(self)
		return False

	def is_output_of(self, neighbor: "Block"):
		match neighbor.type:
			case BlockType.SOLID:
			case BlockType.DUST:
			case BlockType.TORCH:
				return True
			case BlockType.REPEATER:
			case BlockType.COMPARATOR:
				return neighbor.is_facing(self)
		return False

class RepeaterBlock(Block):
	def __init__(self, coords: "Vec3", world: "World"):
		super(BlockType.REPEATER, coords, world)

	def is_input_of(self, neighbor: "Block"):
		match neighbor.type:
			case BlockType.SOLID:
			case BlockType.DUST:
				return self.is_facing(neighbor)
			case BlockType.REPEATER:
			case BlockType.COMPARATOR:
				return self.is_facing(neighbor) and not neighbor.is_facing(self)
		return False

	def is_output_of(self, neighbor: "Block"):
		match neighbor.type:
			case BlockType.SOLID:
			case BlockType.DUST:
			case BlockType.TORCH:
				return self.is_facing_away(neighbor)
			case BlockType.REPEATER:
			case BlockType.COMPARATOR:
				return self.is_facing_away(neighbor) and neighbor.is_facing(self)
		return False

class TorchBlock(Block):
	def __init__(self, coords: "Vec3", world: "World"):
		super(BlockType.TORCH, coords, world)

	def is_input_of(self, neighbor: "Block"):
		match neighbor.type:
			case BlockType.SOLID:
				return neighbor.is_above(self)
			case BlockType.DUST:
				return True
			case BlockType.REPEATER:
			case BlockType.COMPARATOR:
				return neighbor.is_facing_away(self)
		return False

	def is_output_of(self, neighbor: "Block"):
		match neighbor.type:
			case BlockType.SOLID:
				return (self.is_above(neighbor) and not self.is_on_wall()) or self.is_on_wall_of(neighbor)
		return False

class ComparatorBlock(Block):
	def __init__(self, coords: "Vec3", world: "World"):
		super(BlockType.COMPARATOR, coords, world)

	def is_input_of(self, neighbor: "Block"):
		match neighbor.type:
			case BlockType.SOLID:
			case BlockType.DUST:
				return self.is_facing(neighbor)
			case BlockType.REPEATER:
			case BlockType.COMPARATOR:
				return self.is_facing(neighbor) and not neighbor.is_facing(self)
		return False

	def is_output_of(self, neighbor: "Block"):
		match neighbor.type:
			case BlockType.SOLID:
			case BlockType.TORCH:
				return self.is_facing_away(neighbor)
			case BlockType.DUST:
			case BlockType.REPEATER:
			case BlockType.COMPARATOR:
				return not self.is_facing(neighbor)
		return False

class RedstoneParser:
	def __init__(self, world: "World"):
		self.world = world
		self.graph = {}  # Maps UUIDs to blocks and their connections

	def add_input(self, block, neighbor):
		self.graph[block.uuid]["inputs"].append(neighbor.uuid)
	
	def add_output(self, block, neighbor):
		self.graph[block.uuid]["outputs"].append(neighbor.uuid)

	def get_add_input(self, block):
		return partial(self.add_input, block)

	def get_add_output(self, block):
		return partial(self.add_output, block)

	def get_both(self, block):
		return self.get_add_input(block), self.get_add_output(block)

	def parse(self, start_block: "Block"):
		queue = deque([start_block])
		visited = set()

		while queue:
			block = queue.popleft()

			if block.uuid in visited:
				continue
			visited.add(block.uuid)

			if block.type in handlers:
				block_inputs, block_outputs = [], []
				for neighbor in self.world.get_neighbors(block):
					if neighbor.is_input_of(block): block_inputs.append(neighbor)
					if neighbor.is_output_of(block): block_outputs.append(neighbor)
				self.graph[block.uuid] = {"block": block, "inputs": block_inputs, "outputs": block_outputs}

		return self.graph
