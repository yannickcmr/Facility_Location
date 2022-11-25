import random as rd
import numpy as np
from Draw_Classes import Draw

""" Classes Algorithm """

class Demand:
    def __init__(self, pos: tuple) -> None:
        self.position = pos
        self.facility = None

class Facility:
    def __init__(self, pos: tuple, demand: Demand) -> None:
        self.position = pos
        self.service = []
        self.Add_Service(demand)

    def Add_Service(self, demand: Demand) -> None:
        self.service.append(demand)
        demand.facility = self

""" Functions """

# create a random Demand within the defined realm. 
def Randomize_Demand(area: tuple) -> Demand:
    pos_demand = [rd.randint(0, area[i]) for i in range(0, len(area))]
    return Demand(tuple(pos_demand))

# generate set_size many random Demands.
def Generate_Stream(set_size: int, area: tuple) -> list[Demand]:
    return [Randomize_Demand(area) for i in range(0, set_size)]

def Randomize_Bias_Demand(area: tuple, bias: float) -> Demand:
    center_area = tuple([np.around((area[i] / 2)) for i in range(0, len(area))])
    pos_demand = [rd.randint(np.around(center_area[i] *(1-bias) ), np.around(center_area[i] * ( 1+bias))) for i in range(0, len(center_area))]
    return Demand(tuple(pos_demand))

def Generate_Bias_Stream(set_size: int, area: tuple, bias: float = 0.5) -> list[Demand]:
    return [Randomize_Bias_Demand(area, bias) for i in range(0, set_size)]


if __name__ == "__main__":
    # testing Demand class and generator function.
    test_area = (10, 10)
    test_demand = Demand((3,4))
    test_stream = Generate_Stream(3, (test_area))

    # testing Facility class and method.
    test_facility = Facility((2,3), test_demand)
    for demand in test_stream:
        test_facility.Add_Service(demand)

    #testing Draw class and methods.
    test_draw = Draw(test_area, [test_demand, *test_stream], [test_facility])
    test_draw.Plot()
    test_draw.Save("test_save")
