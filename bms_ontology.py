from owlready2 import *
import datetime

# Create the ontology
onto = get_ontology("http://test.org/bookstore.owl")

def setup_ontology():
    with onto:
        # --- Classes ---
        class Book(Thing):
            pass
        
        class Person(Thing):
            pass

        class Customer(Person):
            pass

        class Employee(Person):
            pass
        
        class Order(Thing):
            pass
            
        class Inventory(Thing):
            pass
        
        # !!! Added missing class !!!
        class LowStockItem(Book):
            pass

        # --- Properties ---
        class has_price(Book >> float):
            pass

        class has_stock(Book >> int):
            pass
        
        class has_genre(Book >> str):
            pass
            
        class has_author(Book >> str):
            pass

        class purchases(Customer >> Book):
            pass

        class places_order(Customer >> Order):
            pass
            
        class contains_book(Order >> Book):
            pass
            
        class works_at(Employee >> Thing):
            pass

        # --- SWRL Rules ---
        
        # Rule 1: Purchase Logic
        # If a customer orders a book, they are marked as purchasing it.
        try:
            rule1 = Imp()
            rule1.set_as_rule("""Customer(?c) ^ places_order(?c, ?o) ^ contains_book(?o, ?b) -> purchases(?c, ?b)""")
        except Exception as e:
            print(f"Warning: Could not load Rule 1: {e}")

        # Rule 2: Low Stock Logic
        # We wrap this in try/except because 'swrlb' built-ins can be unstable in some environments.
        # The actual restocking logic is also implemented in agents.py (Python level).
        try:
            rule2 = Imp()
            # Simplified rule to avoid swrlb namespace crash if not loaded
            # We try to define it, but if it fails, we skip it to keep the app running.
            rule2.set_as_rule("""Book(?b) ^ has_stock(?b, ?s) ^ swrlb:lessThan(?s, 3) -> LowStockItem(?b)""")
        except Exception as e:
            print(f"Warning: SWRL 'lessThan' rule skipped to prevent crash. Logic is handled by Agents.")

    print("Ontology classes, properties, and SWRL rules defined.")
    return onto

# Initialize
ontology = setup_ontology()

def save_ontology():
    """Helper to save the ontology to a file for the report evidence"""
    onto.save(file="bookstore_ontology.owl", format="rdfxml")
    print("Ontology saved to bookstore_ontology.owl")