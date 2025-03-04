class Circuit:
	def __init__(self):
		self.components = {}

	def add_component(self, component):
		self.components[component.name] = component

	def tick(self, t):
		next_states = {}
		for component in self.components.values():
			next_states[component.name] = component.tick(t)
		
		for component_name, next_state in next_states.items():
			self.components[component_name].signal = next_state

	def is_stabilized(self):
		for component in self.components.values():
			if component.has_state_changed():
				return False
		return True

	def stabilize(self):
		t = 0
		stabilization_timer = 0
		max_stabilization_time = 100

		self.tick(t)
		while stabilization_timer < max_stabilization_time:
			if self.is_stabilized():
				stabilization_timer += 1
			else:
				stabilization_timer = 0

			self.tick(t)
			t += 1

		print(f"\n{t = }")
		print(self)

	def __repr__(self):
		return "\n".join(str(component) for component in self.components.values())

class Component:
	def __init__(self, name, inputs=None, logic=None):
		self.name = name
		self.inputs = inputs if inputs else []
		self.signal = 0
		self.previous_signal = 0
		self.logic = logic

	def tick(self, t):
		self.previous_state = self.signal
		return self.logic(self.inputs, t)

	def has_state_changed(self):
		return self.signal != self.previous_state

	def __str__(self):
		return f"{self.name}: {self.signal}"

def dust(inputs, t):
	return max(i.signal for i in inputs) if len(inputs) > 0 else 0

def get_constant(strength):
	return lambda inputs, t: strength

def torch(inputs, t):
	for i in inputs:
		if i.signal > 0:
			return 0
	return 15

def get_repeater_like(redstone_ticks, get_signal_strength):
	delay = redstone_ticks * 2
	state = False
	next_state = False
	stable_time = 0

	def repeater(inputs, t):
		nonlocal delay, state, next_state, stable_time

		received_state = any(i.signal > 0 for i in inputs)

		if next_state != received_state:
			next_state = received_state
			stable_time = 0
		elif stable_time >= delay:
			state = next_state
			stable_time = 0
		else:
			stable_time += 1

		return get_signal_strength(inputs, t) if state else 0

	return repeater

def get_repeater(redstone_ticks):
	return get_repeater_like(redstone_ticks, lambda inputs, t: 15)

def get_blocked_repeater(redstone_ticks, blocked_inputs):
	delay = redstone_ticks * 2
	state = False
	next_state = False
	stable_time = 0

	def repeater(inputs, t):
		nonlocal delay, state, next_state, stable_time

		received_state = any(i.signal > 0 for i in inputs)
		is_blocked = any(i.signal > 0 for i in blocked_inputs)

		if next_state != received_state:
			next_state = received_state
			if not is_blocked:
				stable_time = 0
		elif stable_time >= delay and not is_blocked:
			state = next_state
			stable_time = 0
		elif not is_blocked:
			stable_time += 1

		if is_blocked:
			stable_time = 0

		return 15 if state else 0

	return repeater

def get_comparator(subtract_mode, side_inputs):
	def normal(inputs, t):
		rear_input = inputs[0].signal
		return 0 if any(i.signal > rear_input for i in side_inputs) else rear_input

	def subtract(inputs, t):
		return max(0, inputs[0].signal - (max(i.signal for i in side_inputs) if len(side_inputs) > 0 else 0))

	return get_repeater_like(1, subtract if subtract_mode else normal)

def pressed_stone_button(inputs, t):
	if t <= 20:
		return 15
	else:
		return 0

def pressed_wooden_button(inputs, t):
	if t <= 40:
		return 15
	else:
		return 0
