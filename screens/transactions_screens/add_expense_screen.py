from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from datetime import datetime
from datas.transaction import Transaction
from datas.date import Date, date_is_in_interval
from screens.transactions_screens.add_expense_options_screen import AddExpenseOptionsScreen
from row_widgets.category_row_widget import CategoryRowWidgetOnlyName
from row_widgets.transaction_row_widget import TransactionRowWidget


red = hex("#E63946")
cream = hex("#F1FAEE")
light_teal = hex("#A8DADC")
blue = hex("#457B9D")
dark_blue = hex("#1D3557")
green = hex("#84a98c")



class AddExpenseScreen(MDScreen):
    def __init__(self, app, **kwargs):
        super(AddExpenseScreen, self).__init__(**kwargs)

        self.layout = MDFloatLayout()

        self.app = app

        self.note = ""  # note defaults to empty

        self.window_width, self.window_height = Window.size

        date_string = str(datetime.now())
        self.date = Date(date_string)


        # Create Add Expense Label
        self.add_expense_label = MDLabel(
            text="Add Expenditure", 
            pos_hint = {"x": 0.3, "y": 0.85},
            size_hint = (0.4, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.add_expense_label)


        # Create Text Fields
        self.value_text_field = MDTextField(
            hint_text = "Value",
            mode = "rectangle",
            helper_text = "Invalid Number",
            helper_text_mode = "on_error",
            pos_hint = {"x": 0.1, "y": 0.775},
            size_hint = (0.8, 0.05)
        )
        self.layout.add_widget(self.value_text_field)

      

        # Create category and subcategorylLabels
        self.choose_category_label = MDLabel(
            text="Choose Category", 
            pos_hint = {"x": 0.25, "y": 0.7},
            size_hint = (0.5, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.choose_category_label)

        self.choose_subcategory_label = MDLabel(
            text="Choose Subcategory", 
            pos_hint = {"x": 0.25, "y": 0.7},
            size_hint = (0.5, 0.05),
            halign = "center"
        )


        
        # Create Grid Layout that holds the Scroll View
        self.scroll_layout = MDGridLayout(
            cols=1,
            size_hint_y = None,
            size = (self.window_width, self.window_height * 0.42),
        )
        self.scroll_layout.bind(
            minimum_height=self.scroll_layout.setter("height")
        )
        self.scroll_layout.height = self.scroll_layout.minimum_height



        # build categories dictionary from storage, build row_widgets and scroll view
        
        self.categories_row_widgets = {}
        self.subcategories_row_widgets = {}

        self.expenses_categories_dict = dict(filter(
            lambda pair: pair[1].kind=="Expense",
            app.categories_screen.categories_dict.items()
            )
        )
        
        expenses_categories_names_list = list(self.expenses_categories_dict.keys())
        expenses_categories_names_list.sort()

        for category_name in expenses_categories_names_list:
            #self.categories_row_widgets[category_name] = expenses_categories_dict[category_name]
            category = self.expenses_categories_dict[category_name]

            row = CategoryRowWidgetOnlyName(category)

            # create edit category btn functionality
            row.name_btn.bind(on_press=self.category_clicked(category))

            
            self.categories_row_widgets[category_name] = row
            self.scroll_layout.add_widget(row)
        

        # Create Scroll View
        self.scroll_view = MDScrollView(
            size_hint = (1, 0.42),
            pos_hint = {"x": 0, "y": 0.28},
            bar_width = 10
        )
        self.scroll_view.add_widget(self.scroll_layout)
        self.layout.add_widget(self.scroll_view)












        # Create selected category and subcategory labels

        self.selected_category_label = MDLabel(
            text="Category:", 
            pos_hint = {"x": 0, "y": 0.22},
            size_hint = (0.5, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.selected_category_label)

        self.selected_subcategory_label = MDLabel(
            text="Subcategory:", 
            pos_hint = {"x": 0, "y": 0.17},
            size_hint = (0.5, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.selected_subcategory_label)

      


        self.chosen_category_label = MDLabel(
            text="", 
            pos_hint = {"x": 0.5, "y": 0.22},
            size_hint = (0.5, 0.05),
            halign = "center"
        )
        

        self.chosen_subcategory_label = MDLabel(
            text="", 
            pos_hint = {"x": 0.5, "y": 0.17},
            size_hint = (0.5, 0.05),
            halign = "center"
        )
        


        # create account option
        self.account_label = MDLabel(
            text="Account:", 
            pos_hint = {"x": 0, "y": 0.12},
            size_hint = (0.5, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.account_label)



        self.chosen_account_label = MDLabel(
            text = "",
            pos_hint = {"x": 0.5, "y": 0.12},
            size_hint = (0.5, 0.05),
            halign = "center"
        )

        
        for account_number in app.accounts_screen.current_account_dict:
            account = app.accounts_screen.current_account_dict[account_number]
            num_name = f"{account.number}. {account.name}"
            self.chosen_account_label.text = num_name
            self.layout.add_widget(self.chosen_account_label)


    

        
        


        # create error messages 
        self.error_category_label = MDLabel(
            text="No category", 
            theme_text_color = "Custom",
            halign = "center",
            text_color = red,
            size_hint=(0.5, 0.05), 
            pos_hint={"x": 0.5, "y": 0.22},
        )

        self.error_account_label = MDLabel(
            text="No account", 
            theme_text_color = "Custom",
            halign = "center",
            text_color = red,
            size_hint=(0.5, 0.05), 
            pos_hint={"x": 0.5, "y": 0.12},
        )

        

        # Create Buttons
        self.cancel_btn = MDRaisedButton(
            text="Cancel", 
            md_bg_color = blue, 
            size_hint=(0.45, 0.04), 
            pos_hint={"x": 0.025, "y": 0.005},
            on_press = self.cancel_pressed(app)
        )
        self.layout.add_widget(self.cancel_btn)


        self.add_expense_btn = MDRaisedButton(
            text="Add", 
            md_bg_color = blue, 
            size_hint=(0.45, 0.04),
            pos_hint={"x": 0.525, "y": 0.005},
            on_press = self.add_expense(app)
        )
        self.layout.add_widget(self.add_expense_btn)


        self.options_btn = MDRaisedButton(
            text = "Options",
            md_bg_color = dark_blue,
            size_hint = (0.4, 0.05),
            pos_hint = {"x": 0.3, "y": 0.06},
            on_press = self.options_clicked(app)
        )
        self.layout.add_widget(self.options_btn)



        # Add layout to Add Account Screen
        self.add_widget(self.layout)


    def options_clicked(self, app):
        def click(instance):
            app.add_expense_options_screen = AddExpenseOptionsScreen(app, name="add_expense_options_screen")
            app.screen_manager.add_widget(app.add_expense_options_screen)

            app.transition_diagram.add_node(
                "add_expense_options_screen",
                root_screen_node = app.home_screen_node,
                left_node_name = "add_expense_screen"
            )

            app.switch_screen("add_expense_options_screen")(instance)
        return click






    

    def category_clicked(self, category):
        def click(instance):

            # remove no category error if it is there
            if self.error_category_label in self.layout.children:
                self.layout.remove_widget(self.error_category_label)

            # reset subcategory chosen if it exists
            if self.chosen_subcategory_label in self.layout.children:
                self.layout.remove_widget(self.chosen_subcategory_label)

            # add chosen category name
            self.chosen_category_label.text = category.name
            if self.chosen_category_label not in self.layout.children:
                self.layout.add_widget(self.chosen_category_label)

            # change to choose subcategory label
            self.layout.remove_widget(self.choose_category_label)
            self.layout.add_widget(self.choose_subcategory_label)

            # remove category rows in scroll view
            for category_name in self.categories_row_widgets:
                self.scroll_layout.remove_widget(self.categories_row_widgets[category_name])



            # add subcategory rows in scroll view
            
            subcategories_names_list = list(category.subcategories.keys())
            subcategories_names_list.sort()

            for subcategory_name in subcategories_names_list:
                subcategory = category.subcategories[subcategory_name]

                row = CategoryRowWidgetOnlyName(subcategory)

                # create click subcategory btn functionality
                row.name_btn.bind(on_press=self.subcategory_clicked(subcategory))

                
                self.subcategories_row_widgets[subcategory_name] = row
                self.scroll_layout.add_widget(row)

        return click
    

    def subcategory_clicked(self, subcategory):
        def click(instance):
            
            # add chosen subcategory label
            self.chosen_subcategory_label.text = subcategory.name
            if self.chosen_subcategory_label not in self.layout.children:
                self.layout.add_widget(self.chosen_subcategory_label)

            # change to choose category label
            self.layout.remove_widget(self.choose_subcategory_label)
            self.layout.add_widget(self.choose_category_label)

            # remove subcategory rows in scroll view
            for subcategory_name in self.subcategories_row_widgets:
                self.scroll_layout.remove_widget(self.subcategories_row_widgets[subcategory_name])

            # clear subcategories_row_widgets
            self.subcategories_row_widgets = {}

            # add category rows
            for category_name in self.categories_row_widgets:
                self.scroll_layout.add_widget(self.categories_row_widgets[category_name])

        return click
    



    def add_expense(self, app):
        def add(instance):
           
            errors = []
            value = self.value_text_field.text
            

            try:
                value = float(value)
                if value < 0:
                    errors.append("invalid_value")
            except:
                errors.append("invalid_value")



            if self.chosen_category_label not in self.layout.children:
                errors.append("no_category_chosen")

          

            if self.chosen_account_label not in self.layout.children:
                errors.append("no_account_chosen")



            if not errors:
                value = round(value, 2)
                value = -value # expenses have negative values

                

                category_name = self.chosen_category_label.text 
                subcategory_name = None
                if self.chosen_subcategory_label in self.layout.children:
                    subcategory_name = self.chosen_subcategory_label.text

                category = app.categories_screen.categories_dict[category_name]
                if subcategory_name != None:
                    subcategory = category.subcategories[subcategory_name]
                else:
                    subcategory = None
                

                account_number = int(self.chosen_account_label.text.split(".")[0])
                account = app.accounts_screen.accounts_dict[account_number]


                new_transaction = Transaction(
                    self.date,
                    value,
                    category,
                    account,
                    self.note,
                    subcategory=subcategory,
                )

                

                app.records_screen.store_transaction(new_transaction)

                # update account balance
                new_balance = round(account.balance + value, 2)
                app.accounts_screen.update_balance(account, new_balance)


                # if this transaction is in the displayed month in home screen and belongs to the displayed account then add it to displayed acts
                if int(new_transaction.date.year) == self.app.home_screen.displayed_month[1] and int(new_transaction.date.month) == self.app.home_screen.displayed_month[0]:
                    if self.app.home_screen.displayed_account == new_transaction.account:
                        self.app.home_screen.displayed_acts_dict[new_transaction.date.get_date_simple_string()] = new_transaction
                        self.app.records_screen.acts_in_use_dict[new_transaction.date.get_date_simple_string()] = new_transaction

                        
                        # need to add the new_transaction to home_screen in the correct position

                        row = TransactionRowWidget(new_transaction)

                        # create edit transaction btn functionality
                        row.category_btn.bind(on_press=self.app.home_screen.transaction_clicked(new_transaction))

                        self.app.home_screen.row_widgets[new_transaction.date.get_date_simple_string()] = row


                        # find correct index position for the new transaction
                        index = 0
                        if len(self.app.home_screen.scroll_layout.children) != 0:
                            date = self.app.home_screen.scroll_layout.children[index].act.date.get_date_simple_string()
                            while self.compare_dates(date, new_transaction.date.get_date_simple_string()):
                                index += 1
                                if index == len(self.app.home_screen.scroll_layout.children):
                                    break
                                date = self.app.home_screen.scroll_layout.children[index].act.date.get_date_simple_string()
                        self.app.home_screen.scroll_layout.add_widget(row, index = index)


            


                # if this transaction should belong to the records screen, add it to the displayed_acts_dict in records screen, and refresh screen
                if date_is_in_interval(
                    new_transaction.date.get_date_simple_string()[:10],
                    self.app.records_screen.start_date_text_field.text,
                    self.app.records_screen.end_date_text_field.text
                ):
                    if self.app.records_screen.change_account_btn.text != "Choose Account":
                        if account.number == int(self.app.records_screen.change_account_btn.text.split(".")[0]):
                            self.app.records_screen.displayed_acts_dict[new_transaction.date.get_date_simple_string()] = new_transaction
                            if new_transaction.date.get_date_simple_string() not in self.app.records_screen.acts_in_use_dict:
                                self.app.records_screen.acts_in_use_dict[new_transaction.date.get_date_simple_string()] = new_transaction
                            
                           
                            row = TransactionRowWidget(new_transaction)

                            # create edit transaction btn functionality
                            row.category_btn.bind(on_press=self.app.records_screen.transaction_clicked(new_transaction))

                            self.app.records_screen.row_widgets[new_transaction.date.get_date_simple_string()] = row


                            # find correct index position for the new transaction
                            index = 0
                            if len(self.app.records_screen.scroll_layout.children) != 0:
                                date = self.app.records_screen.scroll_layout.children[index].act.date.get_date_simple_string()
                                while self.compare_dates(date, new_transaction.date.get_date_simple_string()):
                                    index += 1
                                    if index == len(self.app.records_screen.scroll_layout.children):
                                        break
                                    date = self.app.records_screen.scroll_layout.children[index].act.date.get_date_simple_string()
                            self.app.records_screen.scroll_layout.add_widget(row, index = index)




    
                app.switch_screen("home_screen")(instance)

                app.transition_diagram.remove_node("add_expense_screen")

                app.screen_manager.remove_widget(app.add_expense_screen)


                



            if "invalid_value" in errors:
                if self.value_text_field.error == False:
                    self.value_text_field.error = True

            if "invalid_value" not in errors:
                if self.value_text_field.error == True:
                    self.value_text_field.error = False

        

            if "no_category_chosen" in errors:
                if self.error_category_label not in self.layout.children:
                    self.layout.add_widget(self.error_category_label)

            if "no_category_chosen" not in errors:
                if self.error_category_label in self.layout.children:
                    self.layout.remove_widget(self.error_category_label) 

            if "no_account_chosen" in errors:
                if self.error_account_label not in self.layout.children:
                    self.layout.add_widget(self.error_account_label)

            if "no_account_chosen" not in errors:
                if self.error_account_label in self.layout.children:
                    self.layout.remove_widget(self.error_account_label)


            
        return add

    
        
        


    def cancel_pressed(self, app):
        def cancel(instance):
            app.switch_screen("home_screen")(instance)
            app.transition_diagram.remove_node("add_expense_screen")
            app.screen_manager.remove_widget(app.add_expense_screen)
        return cancel


    @staticmethod
    def compare_dates(date_simple_string1, date_simple_string2):
        '''
        date_simple_string should have the format "dd/mm/yyyy hh:mm:ss"

        returns true if date1 is smaller or equal to date2 (meaning date1 occured before date2)
        '''
        year1 = int(date_simple_string1[6:10])
        year2 = int(date_simple_string2[6:10])

        month1 = int(date_simple_string1[3:5])
        month2 = int(date_simple_string2[3:5])

        day1 = int(date_simple_string1[:2])
        day2 = int(date_simple_string2[:2])

        hour1 = int(date_simple_string1[11:13])
        hour2 = int(date_simple_string2[11:13])

        minutes1 = int(date_simple_string1[14:16])
        minutes2 = int(date_simple_string2[14:16])

        seconds1 = int(date_simple_string1[17:])
        seconds2 = int(date_simple_string2[17:])

        if year1 > year2:
            return False
        if year1 < year2:
            return True

        if month1 > month2:
            return False
        if month1 < month2:
            return True
        
        if day1 > day2:
            return False
        if day1 < day2:
            return True
        
        if hour1 > hour2:
            return False
        if hour1 < hour2:
            return True
        
        if minutes1 > minutes2:
            return False
        if minutes1 < minutes2:
            return True
        
        if seconds1 > seconds2:
            return False
        return True
    


    
    
        


