import matplotlib.pyplot as plt
import random


class WeatherEngine(object):

    def __init__(self):
        self.season = "ardent"  # another available values: breeze, harvest, chill
        self.cloudy = "clear"  # another available values: cloudy, overcast
        self.rain = False
        self.storm = False

    def get_weather(self):
        return self.cloudy, self.rain, self.storm

    def step(self):
        # Ярый
        if self.season == "ardent":
            # Далее конечный автомат из шести состояний, описанный диаграммой в документации
            if self.cloudy == "clear":
                event_probabilities = {"clear": 5000, "cloudy": 4000, "overcast": 1000}
                self.cloudy = what_happened(event_probabilities)
                return
            if self.cloudy == "cloudy":
                event_probabilities = {"clear": 5000, "overcast": 5000}
                self.cloudy = what_happened(event_probabilities)
                return
            if self.cloudy == "overcast" and not self.rain and not self.storm:
                event_probabilities = {"clear": 5000, "cloudy": 3000, "overcast storm": 1500, "overcast rain": 500}
                event = what_happened(event_probabilities)
                if event == "overcast storm":
                    self.storm = True
                    return
                if event == "overcast rain":
                    self.rain = True
                    return
                self.cloudy = event
                return
            if self.cloudy == "overcast" and not self.rain and self.storm:
                event_probabilities = {"cloudy": 8000, "storm and rain": 2000}
                event = what_happened(event_probabilities)
                if event == "storm and rain":
                    self.rain = True
                    return
                self.storm = False
                self.cloudy = event
                return
            if self.cloudy == "overcast" and self.rain and not self.storm:
                event_probabilities = {"cloudy": 5000, "storm and rain": 5000}
                event = what_happened(event_probabilities)
                if event == "storm and rain":
                    self.storm = True
                    return
                self.rain = False
                self.cloudy = event
                return
            if self.cloudy == "overcast" and self.rain and self.storm:
                self.rain = False
                self.storm = False
                self.cloudy = "cloudy"
                return


def what_happened(events_probabilities):
    random_number = random.randint(1, 10000)
    for event, probability in events_probabilities.items():
        if random_number <= probability:
            return event
        else:
            random_number -= probability


eng = WeatherEngine()
history = list()
for i in range(1000):
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
plt.pie([clear_amount, cloudy_amount, overcast_amount], labels=["Clear", "Cloudy", "Overcast"])
plt.show()
