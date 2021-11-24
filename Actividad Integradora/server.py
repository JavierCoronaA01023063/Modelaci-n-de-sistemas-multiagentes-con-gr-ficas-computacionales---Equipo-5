from model import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.ModularVisualization import VisualizationElement
from numpy import histogram as np_histogram

COLORS = {"Moving": "#ffd966", "Box": "#744700", "Delivered": "Green"}


def agent_portrayal(agent):
    if agent is None:
        return

    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 1,
                 "Color": "grey",
                 "r": 0.5}

    if isinstance(agent, OrganizingAgent):
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "Red"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.5

    if isinstance(agent, BoxAgent):
        portrayal["Shape"] = "circle"
        portrayal["Color"] = COLORS[agent.condition]
        portrayal["Layer"] = 1

    return portrayal


class HistogramModule(VisualizationElement):
    package_includes = ["Chart.min.js"]
    local_includes = ["HistogramModule.js"]

    def __init__(self, bins, canvas_height, canvas_width):
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.bins = bins
        new_element = "new HistogramModule({}, {}, {})"
        new_element = new_element.format(bins, canvas_width, canvas_height)
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        agents_move = []
        for agent in model.schedule.agents:
            if isinstance(agent, OrganizingAgent):
                agents_move.append(agent.move_count)
        hist = np_histogram(agents_move, bins=self.bins)[0]
        return [int(x) for x in hist]


model_params = {"N": UserSettableParameter("slider", "Number of Agents", 1, 1, 10, 1), "box": UserSettableParameter(
    "slider", "Number of Boxes", 5, 1, 20, 1), "max_time": UserSettableParameter("slider", "Max Time", 200, 1, 400, 1), "width": 10, "height": 10}

histogram = HistogramModule(
    list(range(201)), 200, 500)

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
server = ModularServer(
    StorageModel, [grid, histogram], "Storage Model", model_params)

server.port = 8521
server.launch()
