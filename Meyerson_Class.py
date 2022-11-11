import numpy as np
import os
from Facility_Class import Facility, Demand, Draw, Generate_Stream
from Meyerson_Algorithm import q_Get_Probability, Find_Nearest_Facility, Flip_Coin

class Meyerson:
    def __init__(self, area: tuple = (10, 10), cost: int = 5, q: float = 0.5) -> None:
        self.area = area
        self.q_value = q
        self.faclility_cost = cost
        self.total_cost = 0
        self.demands = []
        self.facilities = []

    def Add_Demand(self, demand: Demand):
        self.demands.append(demand)

        norm, next_facility = Find_Nearest_Facility(demand, self.facilities)
        probability = q_Get_Probability(self.q_value, norm, self.faclility_cost)

        if Flip_Coin(probability):
            self.facilities.append(Facility(demand.position, demand))
            self.total_cost = np.around(self.total_cost + self.faclility_cost, decimals= 3) 
        else:
            next_facility.Add_Service(demand)
            self.total_cost = np.around(self.total_cost + norm, decimals= 3) 



if __name__ == "__main__":
    save_path = "Test_Meyerson/"
    test_area = (25, 25)
    test_facility_cost = 20
    test_q = 1
    test_demand_size = 15

    input_stream = Generate_Stream(test_demand_size, test_area)
    test_meyerson = Meyerson(test_area, test_facility_cost, test_q)

    for i, demand in enumerate(input_stream):
        save_name = os.path.join(save_path, f"meyerson_img_{i}.png")
        test_meyerson.Add_Demand(demand)
        #Draw(test_area, test_meyerson.demands, test_meyerson.facilities, test_meyerson.total_cost).Plot(True, save_name)