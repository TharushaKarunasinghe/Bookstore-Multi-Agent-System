from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from model import BookstoreModel
from agents import CustomerAgent, EmployeeAgent, BookAgent

def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}

    if isinstance(agent, CustomerAgent):
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.5
        
    elif isinstance(agent, EmployeeAgent):
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.7

    elif isinstance(agent, BookAgent):
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "green"
        portrayal["Layer"] = 0
        portrayal["w"] = 0.8
        portrayal["h"] = 0.8
        # Display stock on the grid
        portrayal["text"] = str(agent.stock)
        portrayal["text_color"] = "white"

    return portrayal

grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)

# Create a chart to track stock levels
chart = ChartModule([{"Label": "Stock", "Color": "Black"}],
                    data_collector_name='datacollector')

server = ModularServer(BookstoreModel,
                       [grid, chart],
                       "Bookstore Simulation",
                       {"N_customers": 5, "N_employees": 2, "width": 20, "height": 20})

server.port = 8521 # The default