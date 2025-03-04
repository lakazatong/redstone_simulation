from block import BlockType, Block

class Comparator(Block):
	def __init__(self, coords: "Vec3", world: "World"):
		super().__init__(BlockType.COMPARATOR, coords, world)

	def is_input_of(self, neighbor: "Block"):
		match neighbor.type:
			case BlockType.SOLI | BlockType.DUST:
				return self.is_facing(neighbor)
			case BlockType.REPEATER | BlockType.COMPARATOR:
				return self.is_facing(neighbor) and not neighbor.is_facing(self)
		return False

	def is_output_of(self, neighbor: "Block"):
		match neighbor.type:
			case BlockType.SOLID | BlockType.TORCH:
				return self.is_facing_away(neighbor)
			case BlockType.DUST | BlockType.REPEATER | BlockType.COMPARATOR:
				return not self.is_facing(neighbor)
		return False
