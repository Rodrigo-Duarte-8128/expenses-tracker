from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from row_widgets.account_row_widget import AccountRowWidget
from stats.budget import create_current_month_budget
from stats.expenses import ExpensesStats
from stats.net_income import create_net_income_stats



red = hex("#E63946")
cream = hex("#F1FAEE")
light_teal = hex("#A8DADC")
blue = hex("#457B9D")
dark_blue = hex("#1D3557")
green = hex("#84a98c")



class ChooseAccountScreen(MDScreen):
    def __init__(self, app, target_screen_name, target_btn, **kwargs):
        super(ChooseAccountScreen, self).__init__(**kwargs)

        self.app = app
        self.target_screen_name = target_screen_name
        self.target_btn = target_btn

        
        self.layout = MDFloatLayout()

        self.window_width, self.window_height = Window.size

        

        # Create Grid Layout that holds the Scroll View
        self.scroll_layout = MDGridLayout(
            cols=1,
            size_hint_y = None,
            size = (self.window_width, self.window_height * 0.75),
        )
        self.scroll_layout.bind(
            minimum_height=self.scroll_layout.setter("height")
        )
        self.scroll_layout.height = self.scroll_layout.minimum_height

        # build accounts dictionary from storage, build row_widgets and scroll view
        self.row_widgets = {}
        
        account_numbers_list = list(app.accounts_screen.accounts_dict.keys())
        account_numbers_list.sort()

        for account_number in account_numbers_list:
            account = app.accounts_screen.accounts_dict[account_number]
            
            row = AccountRowWidget(account)

            # create edit account btn functionality
            row.account_name_btn.bind(on_press=self.account_pressed(account))

            
            self.row_widgets[account_number] = row
            self.scroll_layout.add_widget(row)

        
    
        # Create Scroll View
        self.scroll_view = MDScrollView(
            size_hint = (1, 0.75),
            pos_hint = {"x": 0, "y": 0.05},
            bar_width = 10
        )
        self.scroll_view.add_widget(self.scroll_layout)
        self.layout.add_widget(self.scroll_view)
        

        

        
        # Create label for the categories list
        self.accounts_label = MDLabel(
            text = "Choose Account",
            pos_hint = {"x": 0.3, "y": 0.85},
            size_hint = (0.4, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.accounts_label)




        # Create Categories Scroll View Headers
        self.account_number_label = MDRaisedButton(
            text = "No.",
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            md_bg_color_disabled = blue,
            size_hint = (0.2, 0.05),
            pos_hint = {"x": 0, "y": 0.8},
            elevation = 0,
            _radius = 1
        )
        self.layout.add_widget(self.account_number_label)

        self.account_name_label = MDRaisedButton(
            text = "Account Name",
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            md_bg_color_disabled = blue,
            size_hint = (0.5, 0.05),
            pos_hint = {"x": 0.2, "y": 0.8},
            elevation = 0,
            _radius = 1
        )
        self.layout.add_widget(self.account_name_label)

        self.account_total_label = MDRaisedButton(
            text = "Total",
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            md_bg_color_disabled = blue,
            size_hint = (0.3, 0.05),
            pos_hint = {"x": 0.7, "y": 0.8},
            elevation = 0,
            _radius = 0
        )
        self.layout.add_widget(self.account_total_label)




        self.none_btn = MDRaisedButton(
            text = "None",
            md_bg_color = dark_blue,
            size_hint = (0.4, 0.05),
            pos_hint = {"x": 0.3, "y": 0.06},
            on_press = self.none_clicked(app)
        )
        self.layout.add_widget(self.none_btn)


        self.add_widget(self.layout)



    def none_clicked(self, app):
        def click(instance):
            if self.target_screen_name == "home_screen":
                self.app.home_screen.change_account_btn.text = "Choose Account"
                self.app.home_screen.displayed_account = None
                self.app.home_screen.refresh_display()
                self.app.switch_screen("home_screen")(instance)

            if self.target_screen_name == "budget_stats_screen":
                self.app.budget_stats_screen.change_account_btn.text = "Choose Account"
                self.app.budget_stats_screen.displayed_account = None
                self.app.budget_stats_screen.current_month_budget = create_current_month_budget(
                    self.app.budget_stats_screen.display_date,
                    None,
                    self.app.recurring_acts_screen.recurring_acts_dict
                )
                self.app.budget_stats_screen.refresh_screen()
                self.app.switch_screen("budget_stats_screen")(instance)

            if self.target_screen_name == "net_income_stats_screen":
                self.app.net_income_stats_screen.change_account_btn.text = "Choose Account"
                self.app.net_income_stats_screen.displayed_account = None
                self.app.net_income_stats_screen.net_income_stats = create_net_income_stats(
                    self.app.budget_stats_screen.display_date,
                    None,
                )
                self.app.net_income_stats_screen.refresh_screen()
                self.app.switch_screen("net_income_stats_screen")(instance)

            if self.target_screen_name == "expenses_stats_screen":
                self.app.expenses_stats_screen.change_account_btn.text = "Choose Account"
                self.app.expenses_stats_screen.displayed_account = None
                self.app.expenses_stats_screen.expenses_stats = ExpensesStats(self.app.expenses_stats_screen.display_date, None, self.app.recurring_acts_screen.recurring_acts_dict)
                self.app.expenses_stats_screen.refresh_screen()
                self.app.switch_screen("expenses_stats_screen")(instance)
                
            if self.target_screen_name == "add_transfer_screen":
                self.target_btn.text = "Choose Account"
                self.app.switch_screen("add_transfer_screen")(instance)

            if self.target_screen_name == "edit_transfer_screen":
                self.target_btn.text = "Choose Account"
                self.app.switch_screen("edit_transfer_screen")(instance)
            
            if self.target_screen_name == "records_screen":
                self.target_btn.text = "Choose Account"
                self.app.records_screen.displayed_account = None
                self.app.records_screen.refresh_screen()
                self.app.switch_screen("records_screen")(instance)

            if self.target_screen_name == "recurring_acts_screen":
                self.app.recurring_acts_screen.change_account_btn.text = "Choose Account"
                self.app.recurring_acts_screen.displayed_account = None
                self.app.recurring_acts_screen.refresh_row_widgets()
                self.app.switch_screen("recurring_acts_screen")(instance)

            if self.target_screen_name == "new_recurring_transfer_screen":
                self.target_btn.text = "Choose Account"
                self.app.switch_screen("new_recurring_transfer_screen")(instance)

            if self.target_screen_name == "edit_recurring_transfer_screen":
                self.target_btn.text = "Choose Account"
                self.app.switch_screen("edit_recurring_transfer_screen")(instance)

            self.app.transition_diagram.remove_node("choose_account_screen")
            self.app.screen_manager.remove_widget(self.app.choose_account_screen)
        return click

        

        
    def account_pressed(self, account):
        def pressed(instance):
            if self.target_screen_name == "home_screen":
                self.app.home_screen.change_account_btn.text = f"{account.number}. {account.name}"
                self.app.home_screen.displayed_account = account
                self.app.home_screen.refresh_display()
                self.app.switch_screen("home_screen")(instance)

            if self.target_screen_name == "budget_stats_screen":
                self.app.budget_stats_screen.change_account_btn.text = f"{account.number}. {account.name}"
                self.app.budget_stats_screen.displayed_account = account
                self.app.budget_stats_screen.current_month_budget = create_current_month_budget(
                    self.app.budget_stats_screen.display_date,
                    account,
                    self.app.recurring_acts_screen.recurring_acts_dict
                )
                self.app.budget_stats_screen.refresh_screen()
                self.app.switch_screen("budget_stats_screen")(instance)

            if self.target_screen_name == "expenses_stats_screen":
                self.app.expenses_stats_screen.change_account_btn.text = f"{account.number}. {account.name}"
                self.app.expenses_stats_screen.displayed_account = account
                self.app.expenses_stats_screen.expenses_stats = ExpensesStats(self.app.expenses_stats_screen.display_date, account, self.app.recurring_acts_screen.recurring_acts_dict)
                self.app.expenses_stats_screen.category_expenses_list = [
                    (category, self.app.expenses_stats_screen.expenses_stats.get_category_expenses(category, None)) for category in self.app.categories_screen.categories_dict.values() if category.kind == "Expense"
                ]
                self.app.expenses_stats_screen.category_expenses_list.sort(key=lambda x: x[1], reverse=True)
                self.app.expenses_stats_screen.refresh_screen()
                self.app.switch_screen("expenses_stats_screen")(instance)


            if self.target_screen_name == "net_income_stats_screen":
                self.app.net_income_stats_screen.change_account_btn.text = f"{account.number}. {account.name}"
                self.app.net_income_stats_screen.displayed_account = account
                self.app.net_income_stats_screen.net_income_stats = create_net_income_stats(
                    self.app.net_income_stats_screen.display_date,
                    account
                )
                self.app.net_income_stats_screen.refresh_screen()
                self.app.switch_screen("net_income_stats_screen")(instance)
                
            if self.target_screen_name == "add_transfer_screen":
                self.target_btn.text = f"{account.number}. {account.name}"
                self.app.switch_screen("add_transfer_screen")(instance)

            if self.target_screen_name == "edit_transfer_screen":
                self.target_btn.text = f"{account.number}. {account.name}"
                self.app.switch_screen("edit_transfer_screen")(instance)

            if self.target_screen_name == "records_screen":
                self.target_btn.text = f"{account.number}. {account.name}"
                self.app.records_screen.displayed_account = account
                self.app.records_screen.update_range()(instance)
                self.app.switch_screen("records_screen")(instance)

            if self.target_screen_name == "recurring_acts_screen":
                self.app.recurring_acts_screen.change_account_btn.text = f"{account.number}. {account.name}"
                self.app.recurring_acts_screen.displayed_account = account
                self.app.recurring_acts_screen.refresh_row_widgets()
                self.app.switch_screen("recurring_acts_screen")(instance)

            if self.target_screen_name == "new_recurring_transfer_screen":
                self.target_btn.text = f"{account.number}. {account.name}"
                self.app.switch_screen("new_recurring_transfer_screen")(instance)

            if self.target_screen_name == "edit_recurring_transfer_screen":
                self.target_btn.text = f"{account.number}. {account.name}"
                self.app.switch_screen("edit_recurring_transfer_screen")(instance)

            self.app.transition_diagram.remove_node("choose_account_screen")
            self.app.screen_manager.remove_widget(self.app.choose_account_screen)
                
        return pressed