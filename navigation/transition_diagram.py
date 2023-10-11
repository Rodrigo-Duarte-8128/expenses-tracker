

class TransitionDiagram:
    '''
    The diagram has a list of ordered roots, where earlier screens are above later screens in the list

    The nodes dictionary has keys which are node names and the corresponding value is the node with that name. There can't be two different nodes with the same name.

    The idea is that if screen1 belongs to root1 and screen2 belongs to root2, and root1 is above root2, then screen1 is above screen2. 

    The full list of root_nodes needs to be set when initializing the app

    '''

    def __init__(self, root_nodes_list: list, nodes_dict: dict):
        self.root_nodes_list = root_nodes_list
        self.nodes_dict = nodes_dict


    def add_node(self, name, left_node_name=None, **kwargs):
        if kwargs["root_screen_node"] == None:
            raise ValueError("New node cannot be root.")
        if name in self.nodes_dict:
            raise ValueError("Node name already exists.")
        

        if left_node_name == None:
            if kwargs["left_node"] not in self.nodes_dict.values():
                raise ValueError("Passed left node does not exist.")
            new_node = ScreenNode(name, **kwargs)           
        else:
            if left_node_name not in self.nodes_dict:
                raise ValueError("Passed left node name does not exist.")
            left_node = self.nodes_dict[left_node_name]
            new_node = ScreenNode(name, left_node = left_node, **kwargs)        

        self.nodes_dict[name] = new_node


    def remove_node(self, node_name):
        if node_name not in self.nodes_dict:
            raise ValueError("Node name does not exist.")
        del self.nodes_dict[node_name]




    def compute_direction(self, screen_name1, screen_name2):
        '''
        returns "left", "right", "up" or "down" if the correct transition from screen_name1 to screen_name2 is "left", "right", "up" or "down"
        '''

        node1 = self.nodes_dict[screen_name1]
        node2 = self.nodes_dict[screen_name2]

        if node1 == node2:
            return "right" # this case shouldn't happen


        
        if node1.root_screen_node == None and node2.root_screen_node == None:
            if self.root_nodes_list.index(node1) < self.root_nodes_list.index(node2):
                return "up"
            else:
                return "down"

        if (node1.root_screen_node == None and node2.root_screen_node != None) and node2.root_screen_node != node1:
            if self.root_nodes_list.index(node1) < self.root_nodes_list.index(node2.root_screen_node):
                return "up"
            else:
                return "down"
        
        if (node1.root_screen_node != None and node2.root_screen_node == None) and node1.root_screen_node != node2:
            if self.root_nodes_list.index(node1.root_screen_node) < self.root_nodes_list.index(node2):
                return "up"
            else:
                return "down"
            
        if (node1.root_screen_node != None and node2.root_screen_node != None) and node1.root_screen_node != node2.root_screen_node:
            if self.root_nodes_list.index(node1.root_screen_node) < self.root_nodes_list.index(node2.root_screen_node):
                return "up"
            else:
                return "down"           
        
        
            

        # at this point both screens are at the same height

        # if one of the screens is the root at this height the direction is immediately determined
        if node1.root_screen_node == None:
            return "left"
        if node2.root_screen_node == None:
            return "right"
        
        # at this point both screens are at the same height and neither is the root
        root = node1.root_screen_node

        # go left from node1 and see if we find node 2
        node2_before_node1 = False
        current_node = node1
        while not node2_before_node1 and current_node != root:
            if current_node.left_node == node2:
                node2_before_node1 = True
            current_node = current_node.left_node

        if node2_before_node1:
            return "right"

        # if node2 is not to the left of node1 go left from node2 and see if we find node 1
        node1_before_node2 = False
        current_node = node2
        while not node1_before_node2 and current_node != root:
            if current_node.left_node == node1:
                node1_before_node2 = True
            current_node = current_node.left_node
        
        if node1_before_node2:
            return "left"
        
        # in any other case the screens are not comparable so we just return something random
        return "right"

        


class ScreenNode:
    '''
    A screen node represents a screen. They have a root_screen_node attribute, and they have an attribute for the screen that is to its left.

    A root node has root_screen_node = None
    '''
    def __init__(self, name, root_screen_node=None, left_node=None):
        self.name = name
        self.root_screen_node = root_screen_node
        self.left_node = left_node
        
        





if __name__=="__main__":
    # create roots
    home_screen = ScreenNode("home_screen")
    accounts_screen = ScreenNode("accounts_screen")
    categories_screen = ScreenNode("categories_screen")
    records_screen = ScreenNode("records_screen")

    
    root_nodes_list = [
        home_screen, 
        accounts_screen,
        categories_screen,
        records_screen
    ]

    nodes_dict = {
        "home_screen": home_screen,
        "accounts_screen": accounts_screen,
        "categories_screen": categories_screen,
        "records_screen": records_screen
    }


    td = TransitionDiagram(root_nodes_list, nodes_dict)


    # create non-root screens
    td.add_node("add_expense_screen", root_screen_node = home_screen, left_node = home_screen)
    td.add_node("add_income_screen", root_screen_node = home_screen, left_node = home_screen)
    td.add_node("add_expense_options_screen", root_screen_node = home_screen, left_node_name = "add_expense_screen")
    td.add_node("add_income_options_screen", root_screen_node = home_screen, left_node_name="add_income_screen")
    td.add_node("edit_transaction_screen", root_screen_node = home_screen, left_node = home_screen)
    td.add_node("edit_transaction_options_screen", root_screen_node = home_screen, left_node_name="edit_transaction_screen")

    td.add_node("add_account_screen", root_screen_node=accounts_screen, left_node=accounts_screen)
    td.add_node("edit_account_screen", root_screen_node=accounts_screen, left_node=accounts_screen)
    td.add_node("choose_account_screen", root_screen_node=accounts_screen, left_node=accounts_screen)

    td.add_node("add_category_screen", root_screen_node = categories_screen, left_node = categories_screen)
    td.add_node("edit_category_screen", root_screen_node = categories_screen, left_node = categories_screen)
    td.add_node("add_subcategory_screen", root_screen_node = categories_screen, left_node_name="edit_category_screen")
    td.add_node("edit_subcategory_screen", root_screen_node = categories_screen, left_node_name="edit_category_screen")


    #  let's test compute_direction
    print(td.compute_direction("home_screen", "accounts_screen"), "Expected: up")
    print(td.compute_direction("accounts_screen", "home_screen"), "Expected: down")
    print(td.compute_direction("home_screen", "categories_screen"), "Expected: up")
    print(td.compute_direction("categories_screen", "home_screen"), "Expected: down")

    print(td.compute_direction("home_screen", "add_expense_screen"), "Expected: left")
    print(td.compute_direction("home_screen", "add_expense_options_screen"), "Expected: left")
    print(td.compute_direction("add_expense_screen", "add_expense_options_screen"), "Expected: left")
    print(td.compute_direction("add_expense_options_screen", "add_expense_screen"), "Expected: right")
    print(td.compute_direction("add_expense_options_screen", "home_screen"), "Expected: right")
    print(td.compute_direction("add_expense_options_screen", "accounts_screen"), "Expected: up")






    



