class BlockType(Enum):
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
