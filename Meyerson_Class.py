import numpy as np
import os
from Facility_Class import Facility, Demand, Generate_Stream, Generate_Bias_Stream
from Meyerson_Algorithm import *
from Draw_Classes import Draw, Draw_Map

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

def Create_Basic_Slides(meyerson: Meyerson, demand_list: list, file_name: str = "test_slide_show") -> None:
    for i, demand in enumerate(demand_list):
        save_name = f"{file_name}_{i}"
        meyerson.Add_Demand(demand)
        Draw(meyerson.area, meyerson.demands, meyerson.facilities, meyerson.total_cost).Save(save_name)

def Create_BG_Slides(meyerson: Meyerson, demand_list: list, img_name: str) -> None:
    save_name = f"{img_name.replace('.png', '') }_BG_Slides"
    for i, demand in enumerate(demand_list):
        meyerson.Add_Demand(demand)
        Draw_Map(meyerson.area, meyerson.demands, meyerson.facilities, img_name, meyerson.total_cost).Save(f"{save_name}_{i}")


if __name__ == "__main__":
    save_path = "Test_Meyerson/"
    test_area = (45, 38)
    test_facility_cost = 25
    test_q = 1
    test_demand_size = 21
    test_bias = 0.6
    test_img = "berlin.png"
    test_img = "deutschland.png"

    #input_stream = Generate_Stream(test_demand_size, test_area)
    #input_stream_bias = Generate_Bias_Stream(test_demand_size, test_area, test_bias)
    #test_meyerson = Meyerson(test_area, test_facility_cost, test_q)

    #Create_Basic_Slides(test_meyerson, input_stream)
    #Create_BG_Slides(test_meyerson, input_stream_bias, test_img)