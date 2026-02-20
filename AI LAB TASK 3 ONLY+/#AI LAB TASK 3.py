#AI LAB TASK 3

class HeaterAgent:
    def __init__(self):
        self.last_action = None  # Remember previous action

    def decide(self, temp):
        if temp < 20:
            action = "Turn Heater ON"
        elif temp > 25:
            action = "Turn Heater OFF"
        else:
            action = "Do Nothing"

        # If same as last action, do nothing
        if action == self.last_action:
            action = "Do Nothing"

        self.last_action = action
        return action

# Example temperatures
temps = [18, 21, 27, 23, 19, 26]

agent = HeaterAgent()

for t in temps:
    print(f"Temperature: {t}°C -> Action: {agent.decide(t)}")
