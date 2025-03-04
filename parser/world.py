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
