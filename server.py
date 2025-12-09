from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.ModularVisualization import ModularServer
from model import BookstoreModel
from agents import CustomerAgent, EmployeeAgent, BookAgent

# --- 1. Define the CSS Injection Class ---
class CssStyle(TextElement):
    def __init__(self):
        pass

    def render(self, model):
        return """
        <style>
        /* 1. Make the main container wide enough to hold both elements */
        .container {
            width: 98% !important;
            max-width: 98% !important;
        }
        
        /* 2. Target the rows/columns that Mesa generates */
        /* We force them to be inline-blocks so they sit next to each other */
        .row > div, .col-sm-12, .col-md-6, .col-lg-4 {
            width: 48% !important;  /* Take up roughly half the screen */
            display: inline-block !important;
            vertical-align: top !important;
            margin-right: 1%;
        }

        /* 3. Ensure the chart and grid fit inside these boxes */
        canvas {
            max-width: 100% !important;
        }
        </style>
        """

# --- 2. Define the Agent Visuals ---
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
        portrayal["text"] = str(agent.stock)
        portrayal["text_color"] = "white"

    return portrayal

# --- 3. Setup the Grid and Chart ---
# Note: CanvasGrid(width, height, pixel_w, pixel_h)
# We set pixel width slightly smaller to ensure it fits easily
grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)

chart = ChartModule([{"Label": "Total Stock", "Color": "Black"}],
                    data_collector_name='datacollector')

# --- 4. Launch the Server ---
# IMPORTANT: The order in the list determines the order on screen.
# [CssStyle(), grid, chart] -> CSS loads, then Grid (Left), then Chart (Right)
server = ModularServer(BookstoreModel,
                       [CssStyle(), grid, chart], 
                       "Bookstore Simulation",
                       {"N_customers": 5, "N_employees": 2, "width": 20, "height": 20})

server.port = 8521