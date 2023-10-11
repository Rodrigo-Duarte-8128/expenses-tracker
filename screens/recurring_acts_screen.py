from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex
from kivy.uix.button import Button
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from datas.date import get_date_from_simple_date, date_is_in_interval
from datas.transaction import RecurringTransaction, RecurringTransfer
from row_widgets.recurring_transaction_row_widget import RecurringTransactionRowWidget
from row_widgets.recurring_transfer_row_widget import RecurringTransferRowWidget
from screens.accounts_screens.choose_account_screen import ChooseAccountScreen
from screens.transactions_screens.new_recurring_transaction_screen import NewRecurringTransactionScreen
from screens.transactions_screens.edit_recurring_transaction_screen import EditRecurringTransactionScreen
from screens.transfers_screens.new_recurring_transfer_screen import NewRecurringTransferScreen
from screens.transfers_screens.edit_recurring_transfer_screen import EditRecurringTransferScreen



red = hex("#E63946")
cream = hex("#F1FAEE")
light_teal = hex("#A8DADC")
blue = hex("#457B9D")
dark_blue = hex("#1D3557")
green = hex("#84a98c")





class RecurringActsScreen(MDScreen):
    def __init__(self, app, **kwargs):
        super(RecurringActsScreen, self).__init__(**kwargs)


        self.app = app

        self.recurring_acts_dict = {} # this dictionary holds all the recurring acts from recurring_transfers_store and recurring_transactions_store
        self.displayed_recurring_acts_dict = {}

        self.row_widgets = {} 

        self.recurring_transfers_store = JsonStore("recurring_transfers.json")
        self.recurring_transactions_store = JsonStore("recurring_transactions.json")


        # build recurring_acts_dict
        for name in self.recurring_transfers_store.keys():
            recurring_transfer = self.get_recurring_transfer_from_storage(name)
            self.recurring_acts_dict[name] = recurring_transfer
        
        for name in self.recurring_transactions_store.keys():
            recurring_transaction = self.get_recurring_transaction_from_storage(name)
            self.recurring_acts_dict[name] = recurring_transaction

        

        self.layout = MDFloatLayout()

        self.window_width, self.window_height = Window.size



        # account functionality
        self.account_label = MDLabel(
            text = "Account:",
            pos_hint = {"x": 0, "y": 0.82},
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
            pos_hint={"x": 0.55, "y": 0.82},
            background_normal = ""
        )
        self.layout.add_widget(self.change_account_btn)
        self.change_account_btn.bind(on_press=self.change_account())



        # build displayed_recurring_acts
        if self.displayed_account != None:
            for name in self.recurring_acts_dict:
                act = self.recurring_acts_dict[name]
                if type(act) == RecurringTransfer:
                    if act.account_receiving != None:
                        if act.account_receiving.number == self.displayed_account.number:                   
                            self.displayed_recurring_acts_dict[name] = act

                    
                    if act.account_sending != None:
                        if act.account_sending.number == self.displayed_account.number:
                            self.displayed_recurring_acts_dict[name] = act

                elif type(act) == RecurringTransaction:
                    if act.account.number == self.displayed_account.number:
                        self.displayed_recurring_acts_dict[name] = act


       



        # Create Transactions Scroll View Headers
        self.name_label = MDRaisedButton(
            text = "Name",
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            md_bg_color_disabled = blue,
            size_hint = (0.2, 0.05),
            pos_hint = {"x": 0, "y": 0.68},
            elevation = 0,
            _radius = 1
        )
        self.layout.add_widget(self.name_label)

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





        name_list = list(self.displayed_recurring_acts_dict)
        name_list.sort()

        for name in name_list:
            act = self.displayed_recurring_acts_dict[name]
            if type(act) == RecurringTransaction:

                row = RecurringTransactionRowWidget(act)

                # create edit recurring transaction btn functionality
                row.category_btn.bind(on_press=self.recurring_transaction_clicked(act))

                self.row_widgets[name] = row
                self.scroll_layout.add_widget(row)

            if type(act) == RecurringTransfer:
                if act.account_sending != None:
                    if act.account_sending.number == int(default.split(".")[0]):
                        # create recurring transfer row widget
                        row = RecurringTransferRowWidget(act)

                        # create edit recurring transfer btn functionality
                        row.account_btn.bind(on_press=self.recurring_transfer_clicked(act))

                        self.row_widgets[name] = row
                        self.scroll_layout.add_widget(row)

                if act.account_receiving != None:
                    if act.account_receiving.number == int(default.split(".")[0]):
                        # create recurring transfer row widget
                        row = RecurringTransferRowWidget(act)

                        # create edit recurring transfer btn functionality
                        row.account_btn.bind(on_press=self.recurring_transfer_clicked(act))

                        self.row_widgets[name] = row
                        self.scroll_layout.add_widget(row)


        # Create Scroll View
        self.scroll_view = MDScrollView(
            size_hint = (1, 0.62),
            pos_hint = {"x": 0, "y": 0.06},
            bar_width = 10
        )
        self.scroll_view.add_widget(self.scroll_layout)
        self.layout.add_widget(self.scroll_view)



        # create button to update recurring acts
        self.build_missing_acts_btn = MDRaisedButton(
            text = "Build Missing Acts",
            md_bg_color = dark_blue,
            size_hint = (0.5, 0.05),
            pos_hint = {"x": 0.25, "y": 0.74},
            on_press = self.build_missing_acts()
        )
        self.layout.add_widget(self.build_missing_acts_btn)



        # Create new recurring transaction button
        self.new_recurring_transaction_btn = MDRaisedButton(
            text = "New Transaction",
            size_hint = (0.45, 0.04),
            pos_hint = {"x": 0.525, "y": 0.005},
            md_bg_color = red,
            on_press = self.new_recurring_transaction_clicked()
        )
        self.layout.add_widget(self.new_recurring_transaction_btn)


        # Create new recurring transfer button
        self.new_recurring_transfer_btn= MDRaisedButton(
            text = "New Transfer",
            size_hint = (0.45, 0.04),
            pos_hint = {"x": 0.025, "y": 0.005},
            md_bg_color = green,
            on_press = self.new_recurring_transfer_clicked()
        )
        self.layout.add_widget(self.new_recurring_transfer_btn)


        
        self.add_widget(self.layout)




    def build_missing_acts(self):
        def build(instance):
            self.app.records_screen.build_missing_recurring_transfers()
            self.app.records_screen.build_missing_recurring_transactions()

            # check if there are acts in storage that should be displayed in the home screen or the records screen
            month_year = self.app.home_screen.displayed_month
            month = str(month_year[0])
            year = str(month_year[1])
            if len(month) == 1:
                month = f"0{month}"
            if len(year) < 4:
                zeros_num = 4 - len(year)
                year = zeros_num*"0" + year


            for transaction_simple_date in self.app.records_screen.transactions_store.keys():
                if transaction_simple_date not in self.app.records_screen.acts_in_use_dict:
                    transaction = self.app.records_screen.get_transaction_from_storage(transaction_simple_date)
                    if transaction.account == self.app.home_screen.displayed_account:
                        if transaction.date.month == month and transaction.date.year == year:
                            self.app.home_screen.displayed_acts_dict[transaction_simple_date] = transaction
                            self.app.records_screen.acts_in_use_dict[transaction_simple_date] = transaction

                    if transaction.account == self.app.records_screen.displayed_account:
                        start_simple_date = self.app.records_screen.start_date_text_field.text
                        end_simple_date = self.app.records_screen.end_date_text_field.text
                        if date_is_in_interval(transaction_simple_date[:10], start_simple_date, end_simple_date):
                            self.app.records_screen.displayed_acts_dict[transaction_simple_date] = transaction
                            if transaction_simple_date not in self.app.records_screen.acts_in_use_dict:
                                self.app.records_screen.acts_in_use_dict[transaction_simple_date] = transaction
                        
            
            for transfer_simple_date in self.app.records_screen.transfers_store.keys():
                if transfer_simple_date not in self.app.records_screen.acts_in_use_dict:
                    transfer = self.app.records_screen.get_transfer_from_storage(transfer_simple_date)

                    if self.app.home_screen.displayed_account != None:
                        if transfer.account_sending == self.app.home_screen.displayed_account or transfer.account_receiving == self.app.home_screen.displayed_account:
                            if transfer.date.month == month and transfer.date.year == year:
                                self.app.home_screen.displayed_acts_dict[transfer_simple_date] = transfer
                                self.app.records_screen.acts_in_use_dict[transfer_simple_date] = transfer

                    if self.app.records_screen.displayed_account != None:
                        if transfer.account_sending == self.app.records_screen.displayed_account or transfer.account_receiving == self.app.records_screen.displayed_account:
                            start_simple_date = self.app.records_screen.start_date_text_field.text
                            end_simple_date = self.app.records_screen.end_date_text_field.text
                            if date_is_in_interval(transfer_simple_date[:10], start_simple_date, end_simple_date):
                                self.app.records_screen.displayed_acts_dict[transfer_simple_date] = transfer
                                if transfer_simple_date not in self.app.records_screen.acts_in_use_dict:
                                    self.app.records_screen.acts_in_use_dict[transfer_simple_date] = transfer
        


            # refresh home screen
            self.app.home_screen.refresh_row_widgets()

            # refresh records screen
            self.app.records_screen.refresh_screen()

           
            
        return build



    def refresh_current_account(self):
        # refresh current account from accounts_screen.current_account_dict
        if self.app.accounts_screen.current_account_dict == {}:
            self.change_account_btn.text = "Choose Account"

        else:
            current_account = list(self.app.accounts_screen.current_account_dict.values())[0]
            self.change_account_btn.text = f"{current_account.number}. {current_account.name}"

        self.refresh_row_widgets()



    def refresh_row_widgets(self):
        '''
        rebuild row widgets and displayed_recurring_acts_dict using recurring_acts_dict
        '''
        
        
        # remove current row widgets from the scroll view
        for name in self.row_widgets:
            self.scroll_layout.remove_widget(self.row_widgets[name])

        # reset row_widgets dict
        self.row_widgets = {}

        # reset displayed_acts_dict
        self.displayed_recurring_acts_dict = {}


        for name in self.recurring_acts_dict:
            act = self.recurring_acts_dict[name]
            if self.displayed_account != None:
                if type(act) == RecurringTransfer:
                    if act.account_receiving != None:
                        if act.account_receiving.number == self.displayed_account.number:                   
                            self.displayed_recurring_acts_dict[name] = act

                    if act.account_sending != None:
                        if act.account_sending.number == self.displayed_account.number:
                            self.displayed_recurring_acts_dict[name] = act

                elif type(act) == RecurringTransaction:
                    if act.account.number == self.displayed_account.number:
                        self.displayed_recurring_acts_dict[name] = act
        
        # use displayed_recurring_acts_dict to build row widgets
        name_list = list(self.displayed_recurring_acts_dict)
        name_list.sort()

        for name in name_list:
            act = self.displayed_recurring_acts_dict[name]
            if type(act) == RecurringTransaction:

                row = RecurringTransactionRowWidget(act)

                # create edit recurring transaction btn functionality
                row.category_btn.bind(on_press=self.recurring_transaction_clicked(act))

                self.row_widgets[name] = row
                self.scroll_layout.add_widget(row)

            if type(act) == RecurringTransfer:
                if act.account_sending != None:
                    if act.account_sending.number == self.displayed_account.number:
                        # create recurring transfer row widget
                        row = RecurringTransferRowWidget(act)

                        # create edit recurring transfer btn functionality
                        row.account_btn.bind(on_press=self.recurring_transfer_clicked(act))

                        self.row_widgets[name] = row
                        self.scroll_layout.add_widget(row)

                if act.account_receiving != None:
                    if act.account_receiving.number == self.displayed_account.number:
                        # create recurring transfer row widget
                        row = RecurringTransferRowWidget(act)

                        # create edit recurring transfer btn functionality
                        row.account_btn.bind(on_press=self.recurring_transfer_clicked(act))

                        self.row_widgets[name] = row
                        self.scroll_layout.add_widget(row)



    def new_recurring_transfer_clicked(self):
        def click(instance):
            self.app.new_recurring_transfer_screen = NewRecurringTransferScreen(self.app, name="new_recurring_transfer_screen")
            self.app.screen_manager.add_widget(self.app.new_recurring_transfer_screen)



            self.app.transition_diagram.add_node(
                "new_recurring_transfer_screen",
                root_screen_node = self.app.recurring_acts_screen_node,
                left_node = self.app.recurring_acts_screen_node
            )

            self.app.switch_screen("new_recurring_transfer_screen")(instance)
        return click



    def new_recurring_transaction_clicked(self):
        def click(instance):
            self.app.new_recurring_transaction_screen = NewRecurringTransactionScreen(self.app, name="new_recurring_transaction_screen")
            self.app.screen_manager.add_widget(self.app.new_recurring_transaction_screen)

            self.app.transition_diagram.add_node(
                "new_recurring_transaction_screen",
                root_screen_node = self.app.recurring_acts_screen_node,
                left_node = self.app.recurring_acts_screen_node
            )

            self.app.switch_screen("new_recurring_transaction_screen")(instance)
        return click



    def recurring_transfer_clicked(self, recurring_transfer):
        def click(instance):
            self.app.edit_recurring_transfer_screen = EditRecurringTransferScreen(self.app, recurring_transfer, name="edit_recurring_transfer_screen")
            self.app.screen_manager.add_widget(self.app.edit_recurring_transfer_screen)

            self.app.transition_diagram.add_node(
                "edit_recurring_transfer_screen",
                root_screen_node = self.app.recurring_acts_screen_node,
                left_node = self.app.recurring_acts_screen_node
            )

            self.app.switch_screen("edit_recurring_transfer_screen")(instance)
        return click



    def recurring_transaction_clicked(self, recurring_transaction):
        def click(instance):
            self.app.edit_recurring_transaction_screen = EditRecurringTransactionScreen(self.app, recurring_transaction, name="edit_recurring_transaction_screen")
            self.app.screen_manager.add_widget(self.app.edit_recurring_transaction_screen)

            self.app.transition_diagram.add_node(
                "edit_recurring_transaction_screen",
                root_screen_node = self.app.recurring_acts_screen_node,
                left_node = self.app.recurring_acts_screen_node
            )

            self.app.switch_screen("edit_recurring_transaction_screen")(instance)
        return click
    


    def change_account(self):
        def change(instance):
            self.app.choose_account_screen = ChooseAccountScreen(self.app, "recurring_acts_screen", instance, name="choose_account_screen")
            self.app.screen_manager.add_widget(self.app.choose_account_screen)

            # add screen to transition diagram
            self.app.transition_diagram.add_node("choose_account_screen", root_screen_node = self.app.home_screen_node, left_node = self.app.home_screen_node)

            self.app.switch_screen("choose_account_screen")(instance)
        return change



    def store_recurring_transaction(self, recurring_transaction):
        self.recurring_transactions_store.put(
            recurring_transaction.name,
            identifier = str(recurring_transaction.identifier),
            start_simple_date = recurring_transaction.start_date.get_date_simple_string(),
            month_day = str(recurring_transaction.month_day),
            value = str(recurring_transaction.value),
            category = recurring_transaction.category.name if recurring_transaction.category != None else None,
            note = recurring_transaction.note,
            account = str(recurring_transaction.account.number),
            end_simple_date = recurring_transaction.end_date.get_date_simple_string() if recurring_transaction.end_date != None else None,
            subcategory = recurring_transaction.subcategory.name if recurring_transaction.subcategory != None else None,
            old_category_name = recurring_transaction.old_category_name,
            old_subcategory_name = recurring_transaction.old_subcategory_name,
            instantiation_dates_list = recurring_transaction.instantiation_dates_list
        )



    def store_recurring_transfer(self, recurring_transfer):
        self.recurring_transfers_store.put(
            recurring_transfer.name,
            identifier = str(recurring_transfer.identifier),
            start_simple_date = recurring_transfer.start_date.get_date_simple_string(),
            month_day = str(recurring_transfer.month_day),
            value = str(recurring_transfer.value),
            note = recurring_transfer.note,
            end_simple_date = recurring_transfer.end_date.get_date_simple_string() if recurring_transfer.end_date != None else None,
            account_sending = str(recurring_transfer.account_sending.number) if recurring_transfer.account_sending != None else None,
            account_receiving = str(recurring_transfer.account_receiving.number) if recurring_transfer.account_receiving != None else None,
            instantiation_dates_list = recurring_transfer.instantiation_dates_list
        )



    def get_recurring_transaction_from_storage(self, name):
        recurring_transaction_info = self.recurring_transactions_store.get(name)

        identifier = int(recurring_transaction_info["identifier"])

        start_date = get_date_from_simple_date(recurring_transaction_info["start_simple_date"])

        
        if recurring_transaction_info["end_simple_date"] != None:
            end_date = get_date_from_simple_date(recurring_transaction_info["end_simple_date"])
        else:
            end_date = None
        
        month_day = int(recurring_transaction_info["month_day"])
        value = float(recurring_transaction_info["value"])

        if recurring_transaction_info["category"] != None:
            category = self.app.categories_screen.categories_dict[recurring_transaction_info["category"]]
        else:
            category = None

        note = recurring_transaction_info["note"]

        account = self.app.accounts_screen.accounts_dict[int(recurring_transaction_info["account"])]

        if recurring_transaction_info["subcategory"] != None:
            subcategory = category.subcategories[recurring_transaction_info["subcategory"]]
        else:
            subcategory = None

        old_category_name = recurring_transaction_info["old_category_name"] 
        old_subcategory_name = recurring_transaction_info["old_subcategory_name"]


        recurring_transaction = RecurringTransaction(
            identifier,
            name,
            start_date,
            month_day,
            value,
            category,
            note,
            account,
            end_date=end_date,
            subcategory = subcategory,
            old_category_name = old_category_name,
            old_subcategory_name= old_subcategory_name,
            instantiation_dates_list = recurring_transaction_info["instantiation_dates_list"]
        )

        return recurring_transaction
    


    def get_recurring_transfer_from_storage(self, name):
        recurring_transfer_info = self.recurring_transfers_store.get(name)

        identifier = int(recurring_transfer_info["identifier"])

        start_date = get_date_from_simple_date(recurring_transfer_info["start_simple_date"])

        month_day = int(recurring_transfer_info["month_day"])

        value = float(recurring_transfer_info["value"])

        note = recurring_transfer_info["note"]

        if recurring_transfer_info["end_simple_date"] != None:
            end_date = get_date_from_simple_date(recurring_transfer_info["end_simple_date"])
        else:
            end_date = None

        if recurring_transfer_info["account_sending"] != None:
            account_sending = self.app.accounts_screen.accounts_dict[int(recurring_transfer_info["account_sending"])]
        else:
            account_sending = None
        
        if recurring_transfer_info["account_receiving"] != None:
            account_receiving = self.app.accounts_screen.accounts_dict[int(recurring_transfer_info["account_receiving"])]
        else:
            account_receiving = None

        recurring_transfer = RecurringTransfer(
            identifier,
            name,
            start_date,
            month_day,
            value,
            note,
            end_date = end_date,
            account_sending = account_sending,
            account_receiving = account_receiving,
            instantiation_dates_list = recurring_transfer_info["instantiation_dates_list"]
        )

        return recurring_transfer



    def get_new_identifier(self):
        '''
        returns the first int that is not in use among the identifiers in recurring_acts_dict
        '''
        used_identifiers = [recurring_act.identifier for recurring_act in self.recurring_acts_dict.values()]

        first_non_used_num = 0
        while first_non_used_num in used_identifiers:
            first_non_used_num += 1

        return first_non_used_num
    


    def remove_recurring_act(self, recurring_act):
        # remove from storage
        if type(recurring_act) == RecurringTransaction:
            self.recurring_transactions_store.delete(recurring_act.name)
        elif type(recurring_act) == RecurringTransfer:
            self.recurring_transfers_store.delete(recurring_act.name)

        # if its displayed remove from scroll view and displayed dict
        if recurring_act.name in self.displayed_recurring_acts_dict:
            row = self.row_widgets[recurring_act.name]
            self.scroll_layout.remove_widget(row)
            del self.row_widgets[recurring_act.name]
            del self.displayed_recurring_acts_dict[recurring_act.name]

        del self.recurring_acts_dict[recurring_act.name]
