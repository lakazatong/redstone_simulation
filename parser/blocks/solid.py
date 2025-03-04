from block import BlockType, Block

class Solid(Block):
	def __init__(self, coords: "Vec3", world: "World"):
		super().__init__(BlockType.SOLID, coords, world)

	def is_input_of(self, neighbor: "Block"):
		match neighbor.type:
			case BlockType.DUST:
				return True
			case BlockType.REPEATER | BlockType.COMPARATOR:
				return neighbor.is_facing_away(self)
			case BlockType.TORCH:
				return (neighbor.is_above(self) and not neighbor.is_on_wall()) or neighbor.is_on_wall_of(self)
		return False

	def is_output_of(self, neighbor: "Block"):
		match neighbor.type:
			case BlockType.DUST:
				return neighbor.is_facing(self)
			case BlockType.REPEATER | BlockType.COMPARATOR:
				return neighbor.is_facing(self)
			case BlockType.TORCH:
				return neighbor.is_below(self)
		return False
