from owlready2 import *
import datetime

# Create the ontology
onto = get_ontology("http://test.org/bookstore.owl")

def setup_ontology():
    with onto:
        # --- Classes  ---
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

        # --- Properties  ---
        class has_price(Book >> float):
            pass

        class has_stock(Book >> int):
            pass
        
        class has_genre(Book >> str):
            pass
            
        class has_author(Book >> str):
            pass

        class places_order(Customer >> Order):
            pass
            
        class contains_book(Order >> Book):
            pass
            
        class works_at(Employee >> Thing):
            pass

        # --- SWRL Rules [cite: 23, 25, 26] ---
        # Note: We define these as string rules in Owlready2. 
        # These explain the logic of the system.
        
        # Rule 1: If a customer places an order for a book, they have purchased it.
        rule1 = Imp()
        rule1.set_as_rule("""Customer(?c) ^ places_order(?c, ?o) ^ contains_book(?o, ?b) -> purchases(?c, ?b)""")
        
        # Rule 2: Low Stock Warning (Logic for Employee interaction)
        # If a book has stock less than 3, it is a LowStockItem.
        rule2 = Imp()
        rule2.set_as_rule("""Book(?b) ^ has_stock(?b, ?s) ^ swrlb:lessThan(?s, 3) -> LowStockItem(?b)""")

    print("Ontology classes, properties, and SWRL rules defined.")
    return onto

# Initialize
ontology = setup_ontology()

def save_ontology():
    """Helper to save the ontology to a file for the report evidence"""
    onto.save(file="bookstore_ontology.owl", format="rdfxml")
    print("Ontology saved to bookstore_ontology.owl")