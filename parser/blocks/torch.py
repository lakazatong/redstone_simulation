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
