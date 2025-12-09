from mesa import Agent
import random

class BookAgent(Agent):
    """ An agent representing a Book in the store. [cite: 20] """
    def __init__(self, unique_id, model, title, price, initial_stock):
        super().__init__(unique_id, model)
        self.title = title
        self.price = price
        self.stock = initial_stock
        self.genre = random.choice(["Fiction", "Sci-Fi", "History"])

    def step(self):
        # Book agents are passive entities in this sim, but they hold state
        pass

class CustomerAgent(Agent):
    """ An agent representing a Customer. [cite: 18] """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.books_bought = 0

    def step(self):
        # Logic: Randomly browse and buy
        # 1. Move randomly
        self.move()
        # 2. Check if there is a book here
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        books = [obj for obj in cell_contents if isinstance(obj, BookAgent)]
        
        if books:
            book = random.choice(books)
            if book.stock > 0:
                self.buy_book(book)

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False)
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def buy_book(self, book):
        # Logic: Reduce stock, message bus update [cite: 25]
        book.stock -= 1
        self.books_bought += 1
        self.model.message_bus.append(f"SALE: Customer {self.unique_id} bought {book.title}")

class EmployeeAgent(Agent):
    """ An agent representing an Employee. [cite: 19] """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        self.move()
        # Logic: Check for low inventory and restock [cite: 19]
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        books = [obj for obj in cell_contents if isinstance(obj, BookAgent)]
        
        for book in books:
            if book.stock < 3: # Threshold
                self.restock(book)

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False)
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def restock(self, book):
        # Logic: Increase stock [cite: 26]
        book.stock += 10
        self.model.message_bus.append(f"RESTOCK: Employee {self.unique_id} restocked {book.title}")