import random as rd
import numpy as np
import matplotlib.pyplot as plt

""" Classes """

class Demand:
    def __init__(self, pos: tuple) -> None:
        self.position = pos
        self.facility = None

class Facility:
    def __init__(self, pos: tuple, demand: Demand) -> None:
        self.position = pos
        self.service = [demand]

    def Add_Service(self, demand: Demand) -> None:
        self.service.append(demand)

def Split_Position(points: list):
    x_pos = [point.position[0] for point in points]
    y_pos = [point.position[1] for point in points]
    return x_pos, y_pos

class Draw:
    def __init__(self, area: tuple, demands: list, facilites: list) -> None:
        self.area = area
        self.demands = demands
        self.facilities = facilites
    
    def Plot(self, show_rel: bool = False):
        # Preparing the plot.
        figure, axes = plt.subplots()
        plt.title(f"Facility Location\nArea:{self.area}\nDemand:{len(self.demands)} - Facilities: {len(self.facilities)}")
        plt.grid(True, which="both")
        axes.set_aspect("equal")

        plt.xlim([0, self.area[0]])
        plt.ylim([0, self.area[1]])

        plt.axhline(linewidth=1, color="black")
        plt.axvline(linewidth=1, color="black")

        # get data points to plot.
        x_demand, y_demand = Split_Position(self.demands)
        x_facilities, y_facilities = Split_Position(self.facilities)

        # demand will be shown as black dots, facilities as red stars
        plt.scatter(x_demand, y_demand , color="black", s=50, zorder=2)
        plt.scatter(x_facilities, y_facilities , color="red", s=25, marker="*", zorder=2)

        if show_rel:
            pass

        plt.show()

""" Functions """

def Randomize_Demand(area: tuple) -> Demand:
    pos_demand = [rd.randint(0, area[i]) for i in range(0, len(area))]
    return Demand(tuple(pos_demand))

def Generate_Stream(set_size: int, area: tuple) -> list:
    return [Randomize_Demand(area) for i in range(0, set_size)]

if __name__ == "__main__":
    test_demand_1 = Demand((3,4))
    test_demand_2 = Demand((1,3))

    test_facility = Facility((2,3), test_demand_1)
    test_facility.Add_Service(test_demand_2)

    print(len(test_facility.service))

    test_draw = Draw((5,5), [test_demand_1, test_demand_2], [test_facility])
    test_draw.Plot()
