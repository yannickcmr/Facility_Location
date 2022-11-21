import random as rd
import numpy as np
from time import perf_counter
from Facility_Class import Facility, Demand, Draw, Draw_Comparison, Generate_Stream

""" Helper Functions """

def Round(values: float, decimals: int) -> float:
    return np.around(values, decimals=decimals)

# calculates the distance (ordinary norm) of two points and rounds it to 4 decimal places.
def Euclidean_Norm(point_1, point_2) -> float:
    return Round(np.linalg.norm(np.array(point_1) - np.array(point_2)), 4)

# find the closest facility based on the norm. returns the distance and the facility.
def Find_Nearest_Facility(demand: Demand, facility_list: list) -> tuple:
    # base case if facility_list is still empty (1. iteration). 
    if len(facility_list) == 0:
        return (10000, None)
    
    norm = [Euclidean_Norm(demand.position, facility.position) for facility in facility_list]
    return (np.min(norm), facility_list[np.argmin(norm)])

# calculates the relative distance based on the cost of opening a new facility.
def q_Get_Probability(q, distance: float, cost: int) -> float:
    relative_distance = Round(distance/cost, 3)
    relative_distance = q*relative_distance
    return min(relative_distance, 1)

def Flip_Coin(prob: float) -> bool:
    return rd.random() < prob


""" Meyerson's Algorithm """

def Meyerson_Algorithm_Online(demand_list: list, facility_cost: int = 1) -> list[Facility]:
    facilities_list = []
    for demand in demand_list:
        # calculate the relevent values
        norm, next_facility = Find_Nearest_Facility(demand, facilities_list)
        probability_facility = q_Get_Probability(1, norm, facility_cost)

        if Flip_Coin(probability_facility):
            # opens up a new facility.
            facilities_list.append(Facility(demand.position, demand))
        else:
            # uses already existing facility.
            next_facility.Add_Service(demand)
    
    return facilities_list


def q_Meyerson_Algorithm_Online(q: float, demand_list: list, facility_cost: int = 1) -> list[Facility]:
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

# Use the squar root of the amount of facilities.
def Center_Range(demand_set_size: int) -> int:
   return int(np.sqrt(demand_set_size))

# returns a random starting position.
def Randomize_Center(area: tuple) -> tuple:
    return (rd.randint(0, area[0]), rd.randint(0, area[1]))


def Find_Nearest_Center(demand: Demand, centers: list) -> tuple:
    distances = [Euclidean_Norm(demand.position, center) for center in centers]
    nearest_center = np.argmin(distances)
    return centers[nearest_center]


def Calculate_Mean_Center(demands: list) -> tuple:
    len_ = len(demands)
    x_val = [demand.position[0] for demand in demands]
    y_val = [demand.position[1] for demand in demands]
    return (Round(np.sum(x_val) / len_, 3), Round(np.sum(y_val) / len_, 3))


def Update_Centers(clusters: list) -> list[tuple]:
    clusters = [cluster for cluster in clusters if len(cluster) > 0]
    return [Calculate_Mean_Center(cluster) for cluster in clusters]


def Assign_Demand_to_Center(center: tuple, demands: list) -> Facility:
    facility = Facility(center, demands[0])
    for demand in demands[1:]:
        facility.Add_Service(demand)
    return facility


def Lloyd_Clustering(area: tuple, demand_list: list, iteration: int = 5) -> list[Facility]:
    centers = [Randomize_Center(area) for i in range(0, Center_Range(len(demand_list)))]

    for i in range(0, iteration):
        clusters = [[] for center in centers]

        for demand in demand_list:
            nearest_center = Find_Nearest_Center(demand, centers)
            index = centers.index(nearest_center)
            clusters[index].append(demand)

        centers = Update_Centers(clusters)

    return [Assign_Demand_to_Center(center, cluster) for center, cluster in zip(centers, clusters)]

    

""" Cost Function """
# Calculates formula: |F|*f + \sum d(F, u)
# where F: facilities, f: opening costs, d(F,u): distance from demand to the closest facility.
def Calculate_Costs(facilities: list, facility_cost: int) -> float:
    total_cost = 0
    for facility in facilities:
        total_cost += facility_cost

        for demand in facility.service:
            total_cost += Euclidean_Norm(facility.position, demand.position)
    
    return Round(total_cost, 2)


""" Test Function """

def Sample_Size(area: tuple, frac: float = 0.1) -> int:
    upper_bound = Round((area[0] * area[1])*frac, 0)
    if upper_bound <= 2:
        upper_bound = 2
    return rd.randint(1, upper_bound)


def Print_Results(results: list, option: str) -> None:
    if option == "all":
        rating = 0
        for item in results:
            # compare total costs.
            cache = (item[1][1] > item[2][1])
            if cache: rating += 1

            print(f"--> Demand: {item[0]}")
            print(f"meyerson: \t{len(item[1][0])} Facilities \t{item[1][1]} Costs.")
            print(f"q-meyerson: \t{len(item[2][0])} Facilities \t{item[2][1]} Costs.")
            print(f"lloyd: \t\t{len(item[3][0])} Facilities \t{item[3][1]} Costs.")
            print(f"--> {cache}\n")
    
        print(f"Overall performance: {rating/len(results)}")
    
    else:
        for item in results:
            print(f"--> Demand: {item[0]}")
            print(f"{option}: \t{len(item[1][0])} Facilities \t{item[1][1]} Costs.\n")



def Test_Algorithm(iterations: int, area: tuple, costs: int, option: str = "meyerson", q: float = 0.5, timing: bool = False) -> list:
    # options = ["meyerson", "q_meyerson", "lloyd"]
    if timing: start = perf_counter()
    results_alg = []
    # creating the instances
    for i in range(0, iterations):
        if timing: iter_start = perf_counter()
        # generate test case.
        sample_size = Sample_Size(area, 0.05)
        input_stream = Generate_Stream(sample_size, area)

        # calculate facilities.
        if option == "meyerson":
            test_facilities = Meyerson_Algorithm_Online(input_stream, costs)
        elif option == "q_meyerson":
            test_facilities = q_Meyerson_Algorithm_Online(q, input_stream, costs)
        elif option == "lloyd":
            test_facilities = Lloyd_Clustering(area, input_stream, iteration=10)
        else:
            raise Exception(f"\n\tOption '{option}' is not valid.")

        if timing: iter_facilities_time = perf_counter()

        # calculate costs and append result to results_alg
        total_costs = Calculate_Costs(test_facilities, costs)
        results_alg.append([sample_size, [test_facilities, total_costs]])

        if timing:
            print(f"{len(input_stream)}\t{Round(iter_facilities_time - iter_start, 5)}\t\t{Round(perf_counter() - iter_facilities_time, 5)}")
    # end of test
    end = perf_counter()
    Print_Results(results_alg, option)

    print(f"Total time: {end - start} sec for {sum([x[0] for x in results_alg])} Demand points.")
    print(f"Per Demand point time: {Round((end - start)/sum([x[0] for x in results_alg]), 5)}\n\n")
    # returns list of list with [#demand, [Facility, cost]]
    return results_alg

# compares the three algorithms, namely Meyerson, q-meyerson, lloyd
# returns list consisting of [#demand, [Facility, cost], [Facility, cost], [Facility, cost]]
def Compare_Algorithms(iterations: int, area: tuple, costs: int, q: float = 0.5, timing: bool = False) -> list:
    if timing: start = perf_counter()
    results_alg = []
    # start of the simulation
    for i in range(0, iterations):
        if timing: iter_start = perf_counter()
        # generate test case.
        sample_size = Sample_Size(area, 0.05)
        input_stream = Generate_Stream(sample_size, area)

        # calculate facilities.
        meyerson = Meyerson_Algorithm_Online(input_stream, costs)
        q_meyerson = q_Meyerson_Algorithm_Online(q, input_stream, costs)
        lloyd = Lloyd_Clustering(area, input_stream, iteration=10)
        if timing: iter_facilities_time = perf_counter()

        # calculate costs.
        costs_meyerson = Calculate_Costs(meyerson, costs)
        costs_q_meyerson = Calculate_Costs(q_meyerson, costs)
        costs_lloyd = Calculate_Costs(lloyd, costs)
        if timing: 
            print(f"{len(input_stream)}\t{Round(iter_facilities_time - iter_start, 5)}\t\t{Round(perf_counter() - iter_facilities_time, 5)}")

        # append results
        results_alg.append([sample_size, [meyerson, costs_meyerson], [q_meyerson, costs_q_meyerson], [lloyd, costs_lloyd]])

    end = perf_counter()
    Print_Results(results_alg, "all")

    print(f"Total time: {end - start} sec for {sum([x[0] for x in results_alg])} Demand points.")
    print(f"Per Demand point time: {Round((end - start)/sum([x[0] for x in results_alg]), 5)}\n\n")


    return results_alg


if __name__ == "__main__":
    """ test options """
    test_area = (100, 100)
    test_facility_cost = 27
    test_stream_size = 20
    test_q_value = 0.5
    test_iterations = 10

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
    #q_result.Plot()

    #print(f"---- Lloyd ----")
    #test_lloyd = Lloyd_Clustering(test_area, test_stream)
    #cost_lloyd = Calculate_Costs(test_lloyd, test_facility_cost)
    #lloyd_result = Draw(test_area, test_stream, test_lloyd, cost_lloyd)
    #lloyd_result.Plot(True)

    Test_Algorithm(test_iterations, test_area, test_facility_cost, "meyerson", timing = True)
    Compare_Algorithms(test_iterations, test_area, test_facility_cost, timing=True)