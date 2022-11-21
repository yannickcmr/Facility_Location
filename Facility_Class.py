import random as rd
import os
import matplotlib.pyplot as plt

Save_Path = "Test_Meyerson/"

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

# split the x and y coordinates into two list. used for plotting.
def Split_Position(points: list) -> tuple:
    x_pos = [point.position[0] for point in points]
    y_pos = [point.position[1] for point in points]
    return (x_pos, y_pos)

# split x and y coordinates into two list for all demands, that a facility serves. used for plotting.
def Get_Service_Connections(facility: Facility) -> tuple:
    x_pos = [(point.position[0], facility.position[0]) for point in facility.service]
    y_pos = [(point.position[1], facility.position[1]) for point in facility.service]
    return (x_pos, y_pos)

""" Classes Plot """

class Draw:
    def __init__(self, area: tuple, demands: list, facilites: list, costs: float = 0) -> None:
        self.area = area
        self.demands = demands
        self.facilities = facilites
        self.costs = costs

    def Generate_Plot(self) -> plt:
        # Preparing the plot.
        figure, axes = plt.subplots()
        figure.set_size_inches(10, 7)
        figure.canvas.set_window_title("Facility Location")
        
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

        # plot the lines to see, which facility serves which demand point.
        for facility in self.facilities:
            # get the coordinates for all the demands served.
            x_service, y_service = Get_Service_Connections(facility)

            for i in range(0, len(x_service)):
                plt.plot(x_service[i], y_service[i], color="grey", zorder=-2)

        return plt

    def Plot(self) -> None:
        # formating the title.
        title_str = f"Area:{self.area}\nDemand:{len(self.demands)} --- Facilities: {len(self.facilities)}"
        if self.costs > 0: 
            title_str += f" --- Total Costs: {self.costs}"
        
        # generate the plot.
        plt_self = self.Generate_Plot()
        plt_self.title(title_str)
        plt_self.show()


    def Save(self, file_name: str, dpi: int = 300, format: str = "png") -> None:
        # formating the save path.
        file_name = f"{file_name}.{format}"
        path = os.path.join(Save_Path, file_name)

        # formating the title.
        title_str = f"Area:{self.area}\nDemand:{len(self.demands)} --- Facilities: {len(self.facilities)}"
        if self.costs > 0: 
            title_str += f" --- Total Costs: {self.costs}"

        # generating the plot.
        plt_self = self.Generate_Plot()
        plt_self.title(title_str)
        plt_self.savefig(path, dpi = dpi, format = format, bbox_inches = "tight")


class Draw_Comparison:
    def __init__(self, area: tuple, meyerson: list, q_meyerson: list, lloyd: list) -> None:
        self.area = area
        self.result_1 = meyerson
        self.result_2 = q_meyerson
        self.result_3 = lloyd
    
    def Plot(self) -> plt:
        figure, axes = plt.subplots(2 ,2)
        figure.set_size_inches(10, 7)
        figure.canvas.set_window_title("Facility Location")


""" Functions """

# create a random Demand within the defined realm. 
def Randomize_Demand(area: tuple) -> Demand:
    pos_demand = [rd.randint(0, area[i]) for i in range(0, len(area))]
    return Demand(tuple(pos_demand))

# generate set_size many random Demands.
def Generate_Stream(set_size: int, area: tuple) -> list:
    return [Randomize_Demand(area) for i in range(0, set_size)]


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
    #test_draw = Draw(test_area, [test_demand, *test_stream], [test_facility])
    #test_draw.Plot()
    #test_draw.Save("test_save")

    #test_results = Draw_Results(test_area)
