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
		return other != None and self.x == other.x and self.y == other.y and self.z == other.z

	def __add__(self, other):
		return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
	
	def __sub__(self, other):
		return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

	def __str__(self):
		return f"{self.x}, {self.y}, {self.z}"

	def __repr__(self):
		return "(" + self.__str__() + ")"
	
	def __hash__(self):
		return hash((self.x, self.y, self.z))
	
	@staticmethod
	def from_cardinal(cardinal: str):
		match cardinal:
			case "east": return Vec3(1, 0, 0)
			case "west": return Vec3(-1, 0, 0)
			case "south": return Vec3(0, 0, 1)
			case "north": return Vec3(0, 0, -1)
			case "up": return Vec3(0, 1, 0)
			case "down": return Vec3(0, -1, 0)
		return None

class World:
	def __init__(self):
		self.blocks = []

	def get_neighbors(self, block):
		r = []
		for coord in block.coords.neighbors():
			if coord.x < len(self.blocks):
				tmp1 = self.blocks[coord.x]
				if coord.y < len(tmp1):
					tmp2 = tmp1[coord.y]
					if coord.z < len(tmp2) and (b := tmp2[coord.z]) != None:
						r.append(b)
		return r

	def set_block(self, block):
		coords = block.coords
		while len(self.blocks) <= coords.x:
			self.blocks.append([])
		while len(self.blocks[coords.x]) <= coords.y:
			self.blocks[coords.x].append([])
		while len(self.blocks[coords.x][coords.y]) <= coords.z:
			self.blocks[coords.x][coords.y].append(None)

		self.blocks[coords.x][coords.y][coords.z] = block

	def __str__(self):
		if not self.blocks:
			return "Empty world"

		max_x = len(self.blocks)
		max_y = max(len(self.blocks[x]) for x in range(max_x)) if max_x > 0 else 0
		max_z = max(len(self.blocks[x][y]) for x in range(max_x) for y in range(len(self.blocks[x]))) if max_y > 0 else 0

		output = []
		for y in range(max_y):
			output.append(f"Y-Level {y}:")
			for x in range(max_x):
				row = []
				for z in range(max_z):
					if x < len(self.blocks) and y < len(self.blocks[x]) and z < len(self.blocks[x][y]):
						block = self.blocks[x][y][z]
						row.append(str(block.type.value) if block else "0")
					else:
						row.append("0")
				output.append(" ".join(row))
			output.append("")

		return "\n".join(output)

	def get_first_block(self):
		for x in range(len(self.blocks)):
			if not self.blocks[x]:
				continue
			for y in range(len(self.blocks[x])):
				if not self.blocks[x][y]:
					continue
				for z in range(len(self.blocks[x][y])):
					block = self.blocks[x][y][z] if z < len(self.blocks[x][y]) else None
					if block:
						return block
		return None
