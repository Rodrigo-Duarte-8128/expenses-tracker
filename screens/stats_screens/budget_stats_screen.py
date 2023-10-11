from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex
from kivy.uix.button import Button
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.button import MDIconButton
from kivymd.uix.datatables import MDDataTable
from datetime import datetime
from datas.date import month_year_to_simple_date, get_date_from_simple_date, last_day
from datas.date import Date
from screens.accounts_screens.choose_account_screen import ChooseAccountScreen
from screens.stats_screens.expenses_stats_screen import ExpensesStatsScreen
from stats.budget import create_current_month_budget
import asyncio



red = hex("#E63946")
cream = hex("#F1FAEE")
light_teal = hex("#A8DADC")
blue = hex("#457B9D")
dark_blue = hex("#1D3557")
green = hex("#84a98c")







class BudgetStatsScreen(MDScreen):
    def __init__(self, app, **kwargs):
        super(BudgetStatsScreen, self).__init__(**kwargs)

        self.window_width, self.window_height = Window.size

        

        self.app = app

        self.displayed_account = None


        self.layout = MDFloatLayout()
        self.date = Date(str(datetime.now()))

        self.displayed_month_year = int(self.date.month), int(self.date.year)

        self.display_date = self.date

        


        self.arrow_right_btn = MDIconButton(
            icon = "arrow-right",
            pos_hint = {"x": 0.8, "y": 0.85},
            size_hint = (0.1, 0.05),
            on_press = self.right_arrow_clicked()
        )
        self.layout.add_widget(self.arrow_right_btn)





        self.displayed_stat_label = MDLabel(
            text = "Budget",
            pos_hint = {"x": 0.2, "y": 0.85},
            size_hint = (0.6, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.displayed_stat_label)


        # account functionality
        self.account_label = MDLabel(
            text = "Account:",
            pos_hint = {"x": 0, "y": 0.775},
            size_hint = (0.5, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.account_label)

        

        default = "Choose Account"
        for account_number in app.accounts_screen.current_account_dict:
            self.displayed_account = app.accounts_screen.current_account_dict[account_number]
            default = f"{self.displayed_account.number}. {self.displayed_account.name}"
            

        self.change_account_btn = Button(
            text=default, 
            color = (1, 1, 1, 1),
            background_color = blue, 
            size_hint=(0.4, 0.05), 
            pos_hint={"x": 0.55, "y": 0.775},
            background_normal = ""
        )
        self.layout.add_widget(self.change_account_btn)
        self.change_account_btn.bind(on_press=self.change_account(app))



        # create month budget
        self.current_month_budget = create_current_month_budget(self.date, self.displayed_account, self.app.recurring_acts_screen.recurring_acts_dict)






        # create month display and change month buttons
        self.previous_month_btn = MDIconButton(
            icon = "arrow-left",
            pos_hint = {"x": 0.1, "y": 0.7125},
            size_hint = (0.1, 0.05),
            on_press = self.previous_month_clicked()
        )
        self.layout.add_widget(self.previous_month_btn)

        self.next_month_btn = MDIconButton(
            icon = "arrow-right",
            pos_hint = {"x": 0.8, "y": 0.7125},
            size_hint = (0.1, 0.05),
            on_press = self.next_month_clicked()
        )
        self.layout.add_widget(self.next_month_btn)


        self.displayed_month_label = MDLabel(
            text = self.displayed_month_to_text(),
            pos_hint = {"x": 0.2, "y": 0.7125},
            size_hint = (0.6, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.displayed_month_label)





        # Create Grid Layout that holds the Scroll View
        self.scroll_layout = MDGridLayout(
            cols=1,
            size_hint_y = None,
            size = (self.window_width, self.window_height * 0.7),
        )
        self.scroll_layout.bind(
            minimum_height=self.scroll_layout.setter("height")
        )
        self.scroll_layout.height = self.scroll_layout.minimum_height




        # Create Scroll View
        self.scroll_view = MDScrollView(
            size_hint = (0.95, 0.7),
            pos_hint = {"x": 0.025, "y": 0},
            bar_width = 10
        )
        self.scroll_view.add_widget(self.scroll_layout)
        self.layout.add_widget(self.scroll_view)
        

    

        self.add_widget(self.layout)



        if self.displayed_account == None:
            return 

        column_data=[
            ("Type", dp(22)),
            ("In", dp(22)),
            ("Out", dp(22)),
        ]

        recurring_income = self.current_month_budget.recurring_income
        if recurring_income == int(recurring_income):
            recurring_income = int(recurring_income)
        
        recurring_expenses = self.current_month_budget.recurring_expenses
        if recurring_expenses == int(recurring_expenses):
            recurring_expenses = int(recurring_expenses)
        
        income = self.current_month_budget.income
        if income == int(income):
            income = int(income)
        
        expenses = self.current_month_budget.expenses
        if expenses == int(expenses):
            expenses = int(expenses)
        
        row_data= [
            (
                "Recurring",
                f"[color=#84a98c]\u20ac{recurring_income}[/color]",
                f"[color=#E63946]\u20ac{recurring_expenses}[/color]"                    
            ),
            (
                "Total",
                f"[color=#84a98c]\u20ac{income}[/color]",
                f"[color=#E63946]\u20ac{expenses}[/color]"
            )
        ]

        self.data_table = MDDataTable(
            height = self.window_height * 0.35,
            size_hint_y = None,
            column_data=column_data,
            row_data=row_data,
            elevation = 0
        )
        self.scroll_layout.add_widget(self.data_table)

        


        # Create budget label
        initial_budget = recurring_income - recurring_expenses
        initial_budget = round(initial_budget, 2)
        if initial_budget == int(initial_budget):
            initial_budget = int(initial_budget)


        self.initial_budget_label_layout = MDFloatLayout(
            size_hint_y = None,
            height = self.window_height * 0.05
        )

        self.initial_budget_label = MDLabel(
            text = f"Initial budget: \u20ac{initial_budget}",
            #color = ,
            size_hint = (0.8, 0.9),
            pos_hint = {"x": 0.1, "y": 0.05}
        )
        self.initial_budget_label_layout.add_widget(self.initial_budget_label)
        self.scroll_layout.add_widget(self.initial_budget_label_layout)

        # Create budget label
        current_budget = income - expenses 
        current_budget = round(current_budget, 2)
        if current_budget == int(current_budget):
            current_budget = int(current_budget)

        
        self.current_budget_label_layout = MDFloatLayout(
            size_hint_y = None,
            height = self.window_height * 0.05
        )

        self.current_budget_label = MDLabel(
            text = f"Current budget: \u20ac{current_budget}",
            #color = ,
            size_hint = (0.8, 0.9),
            pos_hint = {"x": 0.1, "y": 0.05}
        )
        self.current_budget_label_layout.add_widget(self.current_budget_label)
        self.scroll_layout.add_widget(self.current_budget_label_layout)


        # Create progress bar
        self.progress_bar_layout = MDRelativeLayout(
            size_hint_y = None,
            height = self.window_height * 0.05
        )

        self.progress_bar = MDProgressBar(
            value = self.current_month_budget.get_progress_bar_percentage(),
            pos_hint = {"x": 0.1, "y": 0.05},
            size_hint = (0.8, 0.9),
            color = dark_blue,
        )
        self.progress_bar_layout.add_widget(self.progress_bar)
        self.scroll_layout.add_widget(self.progress_bar_layout)

        

        # Create budget label
        info_text = ""
        if recurring_income <= recurring_expenses:
             info_text = f"({round(income - expenses, 2)}/{income})"
        
        else:
            info_text = f"({round(income - expenses, 2)}/{round(recurring_income - recurring_expenses, 2)})"


        self.progress_bar_info_layout = MDRelativeLayout(
            size_hint_y = None,
            height = 0.05 * self.window_height
        )

        self.progress_bar_info = MDLabel(
            text = info_text,
            size_hint = (0.5, 0.9),
            pos_hint = {"x": 0.5, "y": 0.05},
            halign = "center",
        )

        self.progress_bar_info_layout.add_widget(self.progress_bar_info)
        self.scroll_layout.add_widget(self.progress_bar_info_layout)




        # create essentials table
        column_data2=[
            ("Type", dp(33)),
            ("Spent", dp(33)),
        ]

        current_essential_expenses = self.current_month_budget.essential_expenses
        current_non_essential_expenses = self.current_month_budget.non_essentials_expenses
        if current_essential_expenses == int(current_essential_expenses):
            current_essential_expenses = int(current_essential_expenses)
        if current_non_essential_expenses == int(current_non_essential_expenses):
            current_non_essential_expenses = int(current_non_essential_expenses)
        
        row_data2 = [
            (
                "Essential",
                f"\u20ac{current_essential_expenses}",
                                  
            ),
            (
                "Non-essential",
                f"\u20ac{current_non_essential_expenses}",
            )
        ]

        self.data_table2 = MDDataTable(
            height = self.window_height * 0.35,
            size_hint_y = None,
            column_data=column_data2,
            row_data=row_data2,
            elevation = 0
        )
        self.scroll_layout.add_widget(self.data_table2)



        average_essential_expenses = self.current_month_budget.average_essential_expenses
        if average_essential_expenses == int(average_essential_expenses):
            average_essential_expenses = int(average_essential_expenses)


        self.average_essential_expenses_label_layout = MDRelativeLayout(
            size_hint_y = None,
            height = 0.05 * self.window_height
        )

        self.average_essential_expenses_label = MDLabel(
            text = f"Average essential expenses: \u20ac{average_essential_expenses}",
            size_hint = (0.8, 0.9),
            pos_hint = {"x": 0.1, "y": 0.05}
        )
        self.average_essential_expenses_label_layout.add_widget(self.average_essential_expenses_label)

        self.scroll_layout.add_widget(self.average_essential_expenses_label_layout)



        non_essentials_budget = self.current_month_budget.compute_non_essentials_budget()
        if non_essentials_budget == int(non_essentials_budget):
            non_essentials_budget = int(non_essentials_budget)

        self.non_essentials_budget_label_layout = MDRelativeLayout(
            size_hint_y = None,
            height = 0.05*self.window_height
        )

        self.non_essentials_budget_label = MDLabel(
            text = f"Non-essentials budget: \u20ac{non_essentials_budget}",
            size_hint = (0.8, 0.9),
            pos_hint = {"x": 0.1, "y": 0.05}
        )
        self.non_essentials_budget_label_layout.add_widget(self.non_essentials_budget_label)

        self.scroll_layout.add_widget(self.non_essentials_budget_label_layout)










    def previous_month_clicked(self):
        def click(instance):
            # update the displayed month and refresh the row widgets
            old_month = self.displayed_month_year[0]
            old_year = self.displayed_month_year[1]
            if old_month == 1:
                new_month = 12
                new_year = old_year - 1
            else:
                new_month = old_month - 1
                new_year = old_year
            
            self.displayed_month_year = (new_month, new_year)
            self.display_date = get_date_from_simple_date(month_year_to_simple_date(last_day(self.displayed_month_year), self.displayed_month_year))

            # update displayed month label
            self.displayed_month_label.text = self.displayed_month_to_text()

            
          

            # update budget
            self.current_month_budget = create_current_month_budget(
                self.display_date,
                self.displayed_account,
                self.app.recurring_acts_screen.recurring_acts_dict
            )

            
            self.refresh_screen()

        return click
    

   

    
    def next_month_clicked(self):
        def click(instance):
            # check if there is a next month, if so then update the displayed month and refresh the row widgets
            if self.displayed_month_year != (int(self.date.month), int(self.date.year)):
                old_month = self.displayed_month_year[0]
                old_year = self.displayed_month_year[1]
                if old_month == 12:
                    new_month = 1
                    new_year = old_year + 1
                else:
                    new_month = old_month + 1
                    new_year = old_year
                
                self.displayed_month_year = (new_month, new_year)
                self.displayed_month_label.text = self.displayed_month_to_text()

                if self.displayed_month_year == (int(self.date.month), int(self.date.year)):
                    self.display_date = self.date
                    
                    
                    self.current_month_budget = create_current_month_budget(
                        self.display_date,
                        self.displayed_account,
                        self.app.recurring_acts_screen.recurring_acts_dict
                    )


                  
                
                else:
                    self.display_date = get_date_from_simple_date(month_year_to_simple_date(last_day(self.displayed_month_year), self.displayed_month_year))

                    self.current_month_budget = create_current_month_budget(
                        self.display_date,
                        self.displayed_account,
                        self.app.recurring_acts_screen.recurring_acts_dict
                    )

                  
                

                self.refresh_screen()
        return click
    




    def displayed_month_to_text(self):
        '''
        takes the displayed month tuple (month_int, year_int) and turns it into the string "month_name year"

        eg (9, 2023) turns into the string "September 2023"
        '''
        calendar = {
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December"
        }

        return f"{calendar[self.displayed_month_year[0]]} {self.displayed_month_year[1]}"




    def right_arrow_clicked(self):
        def click(instance):
            if "expenses_stats_screen" not in self.app.screen_manager.screen_names:
                self.app.expenses_stats_screen = ExpensesStatsScreen(self.app, name="expenses_stats_screen")
                self.app.screen_manager.add_widget(self.app.expenses_stats_screen)

                self.app.transition_diagram.add_node("expenses_stats_screen", root_screen_node = self.app.budget_stats_screen_node, left_node = self.app.budget_stats_screen_node)

            self.app.switch_screen("expenses_stats_screen")(instance)
        return click
    




    def change_account(self, app):
        def change(instance):
            app.choose_account_screen = ChooseAccountScreen(app, "budget_stats_screen", instance, name="choose_account_screen")
            app.screen_manager.add_widget(app.choose_account_screen)

            # add screen to transition diagram
            app.transition_diagram.add_node("choose_account_screen", root_screen_node = app.budget_stats_screen_node, left_node = app.budget_stats_screen_node)

            app.switch_screen("choose_account_screen")(instance)
        return change
    



    def refresh_screen(self):


        self.layout.remove_widget(self.scroll_view)

        if self.displayed_account == None:
            return




        # Create Grid Layout that holds the Scroll View
        self.scroll_layout = MDGridLayout(
            cols=1,
            size_hint_y = None,
            size = (self.window_width, self.window_height * 0.7),
        )
        self.scroll_layout.bind(
            minimum_height=self.scroll_layout.setter("height")
        )
        self.scroll_layout.height = self.scroll_layout.minimum_height


        # self.scroll_layout.add_widget(self.budget_card)
        # self.scroll_layout.add_widget(self.chart_card)
        # self.scroll_layout.add_widget(self.yearly_net_income_card)


        column_data=[
            ("Type", dp(22)),
            ("In", dp(22)),
            ("Out", dp(22)),
        ]

        recurring_income = self.current_month_budget.recurring_income
        if recurring_income == int(recurring_income):
            recurring_income = int(recurring_income)
        
        recurring_expenses = self.current_month_budget.recurring_expenses
        if recurring_expenses == int(recurring_expenses):
            recurring_expenses = int(recurring_expenses)
        
        income = self.current_month_budget.income
        if income == int(income):
            income = int(income)
        
        expenses = self.current_month_budget.expenses
        if expenses == int(expenses):
            expenses = int(expenses)
        
        row_data= [
            (
                "Recurring",
                f"[color=#84a98c]\u20ac{recurring_income}[/color]",
                f"[color=#E63946]\u20ac{recurring_expenses}[/color]"                    
            ),
            (
                "Total",
                f"[color=#84a98c]\u20ac{income}[/color]",
                f"[color=#E63946]\u20ac{expenses}[/color]"
            )
        ]

        self.data_table = MDDataTable(
            height = self.window_height * 0.35,
            size_hint_y = None,
            column_data=column_data,
            row_data=row_data,
            elevation = 0
        )
        self.scroll_layout.add_widget(self.data_table)

        


        # Create budget label
        initial_budget = recurring_income - recurring_expenses
        initial_budget = round(initial_budget, 2)
        if initial_budget == int(initial_budget):
            initial_budget = int(initial_budget)


        self.initial_budget_label_layout = MDFloatLayout(
            size_hint_y = None,
            height = self.window_height * 0.05
        )

        self.initial_budget_label = MDLabel(
            text = f"Initial budget: \u20ac{initial_budget}",
            size_hint = (0.8, 0.9),
            pos_hint = {"x": 0.1, "y": 0.05}
        )
        self.initial_budget_label_layout.add_widget(self.initial_budget_label)
        self.scroll_layout.add_widget(self.initial_budget_label_layout)

        # Create budget label
        current_budget = income - expenses 
        current_budget = round(current_budget, 2)
        if current_budget == int(current_budget):
            current_budget = int(current_budget)

        
        self.current_budget_label_layout = MDFloatLayout(
            size_hint_y = None,
            height = self.window_height * 0.05
        )

        self.current_budget_label = MDLabel(
            text = f"Current budget: \u20ac{current_budget}",
            size_hint = (0.8, 0.9),
            pos_hint = {"x": 0.1, "y": 0.05}
        )
        self.current_budget_label_layout.add_widget(self.current_budget_label)
        self.scroll_layout.add_widget(self.current_budget_label_layout)


        # Create progress bar
        self.progress_bar_layout = MDRelativeLayout(
            size_hint_y = None,
            height = self.window_height * 0.05
        )

        self.progress_bar = MDProgressBar(
            value = self.current_month_budget.get_progress_bar_percentage(),
            pos_hint = {"x": 0.1, "y": 0.05},
            size_hint = (0.8, 0.9),
            color = dark_blue,
        )
        self.progress_bar_layout.add_widget(self.progress_bar)
        self.scroll_layout.add_widget(self.progress_bar_layout)

        

        # Create budget label
        info_text = ""
        if recurring_income <= recurring_expenses:
             info_text = f"({round(income - expenses, 2)}/{income})"
        
        else:
            info_text = f"({round(income - expenses, 2)}/{round(recurring_income - recurring_expenses, 2)})"


        self.progress_bar_info_layout = MDRelativeLayout(
            size_hint_y = None,
            height = 0.05 * self.window_height
        )

        self.progress_bar_info = MDLabel(
            text = info_text,
            size_hint = (0.5, 0.9),
            pos_hint = {"x": 0.5, "y": 0.05},
            halign = "center",
        )

        self.progress_bar_info_layout.add_widget(self.progress_bar_info)
        self.scroll_layout.add_widget(self.progress_bar_info_layout)




        # create essentials table
        column_data2=[
            ("Type", dp(33)),
            ("Spent", dp(33)),
        ]

        current_essential_expenses = self.current_month_budget.essential_expenses
        current_non_essential_expenses = self.current_month_budget.non_essentials_expenses
        if current_essential_expenses == int(current_essential_expenses):
            current_essential_expenses = int(current_essential_expenses)
        if current_non_essential_expenses == int(current_non_essential_expenses):
            current_non_essential_expenses = int(current_non_essential_expenses)
        
        row_data2 = [
            (
                "Essential",
                f"\u20ac{current_essential_expenses}",
                                  
            ),
            (
                "Non-essential",
                f"\u20ac{current_non_essential_expenses}",
            )
        ]

        self.data_table2 = MDDataTable(
            height = self.window_height * 0.35,
            size_hint_y = None,
            column_data=column_data2,
            row_data=row_data2,
            elevation = 0
        )
        self.scroll_layout.add_widget(self.data_table2)



        average_essential_expenses = self.current_month_budget.average_essential_expenses
        if average_essential_expenses == int(average_essential_expenses):
            average_essential_expenses = int(average_essential_expenses)


        self.average_essential_expenses_label_layout = MDRelativeLayout(
            size_hint_y = None,
            height = 0.05 * self.window_height
        )

        self.average_essential_expenses_label = MDLabel(
            text = f"Average essential expenses: \u20ac{average_essential_expenses}",
            size_hint = (0.8, 0.9),
            pos_hint = {"x": 0.1, "y": 0.05}
        )
        self.average_essential_expenses_label_layout.add_widget(self.average_essential_expenses_label)

        self.scroll_layout.add_widget(self.average_essential_expenses_label_layout)



        non_essentials_budget = self.current_month_budget.compute_non_essentials_budget()
        if non_essentials_budget == int(non_essentials_budget):
            non_essentials_budget = int(non_essentials_budget)

        self.non_essentials_budget_label_layout = MDRelativeLayout(
            size_hint_y = None,
            height = 0.05*self.window_height
        )

        self.non_essentials_budget_label = MDLabel(
            text = f"Non-essentials budget: \u20ac{non_essentials_budget}",
            size_hint = (0.8, 0.9),
            pos_hint = {"x": 0.1, "y": 0.05}
        )
        self.non_essentials_budget_label_layout.add_widget(self.non_essentials_budget_label)

        self.scroll_layout.add_widget(self.non_essentials_budget_label_layout)


        


        # Create Scroll View
        self.scroll_view = MDScrollView(
            size_hint = (0.95, 0.7),
            pos_hint = {"x": 0.025, "y": 0},
            bar_width = 10
        )
        self.scroll_view.add_widget(self.scroll_layout)
        self.layout.add_widget(self.scroll_view)