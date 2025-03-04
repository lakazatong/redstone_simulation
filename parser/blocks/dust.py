from block import BlockType, Block

class Dust(Block):
	def __init__(self, coords: "Vec3", world: "World"):
		super().__init__(BlockType.DUST, coords, world)

	def is_input_of(self, neighbor: "Block"):
		match neighbor.type:
			case BlockType.SOLID:
				return self.is_facing(neighbor)
			case BlockType.DUST:
				return True
			case BlockType.REPEATER | BlockType.COMPARATOR:
				return neighbor.is_facing_away(self)
		return False

	def is_output_of(self, neighbor: "Block"):
		match neighbor.type:
			case BlockType.SOLID | BlockType.DUST | BlockType.TORCH:
				return True
			case BlockType.REPEATER | BlockType.COMPARATOR:
				return neighbor.is_facing(self)
		return False
