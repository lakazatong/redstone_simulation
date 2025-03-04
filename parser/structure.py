from nbt import nbt

from world import World, Vec3
from block import BlockType
from blocks.comparator import Comparator
from blocks.dust import Dust
from blocks.repeater import Repeater
from blocks.solid import Solid
from blocks.torch import Torch

# for t in nbtfile["palette"]:
# 	print(t["Name"])
# 	if "Properties" in t:
# 		for k,v in t["Properties"].items():
# 			print("\t", k, v)

def convert_palette(palette):
	r = []
	for t in palette:
	
		props = { "facings": [] }
		builder = lambda coords, w: Solid(coords, w).with_props(props)
		match t["Name"].value:
			case "minecraft:air":
				r.append(None)
				continue
			case "minecraft:redstone_wire":
				builder = lambda coords, w: Dust(coords, w).with_props(props)
			case "minecraft:redstone_torch":
				builder = lambda coords, w: Torch(coords, w).with_props(props)
			case "minecraft:redstone_wall_torch":
				props["on_wall"] = True
				builder = lambda coords, w: Torch(coords, w).with_props(props)
			case _:
				...
				# print(t["Name"])

		if "Properties" in t:
			for k, tmp in t["Properties"].items():
				v = tmp.value

				if k == "facing":
					props["facings"].append(Vec3.from_cardinal(v))
				
				elif (tmp := Vec3.from_cardinal(k)) != None and v == "side":
					props["facings"].append(tmp)

				elif k == "lit":
					props[k] = bool(v)

				elif k == "power":
					props[k] = int(v)

				else:
					...
					# print(t)
					# print("\t", k, v)

		r.append(builder)
	
	return r

def parse_nbt(path):
	nbtfile = nbt.NBTFile(path, "rb")
	blocks = nbtfile["blocks"]
	palette = convert_palette(nbtfile["palette"])

	w = World()

	for b_tag in blocks:
		pos = b_tag["pos"]
		builder = palette[b_tag["state"].value]
		if builder == None:
			continue

		b = builder(Vec3(pos[0].value, pos[1].value, pos[2].value), w)
		w.set_block(b)

	return w
