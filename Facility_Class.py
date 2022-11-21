import random as rd
import os
import matplotlib.pyplot as plt
import numpy as np

Save_Path = "Tests/Test_Meyerson/"

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


def Extract_Demands(result: list) -> list[Demand]:
    return [demand for facility in result[0] for demand in facility.service]

def Percent(value_1, value_2) -> str:
    value = str(np.around(value_1/value_2 - 1, decimals=4)).translate({ord("."): None})
    return f"+{value[1:3]}.{value[3:]}%"

class Draw_Comparison:
    def __init__(self, area: tuple, facility_cost: int, sample_size: int, meyerson: list, q_meyerson: list, lloyd: list) -> None:
        self.area = area
        self.costs = facility_cost
        self.sample_size = sample_size
        self.result_1 = meyerson
        self.result_2 = q_meyerson
        self.result_3 = lloyd
    
    def Generate_Plot(self) -> plt:
        # Preparing the plot.
        figure, ((ax_1, ax_2), (ax_3, ax_4)) = plt.subplots(2 ,2)
        figure.set_size_inches(10, 7)
        figure.canvas.set_window_title("Facility Location")

        # generating the plots.
        axes = [(ax_1, "Meyerson", self.result_1), (ax_2, "q-Meyerson", self.result_2), (ax_3, "Lloyd", self.result_3)]
        for ax in axes:
            # format subplot
            ax[0].set_aspect("auto")
            ax[0].grid(True, which="both")
            ax[0].set(xlim=(-1, self.area[0] + 1), ylim=(-1, self.area[1] + 1))
            ax[0].set_title(ax[1])

            # extract points.
            x_facilities, y_facilities = Split_Position(ax[2][0])
            x_demand, y_demand = Split_Position(Extract_Demands(ax[2]))

            ax[0].scatter(x_demand, y_demand , color="black", s=50, zorder=2)
            ax[0].scatter(x_facilities, y_facilities , color="red", s=50, marker="*", zorder=2)

            for facility in ax[2][0]:
                # get the coordinates for all the demands served.
                x_service, y_service = Get_Service_Connections(facility)

                for i in range(0, len(x_service)):
                    ax[0].plot(x_service[i], y_service[i], color="grey", zorder=-2)


        # formating the textbox
        text_str = "\n".join([f"Area: {self.area}\t Opening Costs:{self.costs}", "",
                                f"Comparison of {self.sample_size} Demand points", "", 
                                f"Meyerson:\t{len(self.result_1[0])} Facilities\t{self.result_1[1]} Costs",
                                f"q-Meyerson:\t{len(self.result_2[0])} Facilities\t{self.result_2[1]} Costs",
                                f"Lloyd:\t\t\t{len(self.result_3[0])} Facilities\t{self.result_3[1]} Costs", "",
                                f"Performance:\t{Percent(self.result_1[1], self.result_3[1])}\t\t{Percent(self.result_2[1], self.result_3[1])}"])
        
        props = dict(boxstyle='round', facecolor='lightgray', alpha=0.5)
        ax_4.axis('off')
        ax_4.text(0, 0.82, text_str.expandtabs(), fontsize=12, verticalalignment='top', horizontalalignment='left', bbox = props)

        return plt

    def Plot(self) -> None:
        plt_compare = self.Generate_Plot()
        plt_compare.show()

    def Save(self, file_name: str, dpi: int = 300, format: str = "png") -> None:
        # formating the save path.
        file_name = f"{file_name}.{format}"
        path = os.path.join(Save_Path, file_name)

        plt_compare = self.Generate_Plot()
        plt_compare.savefig(path, dpi = dpi, format = format, bbox_inches = "tight")

""" Functions """

# create a random Demand within the defined realm. 
def Randomize_Demand(area: tuple) -> Demand:
    pos_demand = [rd.randint(0, area[i]) for i in range(0, len(area))]
    return Demand(tuple(pos_demand))

# generate set_size many random Demands.
def Generate_Stream(set_size: int, area: tuple) -> list[Demand]:
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
