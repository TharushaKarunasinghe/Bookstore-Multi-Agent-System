from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from agents import CustomerAgent, EmployeeAgent, BookAgent

class BookstoreModel(Model):
    """ A model with some number of agents. """
    def __init__(self, N_customers, N_employees, width, height):
        self.num_customers = N_customers
        self.num_employees = N_employees
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        
        # Message Bus [cite: 27]
        self.message_bus = []

        # Create Book Agents (placed at fixed locations like shelves)
        book_titles = ["Python 101", "AI Basics", "Mesa Guide", "Ontology 101"]
        for i, title in enumerate(book_titles):
            b = BookAgent(f"Book_{i}", self, title, price=20.0, initial_stock=5)
            self.schedule.add(b)
            # Place books in the middle
            self.grid.place_agent(b, (5, 5 + i))

        # Create Customer Agents
        for i in range(self.num_customers):
            a = CustomerAgent(f"Cust_{i}", self)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        # Create Employee Agents
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
        # Print Message Bus for Debugging
        if self.message_bus:
            print(self.message_bus[-1]) # Print latest message