import matplotlib.pyplot as plt
import random
import logging


class WeatherEngine(object):

    def __init__(self):
        self.season = "ardent"  # breeze, harvest, chill
        self.cloudy = "clear"  # cloudy, overcast
        self.rain = False
        self.storm = False
        self.state = "clear" # "cloudy [rain, storm, both]"

    def get_weather(self):
        return self.cloudy, self.rain, self.storm

    def set_weather(self, cloudy_value, rain_value, storm_value):
        self.cloudy = cloudy_value
        self.rain = rain_value
        self.storm = storm_value

    def set_state(self, state):
        logging.info(state)
        self.state = state

        states = state.split(" ")

        logging.info(states[0])
        self.cloudy = states[0]

        if len(states) == 1:
            self.rain = False
            self.storm = False
        else:
            logging.info(states[1])
            if states[1] == "rain":
                self.rain = True
                self.storm = False
            elif states[1] == "storm":
                self.rain = False
                self.storm = True
            elif states[1] == "both":
                self.rain = True
                self.storm = True

    def step(self):
        # Ярый
        if self.season == "ardent":
            # Далее конечный автомат из шести состояний
            if self.state == "clear":
                state_probabilities = {"clear":  7000, "cloudy": 3000}
            elif self.state == "cloudy":
                state_probabilities = {"clear": 6000, "overcast": 4000}
            elif self.state == "overcast":
                state_probabilities = {"clear": 3500, "cloudy": 1500, "overcast storm": 3000, "overcast rain": 2000}
            elif self.state == "overcast storm":
                state_probabilities = {"cloudy": 5000, "overcast both": 5000}
            elif self.state == "overcast rain":
                state_probabilities = {"cloudy": 5000, "overcast both": 5000}
            elif self.state == "overcast both":
                state_probabilities = {"cloudy": 10000}
            else:
                return
            self.set_state(what_happened(state_probabilities))


def what_happened(events_probabilities):
    random_number = random.randint(1, 10000)
    for event, probability in events_probabilities.items():
        if random_number <= probability:
            return event
        else:
            random_number -= probability


logging.basicConfig(filename="test.log", level=logging.INFO, datefmt="%m.%d.%y - %H:%M:%S",
                    format="%(levelname)-7s - %(module)-15s - %(asctime)s - %(message)s")

eng = WeatherEngine()
history = list()
for i in range(24):
    print(eng.get_weather())
    history.append(eng.get_weather())
    eng.step()

cloudy_l = list()
cloudy_amount = 0
clear_amount = 0
overcast_amount = 0
rain_l = list()
storm_l = list()

for cloudy, rain, storm in history:
    if cloudy == "clear":
        cloudy_l.append(cloudy)
        clear_amount += 1
    elif cloudy == "cloudy":
        cloudy_l.append(cloudy)
        cloudy_amount += 1
    else:
        cloudy_l.append(cloudy)
        overcast_amount += 1
    if rain:
        rain_l.append("cloudy")
    else:
        rain_l.append("clear")
    if storm:
        storm_l.append("cloudy")
    else:
        storm_l.append("clear")

plt.plot(cloudy_l)
plt.plot(rain_l)
plt.plot(storm_l)
plt.show()
# plt.pie([clear_amount, cloudy_amount, overcast_amount], labels=["Clear", "Cloudy", "Overcast"])
# plt.show()
