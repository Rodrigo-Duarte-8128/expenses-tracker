from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex
from kivy.uix.button import Button
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from datetime import datetime
from datas.date import Date, get_date_from_simple_date, last_day, month_year_to_simple_date
from screens.accounts_screens.choose_account_screen import ChooseAccountScreen
from screens.stats_screens.net_income_stats_screen import NetIncomeStatsScreen
from stats.expenses import ExpensesStats
from row_widgets.expenses_stats_row_widget import ExpensesStatsRowWidget



red = hex("#E63946")
cream = hex("#F1FAEE")
light_teal = hex("#A8DADC")
blue = hex("#457B9D")
dark_blue = hex("#1D3557")
green = hex("#84a98c")


class ExpensesStatsScreen(MDScreen):
    def __init__(self, app, **kwargs):
        super(ExpensesStatsScreen, self).__init__(**kwargs)

        

        self.app = app

        self.displayed_account = None

        self.date = Date(str(datetime.now()))


        self.displayed_month_year = int(self.date.month), int(self.date.year)

        self.display_date = self.date


        self.window_width, self.window_height = Window.size

        self.row_widgets_list = []


        self.layout = MDFloatLayout()



        # create month display and change month buttons
        self.arrow_left_btn = MDIconButton(
            icon = "arrow-left",
            pos_hint = {"x": 0.1, "y": 0.85},
            size_hint = (0.1, 0.05),
            on_press = self.left_arrow_clicked()
        )
        self.layout.add_widget(self.arrow_left_btn)


        self.arrow_right_btn = MDIconButton(
            icon = "arrow-right",
            pos_hint = {"x": 0.8, "y": 0.85},
            size_hint = (0.1, 0.05),
            on_press = self.right_arrow_clicked()
        )
        self.layout.add_widget(self.arrow_right_btn)

        


        self.displayed_stat_label = MDLabel(
            text = "Expenses",
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



        # create month display and change month buttons
        self.previous_month_btn = MDIconButton(
            icon = "arrow-left",
            pos_hint = {"x": 0.1, "y": 0.7125},
            size_hint = (0.1, 0.03),
            on_press = self.previous_month_clicked()
        )
        self.layout.add_widget(self.previous_month_btn)

        self.next_month_btn = MDIconButton(
            icon = "arrow-right",
            pos_hint = {"x": 0.8, "y": 0.7125},
            size_hint = (0.1, 0.03),
            on_press = self.next_month_clicked()
        )
        self.layout.add_widget(self.next_month_btn)


        self.displayed_month_label = MDLabel(
            text = self.displayed_month_to_text(),
            pos_hint = {"x": 0.2, "y": 0.7125},
            size_hint = (0.6, 0.03),
            halign = "center"
        )
        self.layout.add_widget(self.displayed_month_label)



         


        self.expenses_stats = ExpensesStats(self.date, self.displayed_account, self.app.recurring_acts_screen.recurring_acts_dict)


        # Create Grid Layout that holds the Scroll View
        self.scroll_layout = MDGridLayout(
            cols=1,
            size_hint_y = None,
            size = (self.window_width, self.window_height * 0.65),
        )
        self.scroll_layout.bind(
            minimum_height=self.scroll_layout.setter("height")
        )
        self.scroll_layout.height = self.scroll_layout.minimum_height


        # Create Scroll View
        self.scroll_view = MDScrollView(
            size_hint = (1, 0.65),
            pos_hint = {"x": 0, "y": 0.},
            bar_width = 10
        )
        self.scroll_view.add_widget(self.scroll_layout)
        self.layout.add_widget(self.scroll_view)







        self.add_widget(self.layout)
        if self.displayed_account == None:
            self.total_expenses_label = MDLabel(
                bold = True,
                text = f"Total Expenses: ",
                pos_hint = {"x": 0, "y": 0.66625},
                size_hint = (1, 0.03),
                halign = "center"
            )
            self.layout.add_widget(self.total_expenses_label)
            return 
            
        



        # show total expenses
        total_expenses = self.expenses_stats.get_total_expenses()
        if total_expenses == int(total_expenses):
            total_expenses = int(total_expenses)

        self.total_expenses_label = MDLabel(
            bold = True,
            text = f"Total Expenses: \u20ac{total_expenses}",
            pos_hint = {"x": 0, "y": 0.66625},
            size_hint = (1, 0.03),
            halign = "center"
        )
        self.layout.add_widget(self.total_expenses_label)






        self.category_expenses_list = [
            (category, self.expenses_stats.get_category_expenses(category, None)) for category in self.app.categories_screen.categories_dict.values() if category.kind == "Expense"
            ]
        self.category_expenses_list.sort(key=lambda x: x[1], reverse=True)

        for category, _ in self.category_expenses_list:
            
            row = ExpensesStatsRowWidget(
                self.expenses_stats,
                category,
                None
            )
            row.category_name_btn.bind(on_release=self.category_clicked(category))
            self.scroll_layout.add_widget(row)
            self.row_widgets_list.append(row)

       






    def category_clicked(self, category):
        def click(instance):
            
            # remove current row_widgets
            for row in self.row_widgets_list:
                self.scroll_layout.remove_widget(row)

            self.row_widgets_list = []



            subcategories_list = [
                (subcategory_name, self.expenses_stats.get_category_expenses(category, category.subcategories[subcategory_name])) for subcategory_name in category.subcategories
            ]
            subcategories_list.sort(key=lambda x: x[1], reverse=True)

            for subcategory_name, _ in subcategories_list:
                sub_row = ExpensesStatsRowWidget(
                    self.expenses_stats,
                    category,
                    category.subcategories[subcategory_name]
                )
                sub_row.category_name_btn.bind(on_release=self.subcategory_clicked())
                self.scroll_layout.add_widget(sub_row)
                self.row_widgets_list.append(sub_row)
            

        return click
    

    


    def subcategory_clicked(self):
        def click(instance):
            # remove current row_widgets
            for sub_row in self.row_widgets_list:
                self.scroll_layout.remove_widget(sub_row)

            self.row_widgets_list = []



            for category, _ in self.category_expenses_list:
                
                row = ExpensesStatsRowWidget(
                    self.expenses_stats,
                    category,
                    None
                )
                row.category_name_btn.bind(on_release=self.category_clicked(category))
                self.scroll_layout.add_widget(row)
                self.row_widgets_list.append(row)



        return click
        











        



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


            # update expenses stats
            self.expenses_stats = ExpensesStats(
                self.display_date,
                self.displayed_account,
                self.app.recurring_acts_screen.recurring_acts_dict
            )

            
            self.refresh_screen()
            
        return click
    


    

    def refresh_screen(self):

        # remove rows from screen
        for row in self.row_widgets_list:
            self.scroll_layout.remove_widget(row)

        self.row_widgets_list = []

        

        if self.displayed_account == None:
            return 
        
        # update total expenses
        total_expenses = self.expenses_stats.get_total_expenses()
        if total_expenses == int(total_expenses):
            total_expenses = int(total_expenses)

        self.total_expenses_label.text = f"Total Expenses: \u20ac{self.expenses_stats.get_total_expenses()}"

        

        # rebuild row widgets
        category_expenses_list = [
            (category, self.expenses_stats.get_category_expenses(category, None)) for category in self.app.categories_screen.categories_dict.values() if category.kind == "Expense"
            ]
        category_expenses_list.sort(key=lambda x: x[1], reverse=True)

        for category, _ in category_expenses_list:
            
            row = ExpensesStatsRowWidget(
                self.expenses_stats,
                category,
                None
            )
            row.category_name_btn.bind(on_release=self.category_clicked(category))
            self.scroll_layout.add_widget(row)
            self.row_widgets_list.append(row)

            






    
    


    
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

                    self.expenses_stats = ExpensesStats(
                        self.date,
                        self.displayed_account,
                        self.app.recurring_acts_screen.recurring_acts_dict
                    )
                
                else:
                    self.display_date = get_date_from_simple_date(month_year_to_simple_date(last_day(self.displayed_month_year), self.displayed_month_year))
                    
                    self.expenses_stats = ExpensesStats(
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




    def left_arrow_clicked(self):
        def click(instance):
            self.app.switch_screen("budget_stats_screen")(instance)
            
        return click
    

    def right_arrow_clicked(self):
        def click(instance):
            if "net_income_stats_screen" not in self.app.screen_manager.screen_names:
                self.app.net_income_stats_screen = NetIncomeStatsScreen(self.app, name="net_income_stats_screen")
                self.app.screen_manager.add_widget(self.app.net_income_stats_screen)

                self.app.transition_diagram.add_node("net_income_stats_screen", root_screen_node = self.app.budget_stats_screen_node, left_node_name = "expenses_stats_screen")

            self.app.switch_screen("net_income_stats_screen")(instance)
        return click



    def change_account(self, app):
        def change(instance):
            app.choose_account_screen = ChooseAccountScreen(app, "expenses_stats_screen", instance, name="choose_account_screen")
            app.screen_manager.add_widget(app.choose_account_screen)

            # add screen to transition diagram
            app.transition_diagram.add_node("choose_account_screen", root_screen_node = app.budget_stats_screen_node, left_node_name = "expenses_stats_screen")

            app.switch_screen("choose_account_screen")(instance)
        return change




