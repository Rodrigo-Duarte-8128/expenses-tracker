from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex
from kivy.uix.button import Button
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.button import MDIconButton
from datetime import datetime
from screens.accounts_screens.choose_account_screen import ChooseAccountScreen
from screens.transactions_screens.add_expense_screen import AddExpenseScreen
from screens.transactions_screens.add_income_screen import AddIncomeScreen
from screens.transactions_screens.edit_transaction_screen import EditTransactionScreen
from screens.transfers_screens.add_transfer_screen import AddTransferScreen
from screens.transfers_screens.edit_transfer_screen import EditTransferScreen
from datas.date import Date
from datas.transaction import Transaction, Transfer
from row_widgets.transaction_row_widget import TransactionRowWidget
from row_widgets.transfer_row_widget import TransferRowWidget



red = hex("#E63946")
cream = hex("#F1FAEE")
light_teal = hex("#A8DADC")
blue = hex("#457B9D")
dark_blue = hex("#1D3557")
green = hex("#84a98c")



class HomeScreen(MDScreen):
    def __init__(self, app, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        '''
        The home screen contains the following elements:
            - A scrollable list of the month's transactions
            - The option to add new transactions and transfers
        ''' 

        self.app = app

        

        self.displayed_acts_dict = {} # an act includes both a transaction and a transfer

        # when the app starts the displayed acts are the same as the acts in use
        for act_simple_date in self.app.records_screen.acts_in_use_dict:
            act = self.app.records_screen.acts_in_use_dict[act_simple_date]

            self.displayed_acts_dict[act_simple_date] = act

        self.row_widgets = {} # this has keys which are simple_dates and values which can be Transaction or Transfer objects


        
        # when the app starts the displayed month is the current month
        date_string = str(datetime.now())
        self.date = Date(date_string)
        self.displayed_month = (int(self.date.month), int(self.date.year)) # eg (8, 2023) both ints

        

        self.layout = MDFloatLayout()

        self.window_width, self.window_height = Window.size




        # create month display and change month buttons
        self.arrow_left_btn = MDIconButton(
            icon = "arrow-left",
            pos_hint = {"x": 0.1, "y": 0.85},
            size_hint = (0.1, 0.05),
            on_press = self.previous_month_clicked()
        )
        self.layout.add_widget(self.arrow_left_btn)

        self.arrow_right_btn = MDIconButton(
            icon = "arrow-right",
            pos_hint = {"x": 0.8, "y": 0.85},
            size_hint = (0.1, 0.05),
            on_press = self.next_month_clicked()
        )
        self.layout.add_widget(self.arrow_right_btn)


        self.displayed_month_label = MDLabel(
            text = self.displayed_month_to_text(),
            pos_hint = {"x": 0.2, "y": 0.85},
            size_hint = (0.6, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.displayed_month_label)




        # add transfer button
        self.add_transfer_label = MDLabel(
            text = "Add Transfer:",
            pos_hint = {"x": 0, "y": 0.73},
            size_hint = (0.5, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.add_transfer_label)

        self.transfer_btn = MDIconButton(
            icon = "bank-transfer",
            pos_hint = {"x": 0.5, "y": 0.73},
            size_hint = (0.5, 0.05),
            on_press = self.new_transfer_clicked()
        )
        self.layout.add_widget(self.transfer_btn)


        # account functionality
        self.account_label = MDLabel(
            text = "Account:",
            pos_hint = {"x": 0, "y": 0.79},
            size_hint = (0.5, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.account_label)

        

        

        default = "Choose Account"
        self.displayed_account = None
        for account_number in app.accounts_screen.current_account_dict:
            self.displayed_account = app.accounts_screen.current_account_dict[account_number]
            default = f"{self.displayed_account.number}. {self.displayed_account.name}"


       

        self.change_account_btn = Button(
            text=default, 
            color = (1, 1, 1, 1),
            background_color = blue, 
            size_hint=(0.4, 0.05), 
            pos_hint={"x": 0.55, "y": 0.79},
            background_normal = ""
        )
        self.layout.add_widget(self.change_account_btn)
        self.change_account_btn.bind(on_press=self.change_account(app))



        



        # Create Transactions Scroll View Headers
        self.date_label = MDRaisedButton(
            text = "Date",
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            md_bg_color_disabled = blue,
            size_hint = (0.2, 0.05),
            pos_hint = {"x": 0, "y": 0.68},
            elevation = 0,
            _radius = 1
        )
        self.layout.add_widget(self.date_label)

        self.category_label = MDRaisedButton(
            text = "Category",
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            md_bg_color_disabled = blue,
            size_hint = (0.6, 0.05),
            pos_hint = {"x": 0.2, "y": 0.68},
            elevation = 0,
            _radius = 0
        )
        self.layout.add_widget(self.category_label)

        self.value_label = MDRaisedButton(
            text = "Value",
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            md_bg_color_disabled = blue,
            size_hint = (0.2, 0.05),
            pos_hint = {"x": 0.8, "y": 0.68},
            elevation = 0,
            _radius = 0
        )
        self.layout.add_widget(self.value_label)




        # Create Grid Layout that holds the Scroll View
        self.scroll_layout = MDGridLayout(
            cols=1,
            size_hint_y = None,
            size = (self.window_width, self.window_height * 0.62),
        )
        self.scroll_layout.bind(
            minimum_height=self.scroll_layout.setter("height")
        )
        self.scroll_layout.height = self.scroll_layout.minimum_height





        date_list = list(self.displayed_acts_dict)
        date_list.sort(key=self.absolute_date, reverse=True)

        for simple_date in date_list:
            act = self.displayed_acts_dict[simple_date]
            if type(act) == Transaction:
                if default != "Choose Account":
                    if act.account.number == int(default.split(".")[0]):

                        row = TransactionRowWidget(act)

                        # create edit transaction btn functionality
                        row.category_btn.bind(on_press=self.transaction_clicked(act))

                        self.row_widgets[simple_date] = row
                        self.scroll_layout.add_widget(row)

            if type(act) == Transfer:
                if default != "Choose Account":
                    if act.account_sending != None:
                        if act.account_sending.number == int(default.split(".")[0]):
                            # create transfer row widget
                            row = TransferRowWidget(act, "sent")

                            # create edit transfer btn functionality
                            row.account_btn.bind(on_press=self.transfer_clicked(act))

                            self.row_widgets[simple_date] = row
                            self.scroll_layout.add_widget(row)

                    if act.account_receiving != None:
                        if act.account_receiving.number == int(default.split(".")[0]):
                            # create transfer row widget
                            row = TransferRowWidget(act, "received")

                            # create edit transfer btn functionality
                            row.account_btn.bind(on_press=self.transfer_clicked(act))

                            self.row_widgets[simple_date] = row
                            self.scroll_layout.add_widget(row)


        # Create Scroll View
        self.scroll_view = MDScrollView(
            size_hint = (1, 0.62),
            pos_hint = {"x": 0, "y": 0.06},
            bar_width = 10
        )
        self.scroll_view.add_widget(self.scroll_layout)
        self.layout.add_widget(self.scroll_view)







        # Create new expenditure button
        self.new_expense_button = MDRaisedButton(
            text = "Expenditure",
            size_hint = (0.45, 0.04),
            pos_hint = {"x": 0.525, "y": 0.005},
            md_bg_color = red,
            on_press = self.new_expense_clicked()
        )
        self.layout.add_widget(self.new_expense_button)


        # Create new income button
        self.new_income_button = MDRaisedButton(
            text = "Income",
            size_hint = (0.45, 0.04),
            pos_hint = {"x": 0.025, "y": 0.005},
            md_bg_color = green,
            on_press = self.new_income_clicked()
        )
        self.layout.add_widget(self.new_income_button)




        
        self.add_widget(self.layout)



    def previous_month_clicked(self):
        def click(instance):
            # update the displayed month and refresh the row widgets
            old_month = self.displayed_month[0]
            old_year = self.displayed_month[1]
            if old_month == 1:
                new_month = 12
                new_year = old_year - 1
            else:
                new_month = old_month - 1
                new_year = old_year
            
            self.displayed_month = (new_month, new_year)
            # update displayed month label
            self.displayed_month_label.text = self.displayed_month_to_text()


            # update displayed_acts_dict
            self.displayed_acts_dict = {}

            month_string = str(new_month) if len(str(new_month)) == 2 else f"0{new_month}"
            year_char_len = len(str(new_year))
            if year_char_len == 4:
                year_string = str(new_year)
            elif year_char_len == 3:
                year_string = f"0{new_year}"
            elif year_char_len == 2:
                year_string = f"00{new_year}"
            elif year_char_len == 2:
                year_string = f"000{new_year}"


            for transaction_simple_date, _ in self.app.records_screen.transactions_store.find(month=month_string, year=year_string):
                transaction = self.app.records_screen.get_transaction_from_storage(transaction_simple_date)
                if transaction.account == self.displayed_account:
                    self.displayed_acts_dict[transaction_simple_date] = transaction


            for transfer_simple_date, _ in self.app.records_screen.transfers_store.find(month=month_string, year=year_string):
                transfer = self.app.records_screen.get_transfer_from_storage(transfer_simple_date)
                if self.displayed_account != None:
                    if transfer.account_sending == self.displayed_account or transfer.account_receiving == self.displayed_account:
                        self.displayed_acts_dict[transfer_simple_date] = transfer


            # refresh row widgets
            self.refresh_row_widgets()
        return click
    
    def next_month_clicked(self):
        def click(instance):
            # check if there is a next month, if so then update the displayed month and refresh the row widgets
            current_date = Date(str(datetime.now()))
            if self.displayed_month != (int(current_date.month), int(current_date.year)):
                old_month = self.displayed_month[0]
                old_year = self.displayed_month[1]
                if old_month == 12:
                    new_month = 1
                    new_year = old_year + 1
                else:
                    new_month = old_month + 1
                    new_year = old_year
                
                self.displayed_month = (new_month, new_year)
                self.displayed_month_label.text = self.displayed_month_to_text()

                # update displayed_acts_dict
                self.displayed_acts_dict = {}
                month_string = str(new_month) if len(str(new_month)) == 2 else f"0{new_month}"
                year_char_len = len(str(new_year))
                if year_char_len == 4:
                    year_string = str(new_year)
                elif year_char_len == 3:
                    year_string = f"0{new_year}"
                elif year_char_len == 2:
                    year_string = f"00{new_year}"
                elif year_char_len == 2:
                    year_string = f"000{new_year}"


                for transaction_simple_date, _ in self.app.records_screen.transactions_store.find(month=month_string, year=year_string):
                    transaction = self.app.records_screen.get_transaction_from_storage(transaction_simple_date)
                    if transaction.account == self.displayed_account:
                        self.displayed_acts_dict[transaction_simple_date] = transaction


                for transfer_simple_date, _ in self.app.records_screen.transfers_store.find(month=month_string, year=year_string):
                    transfer = self.app.records_screen.get_transfer_from_storage(transfer_simple_date)
                    if self.displayed_account != None:
                        if transfer.account_sending == self.displayed_account or transfer.account_receiving == self.displayed_account:
                            self.displayed_acts_dict[transfer_simple_date] = transfer

                self.refresh_row_widgets()
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

        return f"{calendar[self.displayed_month[0]]} {self.displayed_month[1]}"




    def transfer_clicked(self, transfer):
        def click(instance):
            self.app.edit_transfer_screen = EditTransferScreen(self.app, transfer, "home_screen", name="edit_transfer_screen")
            self.app.screen_manager.add_widget(self.app.edit_transfer_screen)

            # add screen to transition diagram
            self.app.transition_diagram.add_node("edit_transfer_screen", root_screen_node = self.app.home_screen_node, left_node = self.app.home_screen_node)

            self.app.switch_screen("edit_transfer_screen")(instance)
        return click

    
    def refresh_current_account(self):
        # refresh current account from accounts_screen.current_account_dict
        if self.app.accounts_screen.current_account_dict == {}:
            self.change_account_btn.text = "Choose Account"

        else:
            current_account = list(self.app.accounts_screen.current_account_dict.values())[0]
            self.change_account_btn.text = f"{current_account.number}. {current_account.name}"
            self.displayed_account = current_account

        #self.refresh_row_widgets()
        self.refresh_display()



    def change_account(self, app):
        def change(instance):
            app.choose_account_screen = ChooseAccountScreen(app, "home_screen", instance, name="choose_account_screen")
            app.screen_manager.add_widget(app.choose_account_screen)

            # add screen to transition diagram
            app.transition_diagram.add_node("choose_account_screen", root_screen_node = app.home_screen_node, left_node = app.home_screen_node)

            app.switch_screen("choose_account_screen")(instance)
        return change





    def transaction_clicked(self, transaction):
        def click(instance):
            self.app.edit_transaction_screen = EditTransactionScreen(self.app, transaction, "home_screen", name="edit_transaction_screen")
            self.app.screen_manager.add_widget(self.app.edit_transaction_screen)

            # add screen to transition diagram
            self.app.transition_diagram.add_node("edit_transaction_screen", root_screen_node = self.app.home_screen_node, left_node = self.app.home_screen_node)

            self.app.switch_screen("edit_transaction_screen")(instance)
        return click
    


    def new_transfer_clicked(self):
        def click(instance):
            self.app.add_transfer_screen = AddTransferScreen(self.app, name="add_transfer_screen")
            self.app.screen_manager.add_widget(self.app.add_transfer_screen)

            self.app.transition_diagram.add_node(
                "add_transfer_screen",
                root_screen_node = self.app.home_screen_node,
                left_node = self.app.home_screen_node
            )

            self.app.switch_screen("add_transfer_screen")(instance)
        return click



    def new_income_clicked(self):
        def click(instance):
            self.app.add_income_screen = AddIncomeScreen(self.app, name="add_income_screen")
            self.app.screen_manager.add_widget(self.app.add_income_screen)

            self.app.transition_diagram.add_node(
                "add_income_screen",
                root_screen_node = self.app.home_screen_node,
                left_node = self.app.home_screen_node
            )

            self.app.switch_screen("add_income_screen")(instance)
        return click

    def new_expense_clicked(self):
        def click(instance):
            self.app.add_expense_screen = AddExpenseScreen(self.app, name="add_expense_screen")
            self.app.screen_manager.add_widget(self.app.add_expense_screen)

            self.app.transition_diagram.add_node(
                "add_expense_screen",
                root_screen_node = self.app.home_screen_node,
                left_node = self.app.home_screen_node
            )

            self.app.switch_screen("add_expense_screen")(instance)
        return click
    



    def refresh_display(self):
        '''
        reset displayed_acts and rebuild them, and then refresh row widgets
        '''
        self.displayed_acts_dict = {}
        #self.displayed_month
        month_string = str(self.displayed_month[0]) if len(str(self.displayed_month[0])) == 2 else f"0{self.displayed_month[0]}"
        year_string = f"{'0' * (4 - len(str(self.displayed_month[1])))}{self.displayed_month[1]}"



        for transaction_simple_date, _ in self.app.records_screen.transactions_store.find(month=month_string, year=year_string):
            transaction = self.app.records_screen.get_transaction_from_storage(transaction_simple_date)
            if transaction.account == self.displayed_account:
                self.displayed_acts_dict[transaction_simple_date] = transaction


        for transfer_simple_date, _ in self.app.records_screen.transfers_store.find(month=month_string, year=year_string):
            transfer = self.app.records_screen.get_transfer_from_storage(transfer_simple_date)
            if self.displayed_account != None:
                if transfer.account_sending == self.displayed_account or transfer.account_receiving == self.displayed_account:
                    self.displayed_acts_dict[transfer_simple_date] = transfer

        self.refresh_row_widgets()
    




    def refresh_row_widgets(self):
        '''
        redraws the displayed row widgets from displayed_acts_dict
        '''
    

        # remove current row widgets from the scroll view
        for act_simple_date in self.row_widgets:
            self.scroll_layout.remove_widget(self.row_widgets[act_simple_date])

        # reset row_widgets dict
        self.row_widgets = {}
        

        date_list = list(self.displayed_acts_dict)
        date_list.sort(key=self.absolute_date, reverse=True)

        for simple_date in date_list:
            act = self.displayed_acts_dict[simple_date]
            account_num_name = self.change_account_btn.text
            if type(act) == Transaction:
                if account_num_name != "Choose Account":
                    if act.account.number == int(account_num_name.split(".")[0]):

                        row = TransactionRowWidget(act)

                        # create edit transaction btn functionality
                        row.category_btn.bind(on_press=self.transaction_clicked(act))

                        self.row_widgets[simple_date] = row
                        self.scroll_layout.add_widget(row)

            if type(act) == Transfer:
                if account_num_name != "Choose Account":
                    if act.account_sending != None:
                        if act.account_sending.number == int(account_num_name.split(".")[0]):
                            # create transfer row widget
                            row = TransferRowWidget(act, "sent")

                            # create edit transfer btn functionality
                            row.account_btn.bind(on_press=self.transfer_clicked(act))

                            self.row_widgets[simple_date] = row
                            self.scroll_layout.add_widget(row)

                    if act.account_receiving != None:
                        if act.account_receiving.number == int(account_num_name.split(".")[0]):
                            # create transfer row widget
                            row = TransferRowWidget(act, "received")

                            # create edit transfer btn functionality
                            row.account_btn.bind(on_press=self.transfer_clicked(act))

                            self.row_widgets[simple_date] = row
                            self.scroll_layout.add_widget(row)

    
        
    

    
    def absolute_date(self, simple_date_string):
        ''' 
        returns the amount of time in seconds from january first of the year zero to the given date

        the simle_date_string must have the form "dd/mm/yyyy hh:mm:ss"

        '''
        calendar = {1 : 31, 2 : 28, 3 : 31, 4 : 30, 5 : 31,
            6 : 30, 7 : 31, 8 : 31, 9 : 30, 10 : 31,
            11 : 30, 12 : 31}
        
        leap_calendar = {1 : 31, 2 : 29, 3 : 31, 4 : 30, 5 : 31,
            6 : 30, 7 : 31, 8 : 31, 9 : 30, 10 : 31,
            11 : 30, 12 : 31}
        
        year = int(simple_date_string[6: 10])
        month = int(simple_date_string[3:5])
        day = int(simple_date_string[:2])
        hour = int(simple_date_string[11:13])
        minutes = int(simple_date_string[14:16])
        seconds = int(simple_date_string[17:])

        total_days = 0

        for num in range(year):
            total_days += 365 + int(self.is_leap_year(num))

        for mon in range(1, month):
            if not self.is_leap_year(year):
                total_days += calendar[mon]
            else:
                total_days += leap_calendar[mon] 
        total_days += day
        return total_days * 86400 + hour*3600 + minutes*60 + seconds
        
    @staticmethod
    def is_leap_year(year):
    #year is a natural number (incl zero)
        if year % 4 == 0:
            if year % 100 == 0:
                if year % 400 == 0:
                    return True
                return False
            return True
        return False