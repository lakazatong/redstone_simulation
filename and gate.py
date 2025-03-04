from sim import *

circuit = Circuit()

P1 = Component('P1', logic=get_constant(7))
P2 = Component('P2', logic=get_constant(8))

T1 = Component('T1', inputs=[P1], logic=torch)
T2 = Component('T2', inputs=[P2], logic=torch)
T3 = Component('T3', inputs=[T1, T2], logic=torch)
P3 = Component('P3', inputs=[T3], logic=dust)

circuit.add_component(P1)
circuit.add_component(P2)
circuit.add_component(T1)
circuit.add_component(T2)
circuit.add_component(T3)
circuit.add_component(P3)

circuit.stabilize()

P1.logic = get_constant(0)
circuit.stabilize()

P2.logic = get_constant(0)
circuit.stabilize()

P1.logic = get_constant(15)
P2.logic = get_constant(3)
circuit.stabilize()