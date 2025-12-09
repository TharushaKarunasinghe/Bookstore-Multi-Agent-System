from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.ModularVisualization import ModularServer
from model import BookstoreModel
from agents import CustomerAgent, EmployeeAgent, BookAgent

# --- 1. Strong CSS to Force Side-by-Side Layout ---
class CssStyle(TextElement):
    def __init__(self):
        pass

    def render(self, model):
        return """
        <style>
        /* A. Break the narrow container limit */
        .container, .container-fluid {
            width: 100% !important;
            max-width: 100% !important;
            margin: 0 !important;
            padding: 10px !important;
        }

        /* B. Force the main content row to use Flexbox */
        .row {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important; /* Do not allow wrapping */
            justify-content: center !important;
            align-items: flex-start !important;
        }

        /* C. Force the individual elements (Grid & Chart) to split width */
        /* We target the bootstrap columns Mesa generates */
        .col-sm-12, .col-md-6, .col-lg-4 {
            width: 48% !important;  /* Force nearly half width */
            max-width: 48% !important;
            flex: 0 0 48% !important;
            display: block !important;
            margin: 5px !important;
        }
        </style>
        """

# --- 2. Define Agent Visuals ---
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

# --- 3. Setup Grid and Chart ---
# CHANGED: Reduced grid size to 450x450 to ensure it fits side-by-side on laptops
grid = CanvasGrid(agent_portrayal, 20, 20, 450, 450)

chart = ChartModule([{"Label": "Total Stock", "Color": "Black"}],
                    data_collector_name='datacollector')

# --- 4. Launch ---
# The order matters: CSS first, then Grid, then Chart.
server = ModularServer(BookstoreModel,
                       [CssStyle(), grid, chart], 
                       "Bookstore Simulation",
                       {"N_customers": 5, "N_employees": 2, "width": 20, "height": 20})

# CHANGED: Port updated to 8523 to avoid "Address already in use" error
server.port = 8523