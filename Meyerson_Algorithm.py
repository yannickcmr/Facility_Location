import random as rd
import numpy as np
from Facility_Class import Facility, Demand, Draw, Generate_Stream

""" Helper Functions """

# calculates the distance (ordinary norm) of two points and rounds it to 4 decimal places.
def Euclidean_Norm(point_1, point_2) -> float:
    return np.around(np.linalg.norm(np.array(point_1) - np.array(point_2)), decimals=4)

# find the closest facility based on the norm. returns the distance and the facility.
def Find_Nearest_Facility(demand: Demand, facility_list: list):
    # base case if facility_list is still empty (1. iteration). 
    if len(facility_list) == 0:
        return 10000, None
    
    norm = [Euclidean_Norm(demand.position, facility.position) for facility in facility_list]
    return np.min(norm), facility_list[np.argmin(norm)]

# calculates the relative distance based on the cost of opening a new facility.
def Get_Probability(distance: float, cost: int) -> float:
    relative_distance = np.around(distance/cost, decimals=3)
    return min(relative_distance, 1)

def q_Get_Probability(q, distance: float, cost: int):
    relative_distance = np.around(distance/cost, decimals=3)
    relative_distance = q*relative_distance
    return min(relative_distance, 1)

def Flip_Coin(prob: float) -> bool:
    return rd.random() < prob


""" Meyerson's Algorithm """

def Meyerson_Algorithm_Online(demand_list: list, facility_cost: int = 1):
    facilities_list = []
    for demand in demand_list:
        # calculate the relevent values
        norm, next_facility = Find_Nearest_Facility(demand, facilities_list)
        probability_facility = Get_Probability(norm, facility_cost)

        #if next_facility != None: print(f"{probability_facility} -- {norm} -- {demand.position} -- {next_facility.position}")
        if Flip_Coin(probability_facility):
            # opens up a new facility.
            facilities_list.append(Facility(demand.position, demand))
        else:
            # uses already existing facility.
            next_facility.Add_Service(demand)
    
    return facilities_list


def q_Meyerson_Algorithm_Online(q: float, demand_list: list, facility_cost: int = 1):
    facilities_list = []
    for demand in demand_list:
        # calculate the relevent values
        norm, next_facility = Find_Nearest_Facility(demand, facilities_list)
        probability_facility = q_Get_Probability(q, norm, facility_cost)

        #if next_facility != None: print(f"{probability_facility} -- {norm} -- {demand.position} -- {next_facility.position}")
        if Flip_Coin(probability_facility):
            # opens up a new facility.
            facilities_list.append(Facility(demand.position, demand))
        else:
            # uses already existing facility.
            next_facility.Add_Service(demand)
    
    return facilities_list


""" Cost Function """

def Calculate_Costs(facilities: list, facility_cost: int) -> float:
    total_cost = 0
    for facility in facilities:
        total_cost += facility_cost
        for demand in facility.service:
            total_cost += Euclidean_Norm(facility.position, demand.position)
    
    return np.around(total_cost, decimals=2)


if __name__ == "__main__":
    test_area = (100, 20)
    test_stream = Generate_Stream(35, test_area)

    test_meyerson = Meyerson_Algorithm_Online(test_stream, 30)
    test_cost = Calculate_Costs(test_meyerson, 30)
    result = Draw(test_area, test_stream, test_meyerson, test_cost)
    result.Plot(True)

    test_q_meyerson = q_Meyerson_Algorithm_Online(0.5, test_stream, 30)
    test_q_cost = Calculate_Costs(test_q_meyerson, 30)
    q_result = Draw(test_area, test_stream, test_q_meyerson, test_q_cost)
    q_result.Plot(True)
