import random as rd
import numpy as np
from Facility_Class import Facility, Demand, Draw, Generate_Stream

""" Helper Functions """

def Euclidean_Norm(point_1, point_2) -> float:
    return np.linalg.norm(np.array(point_1) - np.array(point_2))

def Find_Nearest_Facility(demand: Demand, facility_list: list):
    if len(facility_list) == 0:
        return 10000, None
    norm = [Euclidean_Norm(demand.position, facility.position) for facility in facility_list]
    min_fac = np.argmin(norm)

    return np.min(norm), facility_list[min_fac]

def Get_Minimum(distance: float, cost: float) -> float:
    relative_distance = np.around(distance/cost, decimals=3)
    return min(relative_distance, 1)

def Flip_Coin(prob: float) -> bool:
    return rd.random() < prob

""" Meyerson's Algorithm """

def Meyerson_Algorithm_Online(demand_list: list, facility_cost: int = 1):
    facilities_list = []
    for demand in demand_list:
        norm, next_facility = Find_Nearest_Facility(demand, facilities_list)
        probability_facility = Get_Minimum(norm, facility_cost)

        #if next_facility != None: print(f"{probability_facility} -- {norm} -- {demand.position} -- {next_facility.position}")
        if Flip_Coin(probability_facility):
            facilities_list.append(Facility(demand.position, demand))
        else:
            next_facility.Add_Service(demand)
    
    return facilities_list


if __name__ == "__main__":
    test_area = (100, 100)
    test_stream = Generate_Stream(35, test_area)

    test_meyerson = Meyerson_Algorithm_Online(test_stream, 100)
    result = Draw(test_area, test_stream, test_meyerson)
    result.Plot(True)
