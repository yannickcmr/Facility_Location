import random as rd
import numpy as np
from time import perf_counter
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

        if Flip_Coin(probability_facility):
            # opens up a new facility.
            facilities_list.append(Facility(demand.position, demand))
        else:
            # uses already existing facility.
            next_facility.Add_Service(demand)
    
    return facilities_list

""" Clustering """
# returns a random starting position.
def Randomize_Center(area: tuple) -> tuple:
    return (rd.randint(0, area[0]), rd.randint(0, area[1]))

# to be continued.


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

def Print_Results(results: list, option: str) -> None:
    if option == "all":
        rating = 0
        for item in results:
            cache = (item[1][1] > item[2][1])
            if cache: rating += 1

            print(f"--> Demand: {item[0]}")
            print(f"meyerson: \t{item[1][0]} Facilities \t{item[1][1]} Costs.")
            print(f"q-meyerson: \t{item[2][0]} Facilities \t{item[2][1]} Costs.")
            print(f"--> {cache}\n")
    
        print(f"Overall performance: {rating/len(results)}")
    
    else:
        for item in results:
            print(f"--> Demand: {item[0]}")
            print(f"{option}: \t{item[1][0]} Facilities \t{item[1][1]} Costs.\n")


# options = ["meyerson", "q_meyerson", "all"]
def Test_Meyerson_Alg(iterations: int, area: tuple, costs: int, option: str = "all", q: float = 0.5, timing: bool = False) -> None:
    if timing: start = perf_counter()
    results_alg = []
    # creating the instances
    if option == "all":
        for i in range(0, iterations):
            # generate test case.
            sample_size = Sample_Size(area, 0.05)
            input_stream = Generate_Stream(sample_size, area)

            # calculate facilities.
            meyerson = Meyerson_Algorithm_Online(input_stream, costs)
            q_meyerson = q_Meyerson_Algorithm_Online(q, input_stream, costs)

            # calculate costs.
            costs_meyerson = Calculate_Costs(meyerson, costs)
            costs_q_meyerson = Calculate_Costs(q_meyerson, costs)

            # append results
            results_alg.append([sample_size, [len(meyerson), costs_meyerson], [len(q_meyerson), costs_q_meyerson]])

    elif (option == "meyerson") or (option == "q_meyerson"):
        for i in range(0, iterations):
            # generate test case.
            sample_size = Sample_Size(area, 0.05)
            input_stream = Generate_Stream(sample_size, area)

            # calculate facilities.
            if option == "meyerson":
                test_facilities = Meyerson_Algorithm_Online(input_stream, costs)
            elif option == "q_meyerson":
                test_facilities = q_Meyerson_Algorithm_Online(q, input_stream, costs)

            # calculate costs and append result to results_alg
            total_costs = Calculate_Costs(test_facilities, costs)
            results_alg.append([sample_size, [len(test_facilities), total_costs]])
    else:
        raise Exception(f"\n\tOption '{option}' is not valid.")

    # end of test
    end = perf_counter()
    Print_Results(results_alg, option)
    print(f"Total time: {end - start}")

if __name__ == "__main__":
    # test options.
    test_area = (100, 100)
    test_facility_cost = 27
    test_stream_size = 20
    test_q_value = 0.5
    test_iterations = 25

    # generate random test stream.
    test_stream = Generate_Stream(test_stream_size, test_area)

    #print(f"---- Meyerson ----")
    #test_meyerson = Meyerson_Algorithm_Online(test_stream, test_facility_cost)
    #cost_meyerson = Calculate_Costs(test_meyerson, test_facility_cost)
    #result = Draw(test_area, test_stream, test_meyerson, cost_meyerson)
    #result.Plot(True)

    #print(f"---- q-Meyerson ----")
    #test_q_meyerson = q_Meyerson_Algorithm_Online(test_q_value, test_stream, test_facility_cost)
    #cost_q_meyerson = Calculate_Costs(test_q_meyerson, test_facility_cost)
    #q_result = Draw(test_area, test_stream, test_q_meyerson, cost_q_meyerson)
    #q_result.Plot(True)

    Test_Meyerson_Alg(test_iterations, test_area, test_facility_cost, timing = True)

    #Test_Meyerson_Alg(10, test_area, test_facility_cost, "all")
    #result = Lloyd_Cluster_Algorithm(test_area, test_stream, 10)
    #print(result)
    #cost = result[0]
    #test_centers = []
    #for item in result[1]:
    #    cache = Facility(item[0], item[1])
    #    test_centers.append()
