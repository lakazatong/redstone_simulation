from structure import parse_nbt
from parser import Parser

w = parse_nbt("examples/and_gate.nbt")
print(w)
p = Parser(w)
G = p.parse()

print(G)
