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
