from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from datas.account import Account
from datas.transaction import RecurringTransaction, RecurringTransfer
from row_widgets.account_row_widget import AccountRowWidget
from screens.accounts_screens.edit_account_screen import EditAccountScreen
from screens.accounts_screens.add_account_screen import AddAccountScreen


red = hex("#E63946")
cream = hex("#F1FAEE")
light_teal = hex("#A8DADC")
blue = hex("#457B9D")
dark_blue = hex("#1D3557")
green = hex("#84a98c")

light_grey = hex("#EDEDED")



class AccountsScreen(MDScreen):
    def __init__(self, app, **kwargs):
        super(AccountsScreen, self).__init__(**kwargs)

        self.app = app

        
        

        self.layout = MDFloatLayout()

        self.window_width, self.window_height = Window.size

        # get stored accounts
        self.accounts_store = JsonStore("accounts.json")

        self.accounts_dict = {}
        self.row_widgets = {}

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

        # build accounts dictionary from storage, build row_widgets and scroll view   
        account_numbers_list = list(map(lambda x: int(x), self.accounts_store.keys()))
        account_numbers_list.sort()

        for account_number in account_numbers_list:
            current_str = self.accounts_store.get(str(account_number))["current"]
            if current_str == "True":
                current = True
            if current_str == "False":
                current = False
            account = Account(
                self.accounts_store.get(str(account_number))["name"],
                self.accounts_store.get(str(account_number))["balance"],
                account_number,
                current=current
            )
            self.accounts_dict[account_number] = account

            row = AccountRowWidget(account)

            # create edit account btn functionality
            row.account_name_btn.bind(on_press=self.edit_account_clicked(account))

            
            self.row_widgets[account_number] = row
            self.scroll_layout.add_widget(row)

        
        # check for the existence of a current account
        self.current_account_dict = {}
        for account_number in self.accounts_dict:
            account = self.accounts_dict[account_number]
            if account.current:
                self.current_account_dict[account_number] = account
        

        # Create Scroll View
        self.scroll_view = MDScrollView(
            size_hint = (1, 0.7),
            pos_hint = {"x": 0, "y": 0.05},
            bar_width = 10
        )
        self.scroll_view.add_widget(self.scroll_layout)
        self.layout.add_widget(self.scroll_view)
        

        

        
        # Create label for the categories list
        self.accounts_label = MDLabel(
            text = "Accounts",
            pos_hint = {"x": 0.3, "y": 0.85},
            size_hint = (0.4, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.accounts_label)

        total_wealth = 0
        for account_number in self.accounts_dict:
            total_wealth += self.accounts_dict[account_number].balance

        total_wealth = round(total_wealth, 2)

        if total_wealth == int(total_wealth):
            total_wealth = int(total_wealth)

        self.total_wealth_label = MDLabel(
            bold = True,
            text = f"Total Wealth: \u20ac{total_wealth}",
            pos_hint = {"x": 0.25, "y": 0.8},
            size_hint = (0.5, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.total_wealth_label)




        # Create Categories Scroll View Headers
        self.account_number_label = MDRaisedButton(
            text = "No.",
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            md_bg_color_disabled = blue,
            size_hint = (0.2, 0.05),
            pos_hint = {"x": 0, "y": 0.75},
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
            pos_hint = {"x": 0.2, "y": 0.75},
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
            pos_hint = {"x": 0.7, "y": 0.75},
            elevation = 0,
            _radius = 0
        )
        self.layout.add_widget(self.account_total_label)

        

        


        # Create new category button
        self.new_account_btn = MDRaisedButton(
            text = "New Account",
            size_hint = (0.4, 0.04),
            pos_hint = {"x": 0.3, "y": 0.005},
            md_bg_color = blue,
            on_press = self.add_account_clicked()
        )
        self.layout.add_widget(self.new_account_btn)

       
        self.add_widget(self.layout)




    def update_balance(self, account, new_value): 
        '''
        change the balance of the account to new_value
        '''

        self.edit_account(account, {"balance": new_value})




    def edit_account(self, account, changes_dict): 
        '''
        makes changes to storage, then updates the accounts_dict and the screen
        also updates the transaction objects associated to this account, so that their account attributes are up to date

        changes_dict has keys which are account attributes, and the corresponding value is the new value
        eg if changes_dict = {"balance": 1000} this means that the only change is in the balance attribute which has a new value of 1000
        '''

        if account == None:
            return None # this is to incorporate the possibility that we are changing a transfer which has a sending/receiving account set to None

        # remove account from storage 
        self.accounts_store.delete(str(account.number))
        


        if "name" in changes_dict:
            new_name = changes_dict["name"]
            account.name = new_name

        if "balance" in changes_dict:
            new_balance = changes_dict["balance"]
            account.balance = new_balance

        if "number" in changes_dict:
            new_number = changes_dict["number"]
            if new_number != account.number:


                # change the account number of all transactions and transfers stored associated to this account
                new_number = changes_dict["number"]
                transactions_to_be_changed = {}
                for transaction_simple_date, _ in self.app.records_screen.transactions_store.find(account=str(account.number)):
                    transactions_to_be_changed[transaction_simple_date] = self.app.records_screen.get_transaction_from_storage(transaction_simple_date)

                transfers_to_be_changed = {}
                for transfer_simple_date, _ in self.app.records_screen.transfers_store.find(account_sending=str(account.number)):
                    transfers_to_be_changed[transfer_simple_date] = self.app.records_screen.get_transfer_from_storage(transfer_simple_date)
                for transfer_simple_date, _ in self.app.records_screen.transfers_store.find(account_receiving=str(account.number)):
                    transfers_to_be_changed[transfer_simple_date] = self.app.records_screen.get_transfer_from_storage(transfer_simple_date)




                # delete account from accounts_dict since its location has changed
                del self.accounts_dict[account.number]
                # delete account row from row widgets since its location has changed
                row = self.row_widgets[account.number]
                del self.row_widgets[account.number]
                # update account object
                account.number = new_number

                for transaction_simple_date in transactions_to_be_changed:
                    self.app.records_screen.transactions_store.delete(transaction_simple_date)
                    
                    self.app.records_screen.store_transaction(
                        transactions_to_be_changed[transaction_simple_date]
                    )

                for transfer_simple_date in transfers_to_be_changed:
                    self.app.records_screen.transfers_store.delete(transfer_simple_date)
                    
                    self.app.records_screen.store_transfer(
                        transfers_to_be_changed[transfer_simple_date]
                    )

                # change the account number of all associated recurring transactions
                for recurring_act_name in self.app.recurring_acts_screen.recurring_acts_dict:
                    recurring_act = self.app.recurring_acts_screen.recurring_acts_dict[recurring_act_name]
                    if type(recurring_act) == RecurringTransaction:
                        if recurring_act.account == account:
                            self.app.recurring_acts_screen.recurring_transactions_store.delete(recurring_act_name)
                            self.app.recurring_acts_screen.store_recurring_transaction(recurring_act)
                    elif type(recurring_act) == RecurringTransfer:
                        if recurring_act.account_receiving == account or recurring_act.account_sending == account:
                            self.app.recurring_acts_screen.recurring_transfers_store.delete(recurring_act_name)
                            self.app.recurring_acts_screen.store_recurring_transfer(recurring_act)



                # place account in accounts_dict in correct location
                self.accounts_dict[account.number] = account 
                # place account row in row widgets in correct location
                self.row_widgets[account.number] = row

        if "current" in changes_dict:
            new_current = changes_dict["current"]
            if account.current == False and new_current == True:
                for old_current_account_number in self.current_account_dict:
                    old_current_account = self.current_account_dict[old_current_account_number]
                    # remove old current account from storage
                    self.accounts_store.delete(str(old_current_account_number))

                    # change current in old_current_account
                    old_current_account.current = False

                    # put updated old_current_account back in storage
                    self.accounts_store.put(
                        str(old_current_account.number),
                        name = old_current_account.name,
                        balance = old_current_account.balance,
                        current = "False"
                    )
                    
                    
                # reset current_account_dict
                self.current_account_dict = {}
                # add this account to the current_account_dict
                self.current_account_dict[account.number] = account # account.number has already been updated if applicable
            if account.current == True and new_current == False:
                self.current_account_dict = {}
            
            if new_current != account.current:
                account.current = new_current
                self.app.home_screen.refresh_current_account()
                self.app.recurring_acts_screen.refresh_current_account()


        # place new values in storage
        if account.current == True:
            current = "True"
        elif account.current == False:
            current = "False"

        self.accounts_store.put(
            str(account.number),
            name = account.name,
            balance = account.balance,
            current = current
        )

        self.refresh_screen() # to update the row widgets



    
    def refresh_screen(self):

        # update total wealth value
        total_wealth = 0
        for account_number in self.accounts_dict:
            total_wealth += self.accounts_dict[account_number].balance

        total_wealth = round(total_wealth, 2)

        if total_wealth == int(total_wealth):
            total_wealth = int(total_wealth)
        
        self.total_wealth_label.text = f"Total Wealth: \u20ac{total_wealth}"

        



        # re-build the scroll view holding the accounts information based on the current accounts dictionary

        for account_number in self.accounts_dict:
            self.scroll_layout.remove_widget(self.row_widgets[account_number])
            
        self.row_widgets = {}


        account_numbers_list = list(self.accounts_dict.keys())
        account_numbers_list.sort()

        for account_number in account_numbers_list:
            account = self.accounts_dict[account_number]
        
            row = AccountRowWidget(account)

            # create edit account btn functionality
            row.account_name_btn.bind(on_press=self.edit_account_clicked(account))
            
            self.row_widgets[account_number] = row
            self.scroll_layout.add_widget(row)




    def add_account_clicked(self):
        def click(instance):
            self.app.add_account_screen = AddAccountScreen(self.app, name="add_account_screen")
            self.app.screen_manager.add_widget(self.app.add_account_screen)

            self.app.transition_diagram.add_node(
                "add_account_screen",
                root_screen_node = self.app.accounts_screen_node,
                left_node = self.app.accounts_screen_node
            )

            self.app.switch_screen("add_account_screen")(instance)
        return click

    def edit_account_clicked(self, account):
        def edit(instance):
            # create edit account screen
            self.app.edit_account_screen = EditAccountScreen(account, self.app, name="edit_account_screen")
            self.app.screen_manager.add_widget(self.app.edit_account_screen)

            self.app.transition_diagram.add_node(
                "edit_account_screen",
                root_screen_node = self.app.accounts_screen_node,
                left_node = self.app.accounts_screen_node
            )

            # move screen
            self.app.switch_screen("edit_account_screen")(instance)  
        return edit
    


    

    
    
        


    def remove_account(self, account, refresh=True):
        # remove all transactions associated to this account
        for transaction_simple_date in self.app.records_screen.transactions_store.keys():
            transaction_account_number = int(self.app.records_screen.transactions_store.get(transaction_simple_date)["account"])
            if transaction_account_number == account.number:
                self.app.records_screen.remove_transaction(transaction_simple_date, account_removed = True)

        # if this account has transfers, then the correct transfer attribute gets set to None
        # if the transfer has two None accounts then it gets removed
        for transfer_simple_date in self.app.records_screen.transfers_store.keys():
            transfer_info = self.app.records_screen.transfers_store.get(transfer_simple_date)
            if "account_sending" in transfer_info:
                transfer_account_sending_number = int(transfer_info["account_sending"])
            else:
                transfer_account_sending_number = None
            if "account_receiving" in transfer_info:
                transfer_account_receiving_number = int(transfer_info["account_receiving"])
            else:
                transfer_account_receiving_number = None


            if transfer_account_sending_number == account.number:
                if transfer_account_receiving_number == None:
                    self.app.records_screen.remove_transfer(transfer_simple_date, account_sending_removed = True)
                else:
                    transfer = self.app.records_screen.get_transfer_from_storage(transfer_simple_date)
                    self.app.records_screen.edit_transfer(
                        transfer,
                        {
                            "simple_date_string": transfer_simple_date,
                            "value": transfer.value,
                            "note": transfer.note,
                            "account_sending": None,
                            "account_receiving": transfer.account_receiving.number
                        }
                    )

            if transfer_account_receiving_number == account.number:
                if transfer_account_sending_number == None:
                    self.app.records_screen.remove_transfer(transfer_simple_date, account_receiving_removed=True)
                else:
                    transfer = self.app.records_screen.get_transfer_from_storage(transfer_simple_date)
                    self.app.records_screen.edit_transfer(
                        transfer,
                        {
                            "simple_date_string": transfer_simple_date,
                            "value": transfer.value,
                            "note": transfer.note,
                            "account_sending": transfer.account_sending.number,
                            "account_receiving": None
                        }
                    )

        # remove all recurring transactions associated to this account
        # set account to None for a recurring transfer (if both become None, then it is removed)
        recurring_acts_names_list = list(self.app.recurring_acts_screen.recurring_acts_dict.keys())
        for recurring_act_name in recurring_acts_names_list:
            recurring_act = self.app.recurring_acts_screen.recurring_acts_dict[recurring_act_name]
            if type(recurring_act) == RecurringTransaction:
                if recurring_act.account == account:
                    self.app.recurring_acts_screen.remove_recurring_act(recurring_act)
            elif type(recurring_act) == RecurringTransfer:
                if recurring_act.account_sending == account:
                    if recurring_act.account_receiving == None:
                        self.app.recurring_acts_screen.remove_recurring_act(recurring_act)
                    else:
                        recurring_act.account_sending = None
                        self.app.recurring_acts_screen.recurring_transfers_store.delete(recurring_act.name)
                        self.app.recurring_acts_screen.store_recurring_transfer(recurring_act)


                elif recurring_act.account_receiving == account:
                    if recurring_act.account_sending == None:
                        self.app.recurring_acts_screen.remove_recurring_act(recurring_act)
                    
                    else:
                        recurring_act.account_receiving = None
                        self.app.recurring_acts_screen.recurring_transfers_store.delete(recurring_act.name)
                        self.app.recurring_acts_screen.store_recurring_transfer(recurring_act)

        self.app.recurring_acts_screen.refresh_row_widgets()
        self.app.home_screen.refresh_row_widgets()


        # remove account from storage and accounts_dict
        self.accounts_store.delete(str(account.number))
        del self.accounts_dict[account.number]

        # if this was the current account delete from current_account_dict
        if account.current:
            del self.current_account_dict[account.number]
            self.app.home_screen.refresh_current_account()
        
        # remove account from scroll view
        account_row = self.row_widgets[account.number]
        self.scroll_layout.remove_widget(account_row)

        # remove account from rows dict
        del self.row_widgets[account.number]


        if refresh:
            self.refresh_screen()



                

            
        
        

    def add_account(self, account, refresh=True):
        # add new account to storage
        self.accounts_store.put(
            str(account.number),
            name = account.name,
            balance = account.balance,
            current = str(account.current)
        )

        # add new account instance to accounts_dict
        self.accounts_dict[account.number] = account

        # if new current account add to current_account_dict
        if account.current:
            self.current_account_dict[account.number] = account
            self.app.home_screen.refresh_current_account()

        # add new account to scroll view
        row = AccountRowWidget(account)
        self.scroll_layout.add_widget(row)

        # create edit account btn functionality
        row.account_name_btn.bind(on_press=self.edit_account_clicked(account))

        # add new account to row_widgets
        self.row_widgets[account.number] = row

        # refresh the scroll view in accounts_screen
        if refresh:
            self.refresh_screen()