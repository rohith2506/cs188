import mdp, util, pdb

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
		def __init__(self, mdp, discount = 0.9, iterations = 100):
				self.mdp = mdp
				self.discount = discount
				self.iterations = iterations
				self.INF = int(10e9)
				self.values = util.Counter() # A Counter is a dict with default 0
				self.actions = dict(zip(mdp.getStates(), [None] * len(self.mdp.getStates())))

				for i in range(0, self.iterations):
					temp_values = util.Counter()
					for state in self.mdp.getStates():
						maximum_value = -self.INF
						for action in self.mdp.getPossibleActions(state):
							value = self.computeQValueFromValues(state, action)
							if value > maximum_value:
								maximum_value = value
								temp_values[state] = maximum_value
								self.actions[state] = action
					self.values = temp_values

		def getValue(self, state):
				return self.values[state]


		def computeQValueFromValues(self, state, action):
				q_value = 0
				for next_state, prob in self.mdp.getTransitionStatesAndProbs(state, action):
					reward = self.mdp.getReward(state, action, next_state)
					value = self.values[next_state]
					q_value = q_value + prob * (reward + self.discount * value)
				return q_value

		def computeActionFromValues(self, state):
				if self.mdp.isTerminal(state): return None
				return self.actions[state]

		def getPolicy(self, state):
				return self.computeActionFromValues(state)

		def getAction(self, state):
				"Returns the policy at the state (no exploration)."
				return self.computeActionFromValues(state)

		def getQValue(self, state, action):
				return self.computeQValueFromValues(state, action)
