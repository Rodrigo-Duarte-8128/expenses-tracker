from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex
from kivy.storage.jsonstore import JsonStore
from kivy.uix.button import Button
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
from datetime import datetime
from datas.transaction import Transaction, Transfer, RecurringTransaction, RecurringTransfer
from datas.date import Date, get_date_from_simple_date, month_year_to_simple_date, date_is_in_interval, compare_dates
from row_widgets.transaction_row_widget import TransactionRowWidget
from row_widgets.transfer_row_widget import TransferRowWidget
from screens.accounts_screens.choose_account_screen import ChooseAccountScreen
from screens.transactions_screens.edit_transaction_screen import EditTransactionScreen
from screens.transfers_screens.edit_transfer_screen import EditTransferScreen

red = hex("#E63946")
cream = hex("#F1FAEE")
light_teal = hex("#A8DADC")
blue = hex("#457B9D")
dark_blue = hex("#1D3557")
green = hex("#84a98c")



class RecordsScreen(MDScreen):
    def __init__(self, app, **kwargs):
        super(RecordsScreen, self).__init__(**kwargs)

        self.layout = MDFloatLayout()

        self.app = app

        self.window_width, self.window_height = Window.size

        

        # create reference to store transactions and transfers
        self.transactions_store = JsonStore("transactions.json")
        self.transfers_store = JsonStore("transfers.json")

        # acts_in_use includes all the acts displayed in the home screen and the records screen
        # whenever we need an act object we should get/modify it from acts_in_use_dict
        self.acts_in_use_dict = {}

        # displayed acts include the transfer/transaction objects that are displayed in this screen
        self.displayed_acts_dict = {}

        self.row_widgets = {}


        # account functionality
        self.account_label = MDLabel(
            text = "Account:",
            pos_hint = {"x": 0, "y": 0.6575},
            size_hint = (0.5, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.account_label)

        default = "Choose Account"
        self.displayed_account = None
        for account_number in app.accounts_screen.current_account_dict:
            account = app.accounts_screen.current_account_dict[account_number]
            self.displayed_account = account
            default = f"{account.number}. {account.name}"

        self.change_account_btn = Button(
            text=default, 
            color = (1, 1, 1, 1),
            background_color = blue, 
            size_hint=(0.4, 0.05), 
            pos_hint={"x": 0.55, "y": 0.6575},
            background_normal = ""
        )
        self.layout.add_widget(self.change_account_btn)
        self.change_account_btn.bind(on_press=self.change_account())



        # when the app starts we need to create all the missing recurring acts 
        date_string = str(datetime.now())
        self.date = Date(date_string)
        

        self.build_missing_recurring_transactions()
        self.build_missing_recurring_transfers()

       
        # when the app starts, the acts in use are the transfers/transactions from the current month and the default account
        simple_date = self.date.get_date_simple_string()
        month = simple_date[3:5]
        year = simple_date[6:10]
        for transaction_simple_date, _ in self.transactions_store.find(month=month, year=year):
            transaction = self.get_transaction_from_storage(transaction_simple_date)
            if default != "Choose Account":
                if transaction.account.number == int(default.split(".")[0]):
                    self.acts_in_use_dict[transaction_simple_date] = transaction


        for transfer_simple_date, _ in self.transfers_store.find(month=month, year=year):
            transfer = self.get_transfer_from_storage(transfer_simple_date)
            if default != "Choose Account":
                if transfer.account_sending != None:
                    if transfer.account_sending.number == int(default.split(".")[0]):
                        self.acts_in_use_dict[transfer_simple_date] = transfer
                if transfer.account_receiving != None:
                    if transfer.account_receiving.number == int(default.split(".")[0]):
                        self.acts_in_use_dict[transfer_simple_date] = transfer

        


        # create date options
        self.start_date_text_field = MDTextField(
            hint_text = "Start Date (dd/mm/yyyy)",
            mode = "rectangle",
            helper_text = "Invalid Date",
            helper_text_mode = "on_error",
            pos_hint = {"x": 0.025, "y": 0.8},
            size_hint = (0.45, 0.05)
        )
        self.start_date_text_field.text = f"01/{self.date.month}/{self.date.year}"
        self.layout.add_widget(self.start_date_text_field)



        self.end_date_text_field = MDTextField(
            hint_text = "End Date (dd/mm/yyyy)",
            mode = "rectangle",
            helper_text = "Invalid Date",
            helper_text_mode = "on_error",
            pos_hint = {"x": 0.525, "y": 0.8},
            size_hint = (0.45, 0.05)
        )
        self.end_date_text_field.text = f"{self.compute_last_day(self.date)}/{self.date.month}/{self.date.year}"
        self.layout.add_widget(self.end_date_text_field)


        # create button to update range
        self.update_range_btn = MDRaisedButton(
            text = "Update Range",
            md_bg_color = dark_blue,
            size_hint = (0.4, 0.05),
            pos_hint = {"x": 0.3, "y": 0.725},
            on_press = self.update_range()
        )
        self.layout.add_widget(self.update_range_btn)


        
        

        # create scroll view headers
        self.date_label = MDRaisedButton(
            text = "Date",
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            md_bg_color_disabled = blue,
            size_hint = (0.2, 0.05),
            pos_hint = {"x": 0, "y": 0.59},
            elevation = 0,
            _radius = 0
        )
        self.layout.add_widget(self.date_label)

        self.category_label = MDRaisedButton(
            text = "Category",
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            md_bg_color_disabled = blue,
            size_hint = (0.6, 0.05),
            pos_hint = {"x": 0.2, "y": 0.59},
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
            pos_hint = {"x": 0.8, "y": 0.59},
            elevation = 0,
            _radius = 0
        )
        self.layout.add_widget(self.value_label)




        # Create Grid Layout that holds the Scroll View
        self.scroll_layout = MDGridLayout(
            cols=1,
            size_hint_y = None,
            size = (self.window_width, self.window_height * 0.58),
        )
        self.scroll_layout.bind(
            minimum_height=self.scroll_layout.setter("height")
        )
        self.scroll_layout.height = self.scroll_layout.minimum_height





        date_list = list(self.acts_in_use_dict)
        date_list.sort(key=self.absolute_date, reverse=True)

        for simple_date in date_list:
            act = self.acts_in_use_dict[simple_date]
            if type(act) == Transaction:
                if default != "Choose Account":
                    if act.account.number == int(default.split(".")[0]):

                        row = TransactionRowWidget(act)

                        # create edit transaction btn functionality
                        row.category_btn.bind(on_press=self.transaction_clicked(act))

                        self.row_widgets[simple_date] = row
                        self.scroll_layout.add_widget(row)
                        self.displayed_acts_dict[simple_date] = act

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
                            self.displayed_acts_dict[simple_date] = act

                    if act.account_receiving != None:
                        if act.account_receiving.number == int(default.split(".")[0]):
                            # create transfer row widget
                            row = TransferRowWidget(act, "received")

                            # create edit transfer btn functionality
                            row.account_btn.bind(on_press=self.transfer_clicked(act))

                            self.row_widgets[simple_date] = row
                            self.scroll_layout.add_widget(row)
                            self.displayed_acts_dict[simple_date] = act


        # Create Scroll View
        self.scroll_view = MDScrollView(
            size_hint = (1, 0.58),
            pos_hint = {"x": 0, "y": 0},
            bar_width = 10
        )
        self.scroll_view.add_widget(self.scroll_layout)
        self.layout.add_widget(self.scroll_view)


        # create scroll view



        self.add_widget(self.layout)


    @staticmethod
    def convert_identifier_to_time(identifier):
        '''
        converts an int between 0 and 86400 to a time "hh:mm:ss" corresponding to the time after the int number of seconds

        eg 5 converts to "00:00:05", 61 converts to "00:01:01" and so on
        '''
        seconds = identifier % 60
        bulk_minutes = int((identifier - seconds) / 60)
        minutes = bulk_minutes % 60
        hours = int((bulk_minutes - minutes)/ 60)

        sec_str = str(seconds)
        min_str = str(minutes)
        hour_str = str(hours)

        if len(sec_str) == 1:
            sec_str = f"0{sec_str}"
        if len(min_str) == 1:
            min_str = f"0{min_str}"
        if len(hour_str) == 1:
            hour_str = f"0{hour_str}"

        return f"{hour_str}:{min_str}:{sec_str}"



    def build_missing_recurring_transfers(self):
        for recurring_act_name in self.app.recurring_acts_screen.recurring_acts_dict:
            recurring_act = self.app.recurring_acts_screen.recurring_acts_dict[recurring_act_name]
            current_month_year = (int(self.date.month), int(self.date.year))
            
            if type(recurring_act) == RecurringTransfer:
                if recurring_act.instantiation_dates_list != []:
                    recurring_act.instantiation_dates_list.sort(key=self.absolute_date, reverse=True)
                    most_recent_simple_date = recurring_act.instantiation_dates_list[0]
                    most_recent_month_year = (int(most_recent_simple_date[3:5]), int(most_recent_simple_date[6:10]))
                    month_year = most_recent_month_year
                else:
                    if current_month_year[0] == 1:
                        month_year = (12, current_month_year[1] - 1)
                    else:
                        month_year = (current_month_year[0] - 1, current_month_year[1])
                    
                while month_year != current_month_year:
                    
                    # increment month_year
                    if month_year[0] != 12:
                        month_year = (month_year[0] + 1, month_year[1])
                    else:
                        month_year = (1, month_year[1] + 1)


                    # check if the date is in the right interval
                    if not date_is_in_interval(
                        month_year_to_simple_date(recurring_act.month_day, month_year)[:10],
                        recurring_act.start_date.get_date_simple_string()[:10],
                        recurring_act.end_date.get_date_simple_string()[:10] if recurring_act.end_date != None else None
                    ):
                        continue 



                    if month_year != current_month_year:
                        # in this case we always add new transaction
                        simple_date = (month_year_to_simple_date(recurring_act.month_day, month_year)[:11] + 
                                       self.convert_identifier_to_time(recurring_act.identifier))
                        date = get_date_from_simple_date(simple_date)
                        new_transfer = Transfer(
                            date,
                            recurring_act.value,
                            recurring_act.note,
                            account_sending = recurring_act.account_sending,
                            account_receiving = recurring_act.account_receiving
                        )
                        self.store_transfer(new_transfer)

                        # update account sending balance
                        if recurring_act.account_sending != None:
                            new_balance = round(recurring_act.account_sending.balance - recurring_act.value, 2)
                            self.app.accounts_screen.update_balance(recurring_act.account_sending, new_balance)

                        # update account receiving balance
                        if recurring_act.account_receiving != None:
                            new_balance = round(recurring_act.account_receiving.balance + recurring_act.value, 2)
                            self.app.accounts_screen.update_balance(recurring_act.account_receiving, new_balance)


                        # update instantiation list
                        new_instantiation_dates_list = (recurring_act.instantiation_dates_list + 
                                                        [month_year_to_simple_date(recurring_act.month_day, month_year)])
                        recurring_act.instantiation_dates_list = new_instantiation_dates_list
                        self.app.recurring_acts_screen.recurring_transfers_store.delete(recurring_act.name)
                        self.app.recurring_acts_screen.store_recurring_transfer(recurring_act)

                    elif int(self.date.day) >= recurring_act.month_day:
                        # need to check if the current day has surpassed the month_day of the recurring_act
                        simple_date = (month_year_to_simple_date(recurring_act.month_day, month_year)[:11] + 
                                       self.convert_identifier_to_time(recurring_act.identifier))
                        date = get_date_from_simple_date(simple_date)
                        new_transfer = Transfer(
                            date,
                            recurring_act.value,
                            recurring_act.note,
                            account_sending = recurring_act.account_sending,
                            account_receiving = recurring_act.account_receiving
                        )
                        self.store_transfer(new_transfer)

                        # update account sending balance
                        if recurring_act.account_sending != None:
                            new_balance = round(recurring_act.account_sending.balance - recurring_act.value, 2)
                            self.app.accounts_screen.update_balance(recurring_act.account_sending, new_balance)

                        # update account receiving balance
                        if recurring_act.account_receiving != None:
                            new_balance = round(recurring_act.account_receiving.balance + recurring_act.value, 2)
                            self.app.accounts_screen.update_balance(recurring_act.account_receiving, new_balance)


                        # update instantiation list
                        new_instantiation_dates_list = (recurring_act.instantiation_dates_list + 
                                                        [month_year_to_simple_date(recurring_act.month_day, month_year)])
                        recurring_act.instantiation_dates_list = new_instantiation_dates_list
                        self.app.recurring_acts_screen.recurring_transfers_store.delete(recurring_act.name)
                        self.app.recurring_acts_screen.store_recurring_transfer(recurring_act)
                            
                
                



    def build_missing_recurring_transactions(self):
        for recurring_act_name in self.app.recurring_acts_screen.recurring_acts_dict:
            recurring_act = self.app.recurring_acts_screen.recurring_acts_dict[recurring_act_name]
            current_month_year = (int(self.date.month), int(self.date.year))
            if type(recurring_act) == RecurringTransaction:
                if recurring_act.instantiation_dates_list != []:
                    recurring_act.instantiation_dates_list.sort(key=self.absolute_date, reverse=True)
                    most_recent_simple_date = recurring_act.instantiation_dates_list[0]
                    most_recent_month_year = (int(most_recent_simple_date[3:5]), int(most_recent_simple_date[6:10]))
                    month_year = most_recent_month_year
                else:
                    if current_month_year[0] == 1:
                        month_year = (12, current_month_year[1] - 1)
                    else:
                        month_year = (current_month_year[0] - 1, current_month_year[1])
                    

                while month_year != current_month_year:
                    
                    # increment month_year
                    if month_year[0] != 12:
                        month_year = (month_year[0] + 1, month_year[1])
                    else:
                        month_year = (1, month_year[1] + 1)

                    # check if the date is in the right interval
                    if not date_is_in_interval(
                        month_year_to_simple_date(recurring_act.month_day, month_year)[:10],
                        recurring_act.start_date.get_date_simple_string()[:10],
                        recurring_act.end_date.get_date_simple_string()[:10] if recurring_act.end_date != None else None
                    ):
                        continue 



                    if month_year != current_month_year:
                        # in this case we always add new transaction
                        simple_date = (month_year_to_simple_date(recurring_act.month_day, month_year)[:11] + 
                                       self.convert_identifier_to_time(recurring_act.identifier))
                        date = get_date_from_simple_date(simple_date)

                        new_transaction = Transaction(
                            date,
                            recurring_act.value,
                            recurring_act.category if recurring_act.category != None else None,
                            recurring_act.account,
                            recurring_act.note,
                            subcategory= recurring_act.subcategory if recurring_act.subcategory != None else None,
                            old_category_name = recurring_act.old_category_name,
                            old_subcategory_name = recurring_act.old_subcategory_name
                        )
                        self.store_transaction(new_transaction)

                        # update account balance
                        new_balance = round(recurring_act.account.balance + recurring_act.value, 2)
                        self.app.accounts_screen.update_balance(recurring_act.account, new_balance)


                        # update instantiation list
                        new_instantiation_dates_list = (recurring_act.instantiation_dates_list +
                                                        [month_year_to_simple_date(recurring_act.month_day, month_year)])
                        recurring_act.instantiation_dates_list = new_instantiation_dates_list
                        self.app.recurring_acts_screen.recurring_transactions_store.delete(recurring_act.name)
                        self.app.recurring_acts_screen.store_recurring_transaction(recurring_act)

                    elif int(self.date.day) >= recurring_act.month_day: # need to check if the current day has surpassed the month_day of the recurring_act

                        simple_date = (month_year_to_simple_date(recurring_act.month_day, month_year)[:11] + 
                                       self.convert_identifier_to_time(recurring_act.identifier))
                        date = get_date_from_simple_date(simple_date)
                        
                        new_transaction = Transaction(
                            date,
                            recurring_act.value,
                            recurring_act.category,
                            recurring_act.account,
                            recurring_act.note,
                            subcategory= recurring_act.subcategory,
                            old_category_name = recurring_act.old_category_name,
                            old_subcategory_name = recurring_act.old_subcategory_name
                        )
                        self.store_transaction(new_transaction)

                        # update account balance
                        new_balance = round(recurring_act.account.balance + recurring_act.value, 2)
                        self.app.accounts_screen.update_balance(recurring_act.account, new_balance)


                        # update instantiation list
                        new_instantiation_dates_list = (recurring_act.instantiation_dates_list + 
                                                        [month_year_to_simple_date(recurring_act.month_day, month_year)])
                        recurring_act.instantiation_dates_list = new_instantiation_dates_list
                        self.app.recurring_acts_screen.recurring_transactions_store.delete(recurring_act.name)
                        self.app.recurring_acts_screen.store_recurring_transaction(recurring_act)
                            
                
                



    def change_account(self):
        def change(instance):
            self.app.choose_account_screen = ChooseAccountScreen(self.app, "records_screen", instance, name="choose_account_screen")
            self.app.screen_manager.add_widget(self.app.choose_account_screen)

            # add screen to transition diagram
            self.app.transition_diagram.add_node("choose_account_screen", root_screen_node = self.app.records_screen_node, left_node = self.app.records_screen_node)

            self.app.switch_screen("choose_account_screen")(instance)
        return change
    
    
    
        

    def update_range(self):
        def update(instance):
            errors = []
            start_simple_date = self.start_date_text_field.text
            end_simple_date = self.end_date_text_field.text


            if not self._validate_date(start_simple_date):
                errors.append("invalid_start_date")
            if not self._validate_date(end_simple_date):
                errors.append("invalid_end_date")

            if not errors:
                # update acts_in_use_dict and displayed_acts_dict
                for act_simple_date in self.displayed_acts_dict:
                    del self.acts_in_use_dict[act_simple_date]
                self.displayed_acts_dict = {}

                

                for transaction_simple_date in self.transactions_store.keys():
                    if date_is_in_interval(transaction_simple_date[:10], start_simple_date, end_simple_date):
                        if self.change_account_btn.text != "Choose Account":
                            transaction = self.get_transaction_from_storage(transaction_simple_date)
                            if transaction.account.number == int(self.change_account_btn.text.split(".")[0]):
                                self.acts_in_use_dict[transaction_simple_date] = transaction
                                self.displayed_acts_dict[transaction_simple_date] = transaction


                for transfer_simple_date in self.transfers_store.keys():
                    if date_is_in_interval(transfer_simple_date[:10], start_simple_date, end_simple_date):
                        if self.change_account_btn.text != "Choose Account":
                            transfer = self.get_transfer_from_storage(transfer_simple_date)
                        
                            if transfer.account_sending != None:
                                if transfer.account_sending.number == int(self.change_account_btn.text.split(".")[0]):
                                    self.acts_in_use_dict[transfer_simple_date] = transfer
                                    self.displayed_acts_dict[transfer_simple_date] = transfer
                            if transfer.account_receiving != None:
                                if transfer.account_receiving.number == int(self.change_account_btn.text.split(".")[0]):
                                    self.acts_in_use_dict[transfer_simple_date] = transfer
                                    self.displayed_acts_dict[transfer_simple_date] = transfer


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

                
            if "invalid_start_date" in errors:
                if self.start_date_text_field.error == False:
                    self.start_date_text_field.error = True

            if "invalid_start_date" not in errors:
                if self.start_date_text_field.error == True:
                    self.start_date_text_field.error = False

            if "invalid_end_date" in errors:
                if self.end_date_text_field.error == False:
                    self.end_date_text_field.error = True

            if "invalid_end_date" not in errors:
                if self.end_date_text_field.error == True:
                    self.end_date_text_field.error = False
                

        return update


    def transaction_clicked(self, transaction):
        def click(instance):
            self.app.edit_transaction_screen = EditTransactionScreen(self.app, transaction, "records_screen", name="edit_transaction_screen")
            self.app.screen_manager.add_widget(self.app.edit_transaction_screen)

            # add screen to transition diagram
            self.app.transition_diagram.add_node("edit_transaction_screen", root_screen_node = self.app.home_screen_node, left_node = self.app.home_screen_node)

            self.app.switch_screen("edit_transaction_screen")(instance)
        return click
    
    def transfer_clicked(self, transfer):
        def click(instance):
            self.app.edit_transfer_screen = EditTransferScreen(self.app, transfer, "records_screen", name="edit_transfer_screen")
            self.app.screen_manager.add_widget(self.app.edit_transfer_screen)

            # add screen to transition diagram
            self.app.transition_diagram.add_node("edit_transfer_screen", root_screen_node = self.app.home_screen_node, left_node = self.app.home_screen_node)

            self.app.switch_screen("edit_transfer_screen")(instance)
        return click
    





    def refresh_screen(self):
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





    
    def compute_last_day(self, date):
        '''
        returns the last day of the month of the passed date
        '''
        last_day_calendar = {
            "01": "31",
            "02": "28",
            "03": "31",
            "04": "30",
            "05": "31",
            "06": "30",
            "07": "31",
            "08": "31",
            "09": "30",
            "10": "31",
            "11": "30",
            "12": "31"
        }

        last_day_leap_calendar = {
            "01": "31",
            "02": "28",
            "03": "31",
            "04": "30",
            "05": "31",
            "06": "30",
            "07": "31",
            "08": "31",
            "09": "30",
            "10": "31",
            "11": "30",
            "12": "31"
        }
        
        year = int(date.year)
        if self.is_leap_year(year):
            return last_day_leap_calendar[date.month]
        else:
            return last_day_calendar[date.month]



    def add_transfer(self, transfer):
        date_simple_string = transfer.date.get_date_simple_string()
        month = date_simple_string[3:5]
        year = date_simple_string[6:10]

        if transfer.account_sending == None and transfer.account_receiving != None:
            self.transfers_store.put(
                date_simple_string,
                month = month,
                year = year,
                value = str(transfer.value),
                note = transfer.note,
                account_receiving = str(transfer.account_receiving.number)
            )

            # update the balance of the account that received the transfer
            new_balance = round(transfer.account_receiving.balance + transfer.value, 2)
            self.app.accounts_screen.update_balance(transfer.account_receiving, new_balance)

        if transfer.account_sending != None and transfer.account_receiving == None:
            self.transfers_store.put(
                date_simple_string,
                month = month,
                year = year,
                value = str(transfer.value),
                note = transfer.note,
                account_sending = str(transfer.account_sending.number)
            )

            # update the balance of the account that sent the transfer
            new_balance = round(transfer.account_sending.balance - transfer.value, 2)
            self.app.accounts_screen.update_balance(transfer.account_sending, new_balance)

        if transfer.account_sending != None and transfer.account_receiving != None:
            self.transfers_store.put(
                date_simple_string,
                month = month,
                year = year,
                value = str(transfer.value),
                note = transfer.note,
                account_sending = str(transfer.account_sending.number),
                account_receiving = str(transfer.account_receiving.number)
            )

            # update the balance of the account that sent the transfer
            new_balance = round(transfer.account_sending.balance - transfer.value, 2)
            self.app.accounts_screen.update_balance(transfer.account_sending, new_balance)

            # update the balance of the account that received the transfer
            new_balance = round(transfer.account_receiving.balance + transfer.value, 2)
            self.app.accounts_screen.update_balance(transfer.account_receiving, new_balance)


        # if this transfer is in the displayed month in home screen then add it to displayed acts
        if int(transfer.date.year) == self.app.home_screen.displayed_month[1] and int(transfer.date.month) == self.app.home_screen.displayed_month[0]:
            if self.app.home_screen.displayed_account != None:
                if transfer.account_sending == self.app.home_screen.displayed_account or transfer.account_receiving == self.app.home_screen.displayed_account:
                    self.app.home_screen.displayed_acts_dict[date_simple_string] = transfer
                    self.acts_in_use_dict[date_simple_string] = transfer

                # refresh home screen
                #self.app.home_screen.refresh_row_widgets()

                if transfer.account_sending == self.app.home_screen.displayed_account:
                    row = TransferRowWidget(transfer, "sent")

                    # create edit transaction btn functionality
                    row.account_btn.bind(on_press=self.app.home_screen.transfer_clicked(transfer))

                    self.app.home_screen.row_widgets[transfer.date.get_date_simple_string()] = row


                    # find correct index position for the new transaction
                    index = 0
                    if len(self.app.home_screen.scroll_layout.children) != 0:
                        date = self.app.home_screen.scroll_layout.children[index].act.date.get_date_simple_string()
                        while compare_dates(date, transfer.date.get_date_simple_string()):
                            index += 1
                            if index == len(self.app.home_screen.scroll_layout.children):
                                break
                            date = self.app.home_screen.scroll_layout.children[index].act.date.get_date_simple_string()
                    self.app.home_screen.scroll_layout.add_widget(row, index = index)
                
                if transfer.account_receiving == self.app.home_screen.displayed_account:
                    row = TransferRowWidget(transfer, "received")

                    # create edit transaction btn functionality
                    row.account_btn.bind(on_press=self.app.home_screen.transfer_clicked(transfer))

                    self.app.home_screen.row_widgets[transfer.date.get_date_simple_string()] = row


                    # find correct index position for the new transaction
                    index = 0
                    if len(self.app.home_screen.scroll_layout.children) != 0:
                        date = self.app.home_screen.scroll_layout.children[index].act.date.get_date_simple_string()
                        while compare_dates(date, transfer.date.get_date_simple_string()):
                            index += 1
                            if index == len(self.app.home_screen.scroll_layout.children):
                                break
                            date = self.app.home_screen.scroll_layout.children[index].act.date.get_date_simple_string()
                    self.app.home_screen.scroll_layout.add_widget(row, index = index)


        # if this transfer belongs to displayed in records_screen add it to the relevant dicts
        if date_is_in_interval(transfer.date.get_date_simple_string()[:10], self.start_date_text_field.text, self.end_date_text_field.text):
            if self.displayed_account != None:
                if transfer.account_sending == self.displayed_account or transfer.account_receiving == self.displayed_account:

                    self.displayed_acts_dict[transfer.date.get_date_simple_string()] = transfer
                    if transfer.date.get_date_simple_string() not in self.acts_in_use_dict:
                        self.acts_in_use_dict[transfer.date.get_date_simple_string()] = transfer

                    #self.refresh_screen()


                if transfer.account_sending == self.displayed_account:
                    row = TransferRowWidget(transfer, "sent")

                    # create edit transaction btn functionality
                    row.account_btn.bind(on_press=self.transfer_clicked(transfer))

                    self.row_widgets[transfer.date.get_date_simple_string()] = row


                    # find correct index position for the new transaction
                    index = 0
                    if len(self.scroll_layout.children) != 0:
                        date = self.scroll_layout.children[index].act.date.get_date_simple_string()
                        while compare_dates(date, transfer.date.get_date_simple_string()):
                            index += 1
                            if index == len(self.scroll_layout.children):
                                break
                            date = self.scroll_layout.children[index].act.date.get_date_simple_string()
                    self.scroll_layout.add_widget(row, index = index)
                
                if transfer.account_receiving == self.displayed_account:
                    row = TransferRowWidget(transfer, "received")

                    # create edit transaction btn functionality
                    row.account_btn.bind(on_press=self.transfer_clicked(transfer))

                    self.row_widgets[transfer.date.get_date_simple_string()] = row


                    # find correct index position for the new transaction
                    index = 0
                    if len(self.scroll_layout.children) != 0:
                        date = self.scroll_layout.children[index].act.date.get_date_simple_string()
                        while compare_dates(date, transfer.date.get_date_simple_string()):
                            index += 1
                            if index == len(self.scroll_layout.children):
                                break
                            date = self.scroll_layout.children[index].act.date.get_date_simple_string()
                    self.scroll_layout.add_widget(row, index = index)



        








    def get_transfer_from_storage(self, simple_date_string):
        transfer_info = self.transfers_store.get(simple_date_string)

        days = simple_date_string[:2]
        month = simple_date_string[3:5]
        year = simple_date_string[6:10]
        hour = simple_date_string[11:13]
        minutes = simple_date_string[14:16]
        seconds = simple_date_string[17:]

        date_string = f"{year}-{month}-{days} {hour}:{minutes}:{seconds}.000000"

        date = Date(date_string)
        value = float(transfer_info["value"])
        note = transfer_info["note"]
           

        if "account_sending" in transfer_info and "account_receiving" in transfer_info:
            account_sending = self.app.accounts_screen.accounts_dict[int(transfer_info["account_sending"])]
            account_receiving = self.app.accounts_screen.accounts_dict[int(transfer_info["account_receiving"])]
            
            transfer = Transfer(
                date,
                value,
                note,
                account_sending = account_sending,
                account_receiving = account_receiving
            )

        if "account_sending" not in transfer_info and "account_receiving" in transfer_info:
            account_receiving = self.app.accounts_screen.accounts_dict[int(transfer_info["account_receiving"])]
            
            transfer = Transfer(
                date,
                value,
                note,
                account_receiving = account_receiving,
            )

        if "account_sending" in transfer_info and "account_receiving" not in transfer_info:
            account_sending = self.app.accounts_screen.accounts_dict[int(transfer_info["account_sending"])]
            
            transfer = Transfer(
                date,
                value,
                note,
                account_sending = account_sending,
            )


        return transfer



    def store_transfer(self, transfer):
        date_simple_string = transfer.date.get_date_simple_string()
        month = date_simple_string[3:5]
        year = date_simple_string[6:10]

        if transfer.account_sending == None and transfer.account_receiving != None:
            self.transfers_store.put(
                date_simple_string,
                month = month,
                year = year,
                value = str(transfer.value),
                note = transfer.note,
                account_receiving = str(transfer.account_receiving.number)
            )

        elif transfer.account_sending != None and transfer.account_receiving == None:
            self.transfers_store.put(
                date_simple_string,
                month = month,
                year = year,
                value = str(transfer.value),
                note = transfer.note,
                account_sending = str(transfer.account_sending.number)
            )


        elif transfer.account_sending != None and transfer.account_receiving != None:
            self.transfers_store.put(
                date_simple_string,
                month = month,
                year = year,
                value = str(transfer.value),
                note = transfer.note,
                account_sending = str(transfer.account_sending.number),
                account_receiving = str(transfer.account_receiving.number)
            )




    def store_transaction(self, transaction):
        date_simple_string = transaction.date.get_date_simple_string()
        month = date_simple_string[3:5]
        year = date_simple_string[6:10]

        self.transactions_store.put(
                date_simple_string,
                month = month,
                year = year,
                value = str(transaction.value),
                category = transaction.category.name if transaction.category != None else None,
                subcategory = transaction.subcategory.name if (transaction.category != None and transaction.subcategory != None) else None,
                old_category_name = transaction.old_category_name,
                old_subcategory_name = transaction.old_subcategory_name,
                account = str(transaction.account.number),
                note = transaction.note,                
            )

      



    def remove_transfer(self, transfer_simple_date, account_sending_removed=False, account_receiving_removed=False):
        if not account_sending_removed:
            # return value to account
            transfer_info = self.transfers_store.get(transfer_simple_date)
            if "account_sending" in transfer_info:
                account_number = int(self.transfers_store.get(transfer_simple_date)["account_sending"])
            
                account = self.app.accounts_screen.accounts_dict[account_number]
                transfer_value = float(self.transfers_store.get(transfer_simple_date)["value"])
                new_balance = round(account.balance + transfer_value, 2)
                self.app.accounts_screen.update_balance(
                    self.app.accounts_screen.accounts_dict[account_number],
                    new_balance
                )

        if not account_receiving_removed:
            transfer_info = self.transfers_store.get(transfer_simple_date)
            if "account_receiving" in transfer_info:
                account_number = int(self.transfers_store.get(transfer_simple_date)["account_receiving"])
            
                account = self.app.accounts_screen.accounts_dict[account_number]
                transfer_value = float(self.transfers_store.get(transfer_simple_date)["value"])
                new_balance = round(account.balance - transfer_value, 2)
                self.app.accounts_screen.update_balance(
                    self.app.accounts_screen.accounts_dict[account_number],
                    new_balance
                )


        self.transfers_store.delete(transfer_simple_date)
        if transfer_simple_date in self.row_widgets:
            self.scroll_layout.remove_widget(
                self.row_widgets[transfer_simple_date]
            )

            del self.row_widgets[transfer_simple_date]
            del self.displayed_acts_dict[transfer_simple_date]
            del self.acts_in_use_dict[transfer_simple_date]
        
            
        if transfer_simple_date in self.app.home_screen.row_widgets:
            self.app.home_screen.scroll_layout.remove_widget(
                self.app.home_screen.row_widgets[transfer_simple_date]
            )
            del self.app.home_screen.row_widgets[transfer_simple_date]
            del self.app.home_screen.displayed_acts_dict[transfer_simple_date]
            if transfer_simple_date in self.acts_in_use_dict:
                del self.acts_in_use_dict[transfer_simple_date]




    def remove_transaction(self, transaction_simple_date, account_removed=False):
        
        if not account_removed:
            # return value to account
            account_number = int(self.transactions_store.get(transaction_simple_date)["account"])
            account = self.app.accounts_screen.accounts_dict[account_number]
            transaction_value = float(self.transactions_store.get(transaction_simple_date)["value"])
            new_balance = round(account.balance - transaction_value, 2)
            self.app.accounts_screen.update_balance(
                self.app.accounts_screen.accounts_dict[account_number],
                new_balance
            )


        self.transactions_store.delete(transaction_simple_date)
        if transaction_simple_date in self.row_widgets:
            self.scroll_layout.remove_widget(
                self.row_widgets[transaction_simple_date]
            )

            del self.row_widgets[transaction_simple_date]
            del self.displayed_acts_dict[transaction_simple_date]
            del self.acts_in_use_dict[transaction_simple_date]
        
            
        if transaction_simple_date in self.app.home_screen.row_widgets:
            self.app.home_screen.scroll_layout.remove_widget(
                self.app.home_screen.row_widgets[transaction_simple_date]
            )
            del self.app.home_screen.row_widgets[transaction_simple_date]
            del self.app.home_screen.displayed_acts_dict[transaction_simple_date]
            if transaction_simple_date in self.acts_in_use_dict:
                del self.acts_in_use_dict[transaction_simple_date]
            

    



    def remove_transaction_from_storage(self, transaction):
        date_simple_string = transaction.date.get_date_simple_string()
        self.transactions_store.delete(date_simple_string)



    def edit_transfer(self, transfer, changes_dict):
        '''
        The changes_dict has keys which are transfer attributes that are changing, and the respective value is the new value for the attribute.

        If the date has changed, changes_dict should have a key "simple_date_string" where the value is the new simple_date_string

        changes_dict should have the following form
        {
        "simple_date_string": "dd/mm/yyyy hh:mm:ss",
        "value": float,
        "note": string,
        "account_sending": account_sending.number or None,
        "account_receiving": account_receiving.number or None
        }

        Note:  Unlike in edit_transaction the keys "value", "account_sending" and "account_receiving" are mandatory
        '''
        # we first delete the transaction from storage
        transfer_simple_date = transfer.date.get_date_simple_string()
        self.transfers_store.delete(transfer_simple_date)

        if "simple_date_string" in changes_dict:
            new_date = transfer.date.parse_string(changes_dict["simple_date_string"])
            transfer.date = new_date
            new_transfer_simple_date = transfer.date.get_date_simple_string()

            # change the location of this transfer in the relevant dictionaries
            if transfer_simple_date in self.displayed_acts_dict:
                del self.displayed_acts_dict[transfer_simple_date]
                
            if transfer_simple_date in self.app.home_screen.displayed_acts_dict:
                del self.app.home_screen.displayed_acts_dict[transfer_simple_date]
                
            if transfer_simple_date in self.acts_in_use_dict:
                del self.acts_in_use_dict[transfer_simple_date]
                



        if changes_dict["account_sending"] != None:
            new_account_sending = self.app.accounts_screen.accounts_dict[changes_dict["account_sending"]]
        else:
            new_account_sending = None

        if changes_dict["account_receiving"] != None:
            new_account_receiving = self.app.accounts_screen.accounts_dict[changes_dict["account_receiving"]]
        else:
            new_account_receiving = None

        # give old value back to old_account_sending
        if transfer.account_sending != None:
            self.app.accounts_screen.update_balance(
                transfer.account_sending,
                transfer.account_sending.balance + transfer.value
            )
        
        # remove old value from the old account receiving
        if transfer.account_receiving != None:
            self.app.accounts_screen.update_balance(
                transfer.account_receiving,
                transfer.account_receiving.balance - transfer.value
            )

        # remove new value from new_account_sending
        new_value = round(changes_dict["value"], 2)


        if new_account_sending != None:
            self.app.accounts_screen.update_balance(
                new_account_sending,
                round((new_account_sending.balance if new_account_sending != None else 0) - new_value, 2)
            )

        # give new value to new_account_receiving
        if new_account_receiving != None:
            self.app.accounts_screen.update_balance(
                new_account_receiving,
                round((new_account_receiving.balance if new_account_receiving != None else 0) + new_value, 2)
            )

        
        # update the accounts attributes
        transfer.account_sending = new_account_sending
        transfer.account_receiving = new_account_receiving

        # update the transfer value
        transfer.value = new_value



        if "note" in changes_dict:
            transfer.note = changes_dict["note"]
        

        
        # place back in storage after changes have been made
        self.store_transfer(transfer)




        if transfer_simple_date in self.app.home_screen.row_widgets:
            self.app.home_screen.scroll_layout.remove_widget(
                self.app.home_screen.row_widgets[transfer_simple_date]
            )
            del self.app.home_screen.row_widgets[transfer_simple_date]

        if transfer_simple_date in self.row_widgets:
            self.scroll_layout.remove_widget(
                self.row_widgets[transfer_simple_date]
            )
            del self.row_widgets[transfer_simple_date]

        # if this transfer belongs to displayed in records_screen add it to the relevant dicts
        if self.displayed_account != None:
            if date_is_in_interval(transfer.date.get_date_simple_string()[:10], self.start_date_text_field.text, self.end_date_text_field.text):
                if transfer.account_sending == self.displayed_account or transfer.account_receiving == self.displayed_account:
                    self.acts_in_use_dict[transfer.date.get_date_simple_string()] = transfer
                    self.displayed_acts_dict[transfer.date.get_date_simple_string()] = transfer
                
                if transfer.account_sending == self.displayed_account:
                    row = TransferRowWidget(transfer, "sent")

                    # create edit transaction btn functionality
                    row.account_btn.bind(on_press=self.transfer_clicked(transfer))

                    self.row_widgets[transfer.date.get_date_simple_string()] = row


                    # find correct index position for the new transaction
                    index = 0
                    if len(self.scroll_layout.children) != 0:
                        date = self.scroll_layout.children[index].act.date.get_date_simple_string()
                        while compare_dates(date, transfer.date.get_date_simple_string()):
                            index += 1
                            if index == len(self.scroll_layout.children):
                                break
                            date = self.scroll_layout.children[index].act.date.get_date_simple_string()
                    self.scroll_layout.add_widget(row, index = index)

                if transfer.account_receiving == self.displayed_account:
                    row = TransferRowWidget(transfer, "received")

                    # create edit transaction btn functionality
                    row.account_btn.bind(on_press=self.transfer_clicked(transfer))

                    self.row_widgets[transfer.date.get_date_simple_string()] = row


                    # find correct index position for the new transaction
                    index = 0
                    if len(self.scroll_layout.children) != 0:
                        date = self.scroll_layout.children[index].act.date.get_date_simple_string()
                        while compare_dates(date, transfer.date.get_date_simple_string()):
                            index += 1
                            if index == len(self.scroll_layout.children):
                                break
                            date = self.scroll_layout.children[index].act.date.get_date_simple_string()
                    self.scroll_layout.add_widget(row, index = index)

            

        # if this transfer should be displayed in home_screen add it to the relevant dicts
        if (int(transfer.date.month), int(transfer.date.year)) == self.app.home_screen.displayed_month:
            if self.app.home_screen.displayed_account != None:
                if transfer.account_sending == self.app.home_screen.displayed_account or transfer.account_receiving == self.app.home_screen.displayed_account:
                    self.displayed_acts_dict[transfer.date.get_date_simple_string()] = transfer
                    if transfer.date.get_date_simple_string() not in self.acts_in_use_dict:
                        self.acts_in_use_dict[transfer.date.get_date_simple_string()] = transfer

                if transfer.account_sending == self.app.home_screen.displayed_account:
                    row = TransferRowWidget(transfer, "sent")

                    # create edit transaction btn functionality
                    row.account_btn.bind(on_press=self.app.home_screen.transfer_clicked(transfer))

                    self.app.home_screen.row_widgets[transfer.date.get_date_simple_string()] = row


                    # find correct index position for the new transaction
                    index = 0
                    if len(self.app.home_screen.scroll_layout.children) != 0:
                        date = self.app.home_screen.scroll_layout.children[index].act.date.get_date_simple_string()
                        while compare_dates(date, transfer.date.get_date_simple_string()):
                            index += 1
                            if index == len(self.app.home_screen.scroll_layout.children):
                                break
                            date = self.app.home_screen.scroll_layout.children[index].act.date.get_date_simple_string()
                    self.app.home_screen.scroll_layout.add_widget(row, index = index)
                
                if transfer.account_receiving == self.app.home_screen.displayed_account:
                    row = TransferRowWidget(transfer, "received")

                    # create edit transaction btn functionality
                    row.account_btn.bind(on_press=self.app.home_screen.transfer_clicked(transfer))

                    self.app.home_screen.row_widgets[transfer.date.get_date_simple_string()] = row


                    # find correct index position for the new transaction
                    index = 0
                    if len(self.app.home_screen.scroll_layout.children) != 0:
                        date = self.app.home_screen.scroll_layout.children[index].act.date.get_date_simple_string()
                        while compare_dates(date, transfer.date.get_date_simple_string()):
                            index += 1
                            if index == len(self.app.home_screen.scroll_layout.children):
                                break
                            date = self.app.home_screen.scroll_layout.children[index].act.date.get_date_simple_string()
                    self.app.home_screen.scroll_layout.add_widget(row, index = index)


       


    def edit_transaction(self, transaction, changes_dict):
        '''
        The changes_dict has keys which are transaction attributes that are changing, and the respective value is the new value for the attribute.

        If the date has changed, changes_dict should have a key "simple_date_string" where the value is the new simple_date_string

        Note: "recurrent" should not be in changes_dict

        changes_dict should have the following form
        {
        "simple_date_string": "dd/mm/yyyy hh:mm:ss",
        "value": float,
        "category": category_name,
        "subcategory": subcategory_name or None,
        "note": sting,
        "account": account_number_int,
        "old_category_name": string or None,
        "old_subcategory_name": string or None
        }

        '''
        
        # we first delete the transaction from storage
        transaction_simple_date = transaction.date.get_date_simple_string()
        self.transactions_store.delete(transaction_simple_date)


        # change the location of this transaction in the relevant dictionaries
        if transaction_simple_date in self.displayed_acts_dict:
            del self.displayed_acts_dict[transaction_simple_date]
            #self.displayed_acts_dict[new_transaction_simple_date] = transaction 
        if transaction_simple_date in self.acts_in_use_dict:
            del self.acts_in_use_dict[transaction_simple_date]
            #self.acts_in_use_dict[new_transaction_simple_date] = transaction 
        if transaction_simple_date in self.app.home_screen.displayed_acts_dict:
            del self.app.home_screen.displayed_acts_dict[transaction_simple_date]
            #self.app.home_screen.displayed_acts_dict[new_transaction_simple_date] = transaction


        if "simple_date_string" in changes_dict:
            new_date = transaction.date.parse_string(changes_dict["simple_date_string"])
            transaction.date = new_date
            #new_transaction_simple_date = transaction.date.get_date_simple_string()

            


            
            

        if "value" in changes_dict:
            new_value = round(changes_dict["value"], 2)

            # return old value to old account
            self.app.accounts_screen.update_balance(
                transaction.account,
                round(transaction.account.balance - transaction.value, 2)
            )

            transaction.value = new_value

            # update balance of new account with new value
            if "account" in changes_dict:
                new_account = self.app.accounts_screen.accounts_dict[changes_dict["account"]]
                new_balance = round(new_account.balance + transaction.value, 2)
                self.app.accounts_screen.update_balance(new_account, new_balance)
            

        if "category" in changes_dict:
            if changes_dict["category"] != None:
                new_category = self.app.categories_screen.categories_dict[changes_dict["category"]]
            else:
                new_category = None
            transaction.category = new_category

        if "subcategory" in changes_dict:
            if changes_dict["subcategory"] != None:
                new_subcategory = transaction.category.subcategories[changes_dict["subcategory"]]
            else:
                new_subcategory = None
            transaction.subcategory = new_subcategory
        
        if "account" in changes_dict:
            new_account = self.app.accounts_screen.accounts_dict[changes_dict["account"]]
            transaction.account = new_account

        if "note" in changes_dict:
            transaction.note = changes_dict["note"]

        if "old_category_name" in changes_dict:
            transaction.old_category_name = changes_dict["old_category_name"]
        
        if "old_subcategory_name" in changes_dict:
            transaction.old_subcategory_name = changes_dict["old_subcategory_name"]
        

        
        # place back in storage after changes have been made
        self.store_transaction(transaction)



        if transaction_simple_date in self.app.home_screen.row_widgets:
            self.app.home_screen.scroll_layout.remove_widget(
                self.app.home_screen.row_widgets[transaction_simple_date]
            )
            del self.app.home_screen.row_widgets[transaction_simple_date]

        if transaction_simple_date in self.row_widgets:
            self.scroll_layout.remove_widget(
                self.row_widgets[transaction_simple_date]
            )
            del self.row_widgets[transaction_simple_date]


        # if this transfer belongs to displayed in records_screen add it to the relevant dicts
        if date_is_in_interval(transaction.date.get_date_simple_string()[:10], self.start_date_text_field.text, self.end_date_text_field.text):
            if transaction.account.number == int(self.change_account_btn.text.split(".")[0]):
                self.acts_in_use_dict[transaction.date.get_date_simple_string()] = transaction
                self.displayed_acts_dict[transaction.date.get_date_simple_string()] = transaction

                
                row = TransactionRowWidget(transaction)

                # create edit transaction btn functionality
                row.category_btn.bind(on_press=self.transaction_clicked(transaction))

                self.row_widgets[transaction.date.get_date_simple_string()] = row


                # find correct index position for the new transaction
                index = 0
                if len(self.scroll_layout.children) != 0:
                    date = self.scroll_layout.children[index].act.date.get_date_simple_string()
                    while compare_dates(date, transaction.date.get_date_simple_string()):
                        index += 1
                        if index == len(self.scroll_layout.children):
                            break
                        date = self.scroll_layout.children[index].act.date.get_date_simple_string()
                self.scroll_layout.add_widget(row, index = index)


        # if this transfer should be displayed in home_screen add it to the relevant dicts
        if (int(transaction.date.month), int(transaction.date.year)) == self.app.home_screen.displayed_month:
            if transaction.account.number == int(self.app.home_screen.change_account_btn.text.split(".")[0]):
                self.app.home_screen.displayed_acts_dict[transaction.date.get_date_simple_string()] = transaction
                if transaction.date.get_date_simple_string() not in self.acts_in_use_dict:
                    self.acts_in_use_dict[transaction.date.get_date_simple_string()] = transaction
                
                
                row = TransactionRowWidget(transaction)

                # create edit transaction btn functionality
                row.category_btn.bind(on_press=self.app.home_screen.transaction_clicked(transaction))

                self.app.home_screen.row_widgets[transaction.date.get_date_simple_string()] = row


                # find correct index position for the new transaction
                index = 0
                if len(self.app.home_screen.scroll_layout.children) != 0:
                    date = self.app.home_screen.scroll_layout.children[index].act.date.get_date_simple_string()
                    while compare_dates(date, transaction.date.get_date_simple_string()):
                        index += 1
                        if index == len(self.app.home_screen.scroll_layout.children):
                            break
                        date = self.app.home_screen.scroll_layout.children[index].act.date.get_date_simple_string()
                self.app.home_screen.scroll_layout.add_widget(row, index = index)

        

       

      




    



    def get_transaction_from_storage(self, simple_date_string):
        transaction_info = self.transactions_store.get(simple_date_string)

        days = simple_date_string[:2]
        month = simple_date_string[3:5]
        year = simple_date_string[6:10]
        hour = simple_date_string[11:13]
        minutes = simple_date_string[14:16]
        seconds = simple_date_string[17:]

        date_string = f"{year}-{month}-{days} {hour}:{minutes}:{seconds}.000000"

        date = Date(date_string)
        
        if transaction_info["category"] in self.app.categories_screen.categories_dict:
            category = self.app.categories_screen.categories_dict[transaction_info["category"]]
        else:
            category = None

        account = self.app.accounts_screen.accounts_dict[int(transaction_info["account"])]

        if category == None:
            subcategory = None
        else:
            if transaction_info["subcategory"] not in category.subcategories:
                subcategory = None
            else:
                subcategory = category.subcategories[transaction_info["subcategory"]]
            
        transaction = Transaction(
            date,
            float(transaction_info["value"]),
            category,
            account,
            transaction_info["note"],
            subcategory=subcategory,
            old_category_name=transaction_info["old_category_name"],
            old_subcategory_name=transaction_info["old_subcategory_name"]
        )

        
        return transaction
    


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
    

    def _validate_date(self, date):
        # return true if date is valid, ie has the format "dd/mm/yyyy" and corresponds to a real date
        # for example, 29/02/2001 is not a real date because 2001 was not a leap year
        calendar = {
            1: 31,
            2: 28,
            3: 31,
            4: 30,
            5: 31,
            6: 30,
            7: 31,
            8: 31,
            9: 30,
            10: 31,
            11: 30,
            12: 31
        }
        leap_calendar = {
            1: 31,
            2: 29,
            3: 31,
            4: 30,
            5: 31,
            6: 30,
            7: 31,
            8: 31,
            9: 30,
            10: 31,
            11: 30,
            12: 31
        }

        split_date = date.split("/")
        try:
            days = split_date[0]
            month = split_date[1]
            year = split_date[2]
            

            if len(days) != 2 or len(month) != 2 or len(year) != 4:
                return False
            
            days = int(days)
            month = int(month)
            year = int(year)


            if year < 0 or year > 9999:
                return False
            
            if month < 1 or month > 12:
                return False
            
            if self.is_leap_year(year):
                if days < 1 or days > leap_calendar[month]:
                    return False

            if not self.is_leap_year(year):
                if days < 1 or days > calendar[month]:
                    return False
                
            return True           
            
        except:
            return False


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