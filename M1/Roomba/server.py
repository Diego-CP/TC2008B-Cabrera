from model import RandomModel, ObstacleAgent
from mesa.visualization.modules import CanvasGrid, BarChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

def agent_portrayal(agent):
    if agent is None: return
    
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 1,
                 "Color": "red",
                 "r": 0.5}

    if (isinstance(agent, ObstacleAgent)):
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.2

    return portrayal

model_params = {"N":5, "width":10, "height":10}

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
bar_chart = BarChartModule(
    [{"Label":"Steps", "Color":"#AA0000"}], 
    scope="agent", sorting="ascending", sort_by="Steps")

server = ModularServer(RandomModel, [grid, bar_chart], "Random Agents", {"N":20, "width":10, "height":10, "D": UserSettableParameter("slider", "Dust percentage", 0.1, 0.01, 0.5, 0.01), "T": UserSettableParameter("slider", "Maximum Execution Time (s)", 10, 5, 60, 0.5)})
                       
server.port = 8521 # The default
server.launch()