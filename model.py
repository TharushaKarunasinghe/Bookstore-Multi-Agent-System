from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from agents import CustomerAgent, EmployeeAgent, BookAgent
from bms_ontology import save_ontology

# --- New Helper Function for the Chart ---
def get_total_stock(model):
    total = 0
    for agent in model.schedule.agents:
        if isinstance(agent, BookAgent):
            total += agent.stock
    return total

class BookstoreModel(Model):
    def __init__(self, N_customers, N_employees, width, height):
        super().__init__()
        self.num_customers = N_customers
        self.num_employees = N_employees
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.message_bus = [] 

        # Book Data
        book_data = [
            {"title": "Python AI", "price": 45.0, "author": "J. Doe", "genre": "Tech"},
            {"title": "Mesa Sim", "price": 30.0, "author": "A. Smith", "genre": "Tech"},
            {"title": "Ontology 101", "price": 55.0, "author": "B. Russell", "genre": "Philosophy"},
            {"title": "SciFi World", "price": 20.0, "author": "H. Wells", "genre": "Fiction"}
        ]

        # Create Book Agents
        for i, data in enumerate(book_data):
            b = BookAgent(f"Book_{i}", self, data["title"], data["price"], 5, data["author"], data["genre"])
            self.schedule.add(b)
            self.grid.place_agent(b, (5, 5 + (i * 2)))

        # Create Customers
        for i in range(self.num_customers):
            a = CustomerAgent(f"Cust_{i}", self)
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        # Create Employees
        for i in range(self.num_employees):
            e = EmployeeAgent(f"Emp_{i}", self)
            self.schedule.add(e)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(e, (x, y))

        # !!! UPDATED DATA COLLECTOR !!!
        # We now use 'model_reporters' to track the Store Total, not individual agents
        self.datacollector = DataCollector(
            model_reporters={"Total Stock": get_total_stock}
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        
        while self.message_bus:
            msg = self.message_bus.pop(0)
            print(f"[BUS]: {msg}")