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
from kivymd.uix.button import MDIconButton
from kivymd.uix.datatables import MDDataTable
from datetime import datetime
from datas.date import month_year_to_simple_date, get_date_from_simple_date, last_day
from datas.date import Date
from screens.accounts_screens.choose_account_screen import ChooseAccountScreen
from stats.net_income import create_net_income_stats
import asyncio


red = hex("#E63946")
cream = hex("#F1FAEE")
light_teal = hex("#A8DADC")
blue = hex("#457B9D")
dark_blue = hex("#1D3557")
green = hex("#84a98c")


class NetIncomeStatsScreen(MDScreen):
    def __init__(self, app, **kwargs):
        super(NetIncomeStatsScreen, self).__init__(**kwargs)

        self.window_width, self.window_height = Window.size


        self.app = app

        self.displayed_account = None


        self.layout = MDFloatLayout()
        self.date = Date(str(datetime.now()))

        self.displayed_month_year = int(self.date.month), int(self.date.year)

        self.display_date = self.date

        




        
        self.arrow_left_btn = MDIconButton(
            icon = "arrow-left",
            pos_hint = {"x": 0.1, "y": 0.85},
            size_hint = (0.1, 0.05),
            on_press = self.left_arrow_clicked()
        )
        self.layout.add_widget(self.arrow_left_btn)


        self.displayed_stat_label = MDLabel(
            text = "Net Income History",
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


        # create net_income_stats
        
        self.net_income_stats = create_net_income_stats(self.display_date, self.displayed_account)






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
        



        
        calendar = {
            1: "Jan",
            2: "Feb",
            3: "Mar",
            4: "Apr",
            5: "May",
            6: "Jun",
            7: "Jul",
            8: "Aug",
            9: "Sep",
            10: "Oct",
            11: "Nov",
            12: "Dec"
        }

        past_month_year_list = [] # list of past 5 months
        month_year = self.displayed_month_year
        for _ in range(5):
            if month_year[0] == 1:
                month_year = (12, month_year[1] - 1)
            else:
                month_year = (month_year[0] - 1, month_year[1])

            past_month_year_list.append((month_year[0], month_year[1]))


        past_net_income = [self.net_income_stats.months_net_income[month_year] for month_year in past_month_year_list]
        

        past_months = [calendar[x[0]] for x in past_month_year_list]


        column_data=[
            ("Month", dp(33)),
            ("Net Income", dp(33)),
        ]

        row_data = [
            (
                past_months[index],
                f"[color=#84a98c]\u20ac{past_net_income[index]}[/color]" if past_net_income[index] >= 0 else f"[color=#E63946]\u20ac{past_net_income[index]}[/color]"
            )
            for index in range(5)
        ]
        
    
        self.data_table = MDDataTable(
            height = self.window_height * 0.5,
            size_hint_y = None,
            column_data=column_data,
            row_data=row_data,
            elevation = 0
        )
        self.scroll_layout.add_widget(self.data_table)






        # Create year net income label
        net_income_text = ""
        value = self.net_income_stats.current_year_net_income     
        if value == int(value):
            net_income_text = f"Yearly Net Income: \u20ac{int(value)}"
        else:
            net_income_text = f"Yearly Net Income: \u20ac{value}"

        self.yearly_net_income_label_layout = MDRelativeLayout(
            size_hint_y = None,
            height = self.window_height * 0.05
        )

        self.yearly_net_income_label = MDLabel(
            text = net_income_text,
            size_hint = (0.8, 0.9),
            pos_hint = {"x": 0.1, "y": 0.05}
        )
        self.yearly_net_income_label_layout.add_widget(self.yearly_net_income_label)
        self.scroll_layout.add_widget(self.yearly_net_income_label_layout)

       
        


        past_years_list = [(int(self.displayed_month_year[1])) - i for i in range(1, 6)] # list of past 5 years

        past_incomes_list = [self.net_income_stats.years_net_income[past_year] for past_year in past_years_list]


        column_data=[
            ("Year", dp(33)),
            ("Net Income", dp(33)),
        ]

        row_data = [
            (
                past_years_list[index],
                f"[color=#84a98c]\u20ac{past_incomes_list[index]}[/color]" if past_incomes_list[index] >= 0 else f"[color=#E63946]\u20ac{past_incomes_list[index]}[/color]"
            )
            for index in range(5)
        ]
        
    
        self.data_table = MDDataTable(
            size_hint_y = None,
            height = self.window_height * 0.5,
            column_data=column_data,
            row_data=row_data,
            elevation = 0
        )
        self.scroll_layout.add_widget(self.data_table)










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

            
          

            # update net_income_stats
            self.net_income_stats = create_net_income_stats(self.display_date, self.displayed_account)
            
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
                    
                    self.net_income_stats = create_net_income_stats(self.display_date, self.displayed_account)
                    
                
                else:
                    self.display_date = get_date_from_simple_date(month_year_to_simple_date(last_day(self.displayed_month_year), self.displayed_month_year))

                    self.net_income_stats = create_net_income_stats(self.display_date, self.displayed_account)

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




    
    def left_arrow_clicked(self):
        def click(instance):
            # move to expenses_stats_screen
            self.app.switch_screen("expenses_stats_screen")(instance)
        return click




    def change_account(self, app):
        def change(instance):
            app.choose_account_screen = ChooseAccountScreen(app, "net_income_stats_screen", instance, name="choose_account_screen")
            app.screen_manager.add_widget(app.choose_account_screen)

            # add screen to transition diagram
            app.transition_diagram.add_node("choose_account_screen", root_screen_node = app.budget_stats_screen_node, left_node_name = "net_income_stats_screen")

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




        # Create Scroll View
        self.scroll_view = MDScrollView(
            size_hint = (0.95, 0.7),
            pos_hint = {"x": 0.025, "y": 0},
            bar_width = 10
        )
        self.scroll_view.add_widget(self.scroll_layout)
        self.layout.add_widget(self.scroll_view)


        calendar = {
            1: "Jan",
            2: "Feb",
            3: "Mar",
            4: "Apr",
            5: "May",
            6: "Jun",
            7: "Jul",
            8: "Aug",
            9: "Sep",
            10: "Oct",
            11: "Nov",
            12: "Dec"
        }

        past_month_year_list = [] # list of past 5 months
        month_year = self.displayed_month_year
        for _ in range(5):
            if month_year[0] == 1:
                month_year = (12, month_year[1] - 1)
            else:
                month_year = (month_year[0] - 1, month_year[1])

            past_month_year_list.append((month_year[0], month_year[1]))


        past_net_income = [self.net_income_stats.months_net_income[month_year] for month_year in past_month_year_list]
        

        past_months = [calendar[x[0]] for x in past_month_year_list]


        column_data=[
            ("Month", dp(33)),
            ("Net Income", dp(33)),
        ]

        row_data = [
            (
                past_months[index],
                f"[color=#84a98c]\u20ac{past_net_income[index]}[/color]" if past_net_income[index] >= 0 else f"[color=#E63946]\u20ac{past_net_income[index]}[/color]"
            )
            for index in range(5)
        ]
        
    
        self.data_table = MDDataTable(
            height = self.window_height * 0.5,
            size_hint_y = None,
            column_data=column_data,
            row_data=row_data,
            elevation = 0
        )
        self.scroll_layout.add_widget(self.data_table)






        # Create year net income label
        net_income_text = ""
        value = self.net_income_stats.current_year_net_income     
        if value == int(value):
            net_income_text = f"Yearly Net Income: \u20ac{int(value)}"
        else:
            net_income_text = f"Yearly Net Income: \u20ac{value}"

        self.yearly_net_income_label_layout = MDRelativeLayout(
            size_hint_y = None,
            height = self.window_height * 0.05
        )

        self.yearly_net_income_label = MDLabel(
            text = net_income_text,
            size_hint = (0.8, 0.9),
            pos_hint = {"x": 0.1, "y": 0.05}
        )
        self.yearly_net_income_label_layout.add_widget(self.yearly_net_income_label)
        self.scroll_layout.add_widget(self.yearly_net_income_label_layout)

       
        


        past_years_list = [(int(self.displayed_month_year[1])) - i for i in range(1, 6)] # list of past 5 years

        past_incomes_list = [self.net_income_stats.years_net_income[past_year] for past_year in past_years_list]


        column_data=[
            ("Year", dp(33)),
            ("Net Income", dp(33)),
        ]

        row_data = [
            (
                past_years_list[index],
                f"[color=#84a98c]\u20ac{past_incomes_list[index]}[/color]" if past_incomes_list[index] >= 0 else f"[color=#E63946]\u20ac{past_incomes_list[index]}[/color]"
            )
            for index in range(5)
        ]
        
    
        self.data_table = MDDataTable(
            size_hint_y = None,
            height = self.window_height * 0.5,
            column_data=column_data,
            row_data=row_data,
            elevation = 0
        )
        self.scroll_layout.add_widget(self.data_table)