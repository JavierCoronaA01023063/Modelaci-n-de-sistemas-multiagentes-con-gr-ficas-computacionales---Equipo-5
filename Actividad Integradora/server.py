from model import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.ModularVisualization import VisualizationElement


def agent_portrayal(agent):
    if agent is None:
        return

    portrayal = {"Filled": "true"}

    if isinstance(agent, OrganizingAgent):
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "Green"
        portrayal["Layer"] = 50
        portrayal["r"] = 0.5

    if isinstance(agent, BoxAgent):
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "Brown"
        portrayal["Layer"] = 0

    return portrayal


model_params = {"N": UserSettableParameter("slider", "Number of Agents", 5, 1, 10, 1), "box": UserSettableParameter(
    "slider", "Number of Boxes", 10, 1, 20, 1), "max_time": UserSettableParameter("slider", "Max Time", 200, 1, 400, 1), "width": 10, "height": 10}

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
server = ModularServer(
    StorageModel, [grid], "Storage Model", model_params)

server.port = 8521
server.launch()
