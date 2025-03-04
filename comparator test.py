from sim import *

circuit = Circuit()

ports = []
for i in range(16):
	P = Component(f'P{i}', logic=get_constant(i))
	ports.append(P)
	circuit.add_component(P)

rear_inputs = []
side_inputs = []
C1 = Component('C1', inputs=rear_inputs, logic=get_comparator(False, side_inputs))

circuit.add_component(C1)

circuit.stabilize()

C1.inputs = [ports[5]]

circuit.stabilize()

C1.logic = get_comparator(False, [ports[6]])

circuit.stabilize()

C1.inputs = [ports[13]]
C1.logic = get_comparator(True, [ports[12]])

circuit.stabilize()
