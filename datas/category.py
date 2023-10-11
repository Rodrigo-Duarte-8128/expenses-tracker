
class Category:
    '''
    A category is used to organize transactions. A category has a name like "Transportation", it has a kind which is
    "Income" or "Expense", and it has a list of subcategories. 

    Each category is uniquely identified by its name, so there cannot be two different categories with the same name.

    subcategories is a dictionary where the keys are the subcategory names and the values are SubCategory objects

    In memory Categories are stored as the key value pair:
    "category_name": {
        "kind": kind,
        "subcategories": {
            "subcategory_name": {
                "name": subcategory_name,
                "essential": is_essential
            }
        }
    }
    
    '''
    def __init__(self, name, kind, subcategories):
        self.name = name 
        self.kind = kind
        self.subcategories = subcategories




class SubCategory:
    '''
    A subcategory is uniquely identified by its name and parent, so there cannot be two subcategories with the same parent and the same name. 
    However, two subcategories can have the same name if they have different parents.

    The parent_name of a subcategory is a string corresponding to the Category name to which the subcategory belongs.

    A subcategory is essential if the transactions whithin it are considered to be essential. This only applies if the kind of the parent
    category is "Expense". This categorization is useful to estimate how much of the monthly budget can be spent on non-essential expenses.
    If the parent is not an expense, then this property defaults to True.
    '''
    def __init__(self, name, parent_name, essential=True):
        self.name = name
        self.parent_name = parent_name
        self.essential = essential
        

