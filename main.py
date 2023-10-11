from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex
from kivymd.app import MDApp 
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.navigationdrawer import MDNavigationLayout
from kivymd.uix.screen import MDScreen
from navigation.navigation_drawer import MyDrawer
from navigation.transition_diagram import TransitionDiagram, ScreenNode
from screens.home_screen import HomeScreen
from screens.category_screens.categories_screen import CategoriesScreen
from screens.accounts_screens.accounts_screen import AccountsScreen
from screens.records_screen import RecordsScreen
from screens.recurring_acts_screen import RecurringActsScreen



# #RATIO = 16/9
# RATIO = 20/9

# #window config for pc
# WIDTH = 400
# Window.size = (WIDTH, RATIO * WIDTH)
# Window.top = 100
# Window.left = 1500

# # window config for laptop
# WIDTH = 400
# Window.size = (WIDTH, 20 * WIDTH / 9)
# Window.top = 50
# Window.left = 800

red = hex("#E63946")
cream = hex("#F1FAEE")
light_teal = hex("#A8DADC")
blue = hex("#457B9D")
dark_blue = hex("#1D3557")


class ExpensesTrackerApp(MDApp):
    def build(self):
        self.theme_cls.material_style = "M3"
        

        Window.clearcolor = cream
        

        self.main_screen = MDScreen(name="main_screen")

        # create toolbar
        self.toolbar = MDTopAppBar(
            title="Expenses Tracker",
            #anchor_title = "center",
            elevation=4,
            pos_hint={"top": 1},
            md_bg_color = dark_blue,
            #specific_text_color="#4a4939",
            left_action_items=[
                ['menu', lambda x: self.nav_drawer_open()]
            ],
        )
        self.main_screen.add_widget(self.toolbar)


        # create navigation layout that sits below the toolbar
        self.navigation = MDNavigationLayout()
        self.main_screen.add_widget(self.navigation)

        # the navigation layout has two children - the screen manager and the navigation drawer
        self.screen_manager = MDScreenManager()

        self.navigation.add_widget(self.screen_manager)

        self.nav_drawer = MyDrawer(self)
        self.navigation.add_widget(self.nav_drawer)


        # create screens
        

        self.categories_screen = CategoriesScreen(self, name="categories_screen")
        self.screen_manager.add_widget(self.categories_screen)
        
        self.accounts_screen = AccountsScreen(self, name="accounts_screen")
        self.screen_manager.add_widget(self.accounts_screen)
        

        self.recurring_acts_screen = RecurringActsScreen(self, name="recurring_acts_screen")
        self.screen_manager.add_widget(self.recurring_acts_screen)

        self.records_screen = RecordsScreen(self, name="records_screen")
        self.screen_manager.add_widget(self.records_screen)

        

        self.home_screen = HomeScreen(self, name="home_screen")
        self.screen_manager.add_widget(self.home_screen)
        self.screen_manager.current = "home_screen"

        

        # create root_screens
        self.home_screen_node = ScreenNode("home_screen_node")
        self.accounts_screen_node = ScreenNode("accounts_screen_node")
        self.categories_screen_node = ScreenNode("categories_screen_node")
        self.records_screen_node = ScreenNode("records_screen_node")
        self.recurring_acts_screen_node = ScreenNode("recurring_acts_screen_node")
        self.budget_stats_screen_node = ScreenNode("budget_stats_screen_node")
        
        root_nodes_list = [
            self.home_screen_node, 
            self.records_screen_node,
            self.budget_stats_screen_node,
            self.recurring_acts_screen_node,
            self.accounts_screen_node,
            self.categories_screen_node,
        ]

        nodes_dict = {
            "home_screen": self.home_screen_node,
            "accounts_screen": self.accounts_screen_node,
            "categories_screen": self.categories_screen_node,
            "records_screen": self.records_screen_node,
            "recurring_acts_screen": self.recurring_acts_screen_node,
            "budget_stats_screen": self.budget_stats_screen_node
        }

        # create transition diagram
        self.transition_diagram = TransitionDiagram(root_nodes_list, nodes_dict)


        return self.main_screen
    

    def nav_drawer_open(self, *args):
        self.nav_drawer.set_state("open")


    def switch_screen(self, screen_name):
        def switch(instance_list_item):

            current_screen = self.screen_manager.current

            

            self.screen_manager.transition.direction = self.transition_diagram.compute_direction(current_screen, screen_name)

            self.screen_manager.current = screen_name
            self.nav_drawer.set_state("close")


        return switch
        
        



if __name__ == "__main__":
    ExpensesTrackerApp().run()
