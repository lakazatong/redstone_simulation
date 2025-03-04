from sim import *

circuit = Circuit()

B1 = Component('B1', logic=get_constant(0))

R1 = Component('R1', inputs=[B1], logic=get_repeater(4))

T1 = Component('T1', inputs=[B1], logic=torch)
T2 = Component('T2', inputs=[R1], logic=torch)

R2 = Component('R2', inputs=[T1, T2], logic=get_repeater(1))

R7 = Component('R7', inputs=[R2], logic=get_repeater(1))
R8 = Component('R8', inputs=[R2], logic=get_repeater(1))
R9 = Component('R9', inputs=[R2], logic=get_repeater(1))
R10 = Component('R10', inputs=[R2], logic=get_repeater(1))

R6 = Component('R6')

R3 = Component('R3', inputs=[R6], logic=get_blocked_repeater(4, [R7]))
R4 = Component('R4', inputs=[R3], logic=get_blocked_repeater(4, [R8]))
R5 = Component('R5', inputs=[R4], logic=get_blocked_repeater(4, [R9]))
R6.inputs = [R5]
R6.logic = get_blocked_repeater(4, [R10])

circuit.add_component(B1)
circuit.add_component(R1)
circuit.add_component(T1)
circuit.add_component(T2)
circuit.add_component(R2)
circuit.add_component(R7)
circuit.add_component(R8)
circuit.add_component(R9)
circuit.add_component(R10)
circuit.add_component(R3)
circuit.add_component(R4)
circuit.add_component(R5)
circuit.add_component(R6)

circuit.stabilize()

B1.logic = pressed_stone_button
R3.inputs.append(R1)

circuit.stabilize()

R3.inputs.pop()

circuit.stabilize()
circuit.stabilize()
circuit.stabilize()
circuit.stabilize()
