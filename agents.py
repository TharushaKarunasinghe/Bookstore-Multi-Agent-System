from mesa import Agent
import random
# Import ontology classes to link simulation to ontology concepts
from bms_ontology import ontology

class BookAgent(Agent):
    """ An agent representing a Book in the store. """
    def __init__(self, unique_id, model, title, price, initial_stock, author, genre):
        super().__init__(unique_id, model)
        self.title = title
        self.price = price
        self.stock = initial_stock
        self.author = author
        self.genre = genre
        
        # Sync with Ontology (Creating a semantic instance)
        with ontology:
            self.onto_book = ontology.Book(self.unique_id)
            self.onto_book.has_price = [float(self.price)]
            self.onto_book.has_stock = [int(self.stock)]
            self.onto_book.has_genre = [str(self.genre)]
            self.onto_book.has_author = [str(self.author)]

    def step(self):
        # Update ontology with current simulation state
        self.onto_book.has_stock = [int(self.stock)]

class CustomerAgent(Agent):
    """ An agent representing a Customer. """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.books_bought = 0
        with ontology:
            self.onto_cust = ontology.Customer(self.unique_id)

    def step(self):
        self.move()
        # Interaction Logic
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        books = [obj for obj in cell_contents if isinstance(obj, BookAgent)]
        
        if books:
            book = random.choice(books)
            # Logic: Buy if stock > 0
            if book.stock > 0:
                self.buy_book(book)

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False)
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def buy_book(self, book):
        # 1. Update Simulation State
        book.stock -= 1
        self.books_bought += 1
        
        # 2. Update Ontology (Create an Order)
        with ontology:
            order_id = f"Order_{self.model.schedule.steps}_{self.unique_id}"
            new_order = ontology.Order(order_id)
            self.onto_cust.places_order.append(new_order)
            new_order.contains_book.append(book.onto_book)

        # 3. Message Bus Communication 
        msg = f"PURCHASE: {self.unique_id} bought '{book.title}' (Stock left: {book.stock})"
        self.model.message_bus.append(msg)

class EmployeeAgent(Agent):
    """ An agent representing an Employee. """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        with ontology:
            self.onto_emp = ontology.Employee(self.unique_id)

    def step(self):
        self.move()
        # Logic: Restock based on rule (Stock < 3) [cite: 26]
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        books = [obj for obj in cell_contents if isinstance(obj, BookAgent)]
        
        for book in books:
            if book.stock < 3: 
                self.restock(book)

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False)
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def restock(self, book):
        book.stock += 10
        # Message Bus Communication 
        msg = f"RESTOCK: {self.unique_id} detected low stock on '{book.title}'. Restocked to {book.stock}."
        self.model.message_bus.append(msg)