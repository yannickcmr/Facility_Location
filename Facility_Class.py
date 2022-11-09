import random as rd
import matplotlib.pyplot as plt

""" Classes """

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

# split the x and y coordinates into two list. used for plotting.
def Split_Position(points: list):
    x_pos = [point.position[0] for point in points]
    y_pos = [point.position[1] for point in points]
    return x_pos, y_pos

# split x and y coordinates into two list for all demands, that a facility serves. used for plotting.
def Get_Service_Connections(facility: Facility) -> list:
    x_pos = [(point.position[0], facility.position[0]) for point in facility.service]
    y_pos = [(point.position[1], facility.position[1]) for point in facility.service]
    return x_pos, y_pos

class Draw:
    def __init__(self, area: tuple, demands: list, facilites: list, costs: float = 0) -> None:
        self.area = area
        self.demands = demands
        self.facilities = facilites
        self.costs = costs
    
    def Plot(self, show_rel: bool = False):
        # formating the title.
        title_str = f"Area:{self.area}\nDemand:{len(self.demands)} --- Facilities: {len(self.facilities)}"
        if self.costs > 0: 
            title_str += f" --- Costs: {self.costs}"
        
        # Preparing the plot.
        figure, axes = plt.subplots()
        figure.set_size_inches(10, 7)
        figure.canvas.set_window_title("Facility Location")
        plt.title(title_str)
        
        axes.set_aspect("equal")
        plt.grid(True, which="both")
        plt.xlim([-1, self.area[0] + 1])
        plt.ylim([-1, self.area[1] + 1])

        # get data points to plot.
        x_demand, y_demand = Split_Position(self.demands)
        x_facilities, y_facilities = Split_Position(self.facilities)

        # demand will be shown as black dots, facilities as red stars
        plt.scatter(x_demand, y_demand , color="black", s=50, zorder=2)
        plt.scatter(x_facilities, y_facilities , color="red", s=50, marker="*", zorder=2)

        # if you want to see which facility serves which demand, set it to True.
        if show_rel:
            for facility in self.facilities:
                # get the coordinates for all the demands served.
                x_service, y_service = Get_Service_Connections(facility)

                for i in range(0, len(x_service)):
                    plt.plot(x_service[i], y_service[i], color="grey", zorder=-2)

        plt.show()


""" Functions """

# create a random Demand within the defined realm. 
def Randomize_Demand(area: tuple) -> Demand:
    pos_demand = [rd.randint(0, area[i]) for i in range(0, len(area))]
    return Demand(tuple(pos_demand))

# generate set_size many random Demands.
def Generate_Stream(set_size: int, area: tuple) -> list:
    return [Randomize_Demand(area) for i in range(0, set_size)]


if __name__ == "__main__":
    test_demand = Demand((3,4))
    test_stream = Generate_Stream(3, (5,5))

    test_facility = Facility((2,3), test_demand)
    for demand in test_stream:
        test_facility.Add_Service(demand)

    test_draw = Draw((5,5), [test_demand, *test_stream], [test_facility])
    test_draw.Plot(True)
