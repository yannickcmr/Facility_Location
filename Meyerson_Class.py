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

    def Add_Demand(self, demand: Demand) -> None:
        self.demands.append(demand)

        norm, next_facility = Find_Nearest_Facility(demand, self.facilities)
        probability = q_Get_Probability(self.q_value, norm, self.faclility_cost)

        if Flip_Coin(probability):
            self.facilities.append(Facility(demand.position, demand))
            self.total_cost = np.around(self.total_cost + self.faclility_cost, decimals= 3) 
        else:
            next_facility.Add_Service(demand)
            self.total_cost = np.around(self.total_cost + norm, decimals= 3) 

def Create_Slide_Show(meyerson: Meyerson, demand_list: list, file_name: str = "test_slide_show") -> None:
    for i, demand in enumerate(demand_list):
        save_name = f"{file_name}_{i}"
        meyerson.Add_Demand(demand)
        Draw(meyerson.area, meyerson.demands, meyerson.facilities, meyerson.total_cost).Save(save_name)



if __name__ == "__main__":
    save_path = "Test_Meyerson/"
    test_area = (25, 25)
    test_facility_cost = 35
    test_q = 1
    test_demand_size = 15

    input_stream = Generate_Stream(test_demand_size, test_area)
    test_meyerson = Meyerson(test_area, test_facility_cost, test_q)

    Create_Slide_Show(test_meyerson, input_stream)