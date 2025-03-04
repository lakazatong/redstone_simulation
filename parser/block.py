from enum import Enum

class BlockType(Enum):
	AIR = 0
	SOLID = 1
	DUST = 2
	REPEATER = 3
	TORCH = 4
	COMPARATOR = 5

class Block:
	def __init__(self, type: "BlockType", coords: "Vec3", world: "World"):
		self.type = type
		self.coords = coords
		self.world = world
		self.props = {}

	def __str__(self):
		return f"{self.type}, ({self.coords})"

	def with_props(self, props):
		self.props = props
		return self

	def is_above(self, other):
		return self.coords.y > other.coords.y

	def is_below(self, other):
		return self.coords.y < other.coords.y

	def is_on_wall(self):
		return self.props.get("on_wall", False) == True

	def is_on_wall_of(self, other):
		# this is not strictly checking if it's on the wall of other but rather if it could
		# it would then be if self is a neighbor of other
		return self.is_on_wall() and self.is_facing_away(other)

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
