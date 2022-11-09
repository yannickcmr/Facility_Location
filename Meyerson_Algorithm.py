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
# Calculates formula: |F|*f + \sum d(F, u)
# where F: facilities, f: opening costs, d(F,u): distance from demand to the closest facility.
def Calculate_Costs(facilities: list, facility_cost: int) -> float:
    total_cost = 0
    for facility in facilities:
        total_cost += facility_cost

        for demand in facility.service:
            total_cost += Euclidean_Norm(facility.position, demand.position)
    
    return np.around(total_cost, decimals=2)


""" Test Function """

def Sample_Size(area: tuple, frac: float = 0.1) -> int:
    upper_bound = np.around((area[0] * area[1])*frac)
    if upper_bound <= 2:
        upper_bound = 2
    return rd.randint(1, upper_bound)

# options = ["meyerson", "q_meyerson", "all"]
def Test_Meyerson_Alg(iterations: int, area: tuple, costs: int, options: str = "all", q: float = 0.5) -> None:
    # creating the instances
    for i in range(0, iterations):
        sample_size = Sample_Size(area, 0.05)
        input_stream = Generate_Stream(sample_size, area)

        if options == "all":
            test_meyerson = Meyerson_Algorithm_Online(input_stream, costs)
            test_q_meyerson = q_Meyerson_Algorithm_Online(q, input_stream, costs)

            costs_meyerson = Calculate_Costs(test_meyerson, costs)
            costs_q_meyerson = Calculate_Costs(test_q_meyerson, costs)

            print(f"--> Demand: {len(input_stream)}")
            print(f"Meyerson:\t# Facilities: {len(test_meyerson)} for a cost of {costs_meyerson}.")
            print(f"q-Meyerson:\t# Facilities: {len(test_q_meyerson)} for a cost of {costs_q_meyerson}.")
            print(f"---> {costs_q_meyerson <= costs_meyerson}\n")
        else:
            if options == "meyerson":
                test_facilities = Meyerson_Algorithm_Online(input_stream, costs)
            elif options == "q_meyerson":
                test_facilities = q_Meyerson_Algorithm_Online(q, input_stream, costs)
            else:
                raise Exception(f"\n\tOption '{options}' is not valid.")
            
            total_costs = Calculate_Costs(test_facilities, costs)
            
            print(f"--> Demand: {len(input_stream)}")
            print(f"Result:\t# Facilities: {len(test_facilities)} for a cost of {total_costs}.\n")
        
        
if __name__ == "__main__":
    test_area = (25, 25)
    test_cost = 10
    test_size = 5

    #test_stream = Generate_Stream(10, test_area)

    #test_meyerson = Meyerson_Algorithm_Online(test_stream, test_cost)
    #test_cost = Calculate_Costs(test_meyerson, test_cost)
    #result = Draw(test_area, test_stream, test_meyerson, test_cost)
    #result.Plot(True)

    #test_q_meyerson = q_Meyerson_Algorithm_Online(0.5, test_stream, test_cost)
    #test_q_cost = Calculate_Costs(test_q_meyerson, test_cost)
    #q_result = Draw(test_area, test_stream, test_q_meyerson, test_q_cost)
    #q_result.Plot(True)

    Test_Meyerson_Alg(10, test_area, test_cost, "all")
