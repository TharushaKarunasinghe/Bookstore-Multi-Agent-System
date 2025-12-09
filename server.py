from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.ModularVisualization import ModularServer
from model import BookstoreModel
from agents import CustomerAgent, EmployeeAgent, BookAgent

# --- 1. Define the Toggle Button & Logic ---
class ChartToggleButton(TextElement):
    def __init__(self):
        pass

    def render(self, model):
        # We inject HTML for a button and JS to control the visibility
        return """
        <div style='text-align: center; margin-top: 20px; margin-bottom: 20px;'>
            <button id='toggleBtn' class='btn btn-primary' style='font-size: 16px; padding: 10px 20px;' onclick='toggleChartDisplay()'>
                📊 Show/Hide Stock Chart
            </button>
        </div>
        
        <script>
            var isChartVisible = false;

            // This function runs automatically to HIDE the chart initially
            function initChartHiding() {
                // Mesa puts visualization modules in divs. We assume the Chart is the LAST one.
                // We target the main visualization containers
                var rows = document.querySelectorAll(".row > div");
                
                if (rows.length > 0) {
                    // The last element is the Chart (because we add it last in ModularServer)
                    var chartContainer = rows[rows.length - 1]; 
                    chartContainer.id = "myChartContainer"; // Give it an ID
                    chartContainer.style.display = "none";  // Hide it
                }
            }

            // This function runs when you click the button
            function toggleChartDisplay() {
                var chartContainer = document.getElementById("myChartContainer");
                if (chartContainer) {
                    if (isChartVisible) {
                        chartContainer.style.display = "none";
                        isChartVisible = false;
                    } else {
                        chartContainer.style.display = "block";
                        isChartVisible = true;
                    }
                }
            }

            // Wait 1 second for Mesa to load everything, then hide the chart
            setTimeout(initChartHiding, 1000);
        </script>
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
grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)

chart = ChartModule([{"Label": "Total Stock", "Color": "Black"}],
                    data_collector_name='datacollector')

# --- 4. Launch ---
# Order: [Grid, Button, Chart]
# The JS inside 'ChartToggleButton' will look for the LAST item (Chart) and hide it.
server = ModularServer(BookstoreModel,
                       [grid, ChartToggleButton(), chart], 
                       "Bookstore Simulation",
                       {"N_customers": 5, "N_employees": 2, "width": 20, "height": 20})

# New Port to avoid errors
server.port = 9001