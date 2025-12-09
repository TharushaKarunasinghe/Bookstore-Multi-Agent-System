from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from agents import CustomerAgent, EmployeeAgent, BookAgent
from bms_ontology import save_ontology

class BookstoreModel(Model):
    def __init__(self, N_customers, N_employees, width, height):
        self.num_customers = N_customers
        self.num_employees = N_employees
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.message_bus = [] # Communication System 

        # Detailed Book Data for Ontology [cite: 14, 15]
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
            self.grid.place_agent(b, (5, 5 + (i * 2))) # Spread them out

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

        self.datacollector = DataCollector(
            agent_reporters={"Stock": lambda a: a.stock if isinstance(a, BookAgent) else 0}
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        
        # Print Message Bus to console (Evidence for interaction)
        while self.message_bus:
            msg = self.message_bus.pop(0)
            print(f"[BUS]: {msg}")

        # Save ontology periodically or at the end (here we just do it on stop manually)