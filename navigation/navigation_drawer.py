from kivy.utils import get_color_from_hex as hex
from kivymd.uix.navigationdrawer import (
    MDNavigationDrawer,
    MDNavigationDrawerMenu,
    MDNavigationDrawerDivider,
    MDNavigationDrawerItem,
)
from screens.stats_screens.budget_stats_screen import BudgetStatsScreen
import asyncio

light_grey = hex("#e0e0e0")



class ClickableItem(MDNavigationDrawerItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.radius = 24

        self.text_color = "#4a4939"
        self.icon_color = "#4a4939"

        self.focus_color = light_grey
        self.ripple_color = light_grey
        self.selected_color = light_grey



class MyDrawer(MDNavigationDrawer):
    def __init__(self, app, **kwargs):
        super(MyDrawer, self).__init__(**kwargs)

        self.app = app

        self.radius = (0, 16, 16, 0)


        self.menu = MDNavigationDrawerMenu()



        self.home_item = ClickableItem(
            text="Home",
            icon = "home",
            
            on_press = self.nav_drawer_btn_clicked("home_screen")
        )
        self.menu.add_widget(self.home_item)


        self.records_item = ClickableItem(
            text="Records",
            icon = "folder-multiple",
            on_press = self.nav_drawer_btn_clicked("records_screen")
        )
        self.menu.add_widget(self.records_item)


        self.div1 = MDNavigationDrawerDivider()
        self.menu.add_widget(self.div1)


        self.stats_item = ClickableItem(
            text = "Stats",
            icon = "chart-bar",
            on_press = self.stats_screen_btn_clicked()
        )
        self.menu.add_widget(self.stats_item)


        self.div2 = MDNavigationDrawerDivider()
        self.menu.add_widget(self.div2)


        self.recurring_acts_item = ClickableItem(
            text = "Recurring Acts",
            icon = "credit-card-sync",
            on_press = self.nav_drawer_btn_clicked("recurring_acts_screen")
        )
        self.menu.add_widget(self.recurring_acts_item)

        self.div3 = MDNavigationDrawerDivider()
        self.menu.add_widget(self.div3)



        self.accounts_item = ClickableItem(
            text = "Accounts",
            icon = "credit-card-multiple",
            on_press = self.nav_drawer_btn_clicked("accounts_screen")
        )
        self.menu.add_widget(self.accounts_item)



        self.categories_item = ClickableItem(
            text = "Categories",
            icon = "format-list-bulleted",
            on_press = self.nav_drawer_btn_clicked("categories_screen")
        )
        self.menu.add_widget(self.categories_item)


        self.wanted_screens = [    
            "categories_screen",
            "accounts_screen",
            "records_screen",
            "home_screen",
            "recurring_acts_screen"
        ]

        self.wanted_screen_nodes = [
            "home_screen",
            "accounts_screen",
            "categories_screen",
            "records_screen",
            "recurring_acts_screen",
            "budget_stats_screen"
        ]




        self.add_widget(self.menu)



  
    


    def stats_screen_btn_clicked(self):
        def click(instance):
            if "budget_stats_screen" in map(lambda x: x.name, self.app.screen_manager.screens):
                self.app.screen_manager.remove_widget(self.app.budget_stats_screen)
            self.app.budget_stats_screen = BudgetStatsScreen(self.app, name="budget_stats_screen")
            self.app.screen_manager.add_widget(self.app.budget_stats_screen)
            self.wanted_screens.append("budget_stats_screen")

            self.app.switch_screen("budget_stats_screen")(instance)


            for screen in self.app.screen_manager.screens:
                if screen.name not in self.wanted_screens:
                    self.app.screen_manager.remove_widget(screen)

            node_names_list = list(self.app.transition_diagram.nodes_dict.keys())
            for screen_node_name in node_names_list:
                if screen_node_name not in self.wanted_screen_nodes:
                    self.app.transition_diagram.remove_node(screen_node_name)
        return click

     
   


    def nav_drawer_btn_clicked(self, screen_name):
        def click(instance):
            
                

            self.app.switch_screen(screen_name)(instance)



            for screen in self.app.screen_manager.screens:
                if screen.name not in self.wanted_screens:
                    self.app.screen_manager.remove_widget(screen)

            node_names_list = list(self.app.transition_diagram.nodes_dict.keys())
            for screen_node_name in node_names_list:
                if screen_node_name not in self.wanted_screen_nodes:
                    self.app.transition_diagram.remove_node(screen_node_name)


        return click