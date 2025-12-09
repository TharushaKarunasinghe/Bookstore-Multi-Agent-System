from owlready2 import *

# Create and load the ontology
onto = get_ontology("http://test.org/bookstore.owl")

def setup_ontology():
    with onto:
        # Define Classes [cite: 14]
        class Book(Thing):
            pass
        
        class Person(Thing):
            pass

        class Customer(Person):
            pass

        class Employee(Person):
            pass
        
        class Inventory(Thing):
            pass

        # Define Properties [cite: 15]
        class has_price(Book >> float):
            pass

        class has_stock(Book >> int):
            pass
            
        class purchases(Customer >> Book):
            pass
            
        class works_at(Employee >> Thing):
            pass

        # SWRL Rule Example: If customer purchases book, they are related [cite: 25]
        # Note: Owlready2 SWRL implementation can be complex; 
        # this initializes the structure.
        rule = Imp()
        rule.set_as_rule("""Customer(?c) ^ Book(?b) ^ purchases(?c, ?b) -> has_purchased(?c, ?b)""")

    print("Ontology classes and rules loaded successfully.")
    return onto

# Initialize on import
ontology = setup_ontology()