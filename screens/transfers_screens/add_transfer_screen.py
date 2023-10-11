from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex
from kivy.uix.button import Button
from kivymd.uix.screen import MDScreen
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from datetime import datetime
from datas.transaction import Transfer
from datas.date import Date
from screens.accounts_screens.choose_account_screen import ChooseAccountScreen


red = hex("#E63946")
cream = hex("#F1FAEE")
light_teal = hex("#A8DADC")
blue = hex("#457B9D")
dark_blue = hex("#1D3557")
green = hex("#84a98c")



class AddTransferScreen(MDScreen):
    def __init__(self, app, **kwargs):
        super(AddTransferScreen, self).__init__(**kwargs)

        self.layout = MDFloatLayout()

        self.app = app

        self.note = ""  # note defaults to empty

        self.window_width, self.window_height = Window.size

        date_string = str(datetime.now())
        self.date = Date(date_string)


        # Create Add Expense Label
        self.add_transfer_label = MDLabel(
            text="Add Transfer", 
            pos_hint = {"x": 0.3, "y": 0.85},
            size_hint = (0.4, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.add_transfer_label)


        # Create Text Fields
        self.value_text_field = MDTextField(
            hint_text = "Value",
            mode = "rectangle",
            helper_text = "Invalid Number",
            helper_text_mode = "on_error",
            pos_hint = {"x": 0.1, "y": 0.67},
            size_hint = (0.8, 0.05)
        )
        self.layout.add_widget(self.value_text_field)


        # Create Text Fields
        self.date_text_field = MDTextField(
            hint_text = "Date (dd/mm/yyyy)",
            mode = "rectangle",
            helper_text = "Invalid Date",
            helper_text_mode = "on_error",
            pos_hint = {"x": 0.1, "y": 0.775},
            size_hint = (0.35, 0.05)
        )
        self.date_text_field.text = f"{self.date.day}/{self.date.month}/{self.date.year}"
        self.layout.add_widget(self.date_text_field)


        self.time_text_field = MDTextField(
            hint_text = "Time (hh:mm:ss)",
            mode = "rectangle",
            helper_text = "Invalid Hour",
            helper_text_mode = "on_error",
            pos_hint = {"x": 0.55, "y": 0.775},
            size_hint = (0.35, 0.05)
        )
        self.time_text_field.text = f"{self.date.hour}:{self.date.minutes}:{self.date.seconds}"
        self.layout.add_widget(self.time_text_field)



        self.note_text_field = MDTextField(
            hint_text = "Note",
            mode = "rectangle",
            pos_hint = {"x": 0.1, "y": 0.57},
            size_hint = (0.8, 0.05)
        )
        self.layout.add_widget(self.note_text_field)

        


        # create sending account option

        self.account_sending_label = MDLabel(
            text = "Account Sending:",
            pos_hint = {"x": 0, "y": 0.47},
            size_hint = (0.5, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.account_sending_label)

        

        self.account_sending_btn = Button(
            text="Choose Account", 
            color = (1, 1, 1, 1),
            background_color = blue, 
            size_hint=(0.4, 0.05), 
            pos_hint={"x": 0.55, "y": 0.47},
            background_normal = ""
        )
        self.layout.add_widget(self.account_sending_btn)
        self.account_sending_btn.bind(on_press=self.choose_account())


        # create receiving account option

        self.account_receiving_label = MDLabel(
            text = "Account Receiving:",
            pos_hint = {"x": 0, "y": 0.37},
            size_hint = (0.5, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.account_receiving_label)

        

        self.account_receiving_btn = Button(
            text="Choose Account", 
            color = (1, 1, 1, 1),
            background_color = blue, 
            size_hint=(0.4, 0.05), 
            pos_hint={"x": 0.55, "y": 0.37},
            background_normal = ""
        )
        self.layout.add_widget(self.account_receiving_btn)
        self.account_receiving_btn.bind(on_press=self.choose_account())







        
        


        # create error messages 
        self.error_accounts_label = MDLabel(
            text="No accounts chosen.", 
            theme_text_color = "Custom",
            halign = "center",
            text_color = red,
            size_hint=(0.5, 0.05), 
            pos_hint={"x": 0.5, "y": 0.3},
        )

        self.error_equal_label = MDLabel(
            text="Accounts need to be different.", 
            theme_text_color = "Custom",
            halign = "center",
            text_color = red,
            size_hint=(0.5, 0.05), 
            pos_hint={"x": 0.5, "y": 0.2},
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


        self.add_transfer_btn = MDRaisedButton(
            text="Add", 
            md_bg_color = blue, 
            size_hint=(0.45, 0.04),
            pos_hint={"x": 0.525, "y": 0.005},
            on_press = self.add_transfer()
        )
        self.layout.add_widget(self.add_transfer_btn)


        



        # Add layout to Add Account Screen
        self.add_widget(self.layout)


    
    def choose_account(self):
        def choose(instance):
            self.app.choose_account_screen = ChooseAccountScreen(self.app, "add_transfer_screen", instance, name="choose_account_screen")
            self.app.screen_manager.add_widget(self.app.choose_account_screen)
            self.app.transition_diagram.add_node("choose_account_screen", root_screen_node = self.app.home_screen_node, left_node_name = "add_transfer_screen")
            self.app.switch_screen("choose_account_screen")(instance)
        return choose


   
    
    


    def add_transfer(self):
        def add(instance):
            errors = []
            value = self.value_text_field.text
            date = self.date_text_field.text
            time = self.time_text_field.text
            note = self.note_text_field.text
            account_sending_num_name = self.account_sending_btn.text 
            account_receiving_num_name = self.account_receiving_btn.text 

            try:
                value = float(value)
                if value < 0:
                    errors.append("invalid_value")
            except:
                errors.append("invalid_value")

            
            if not self._validate_date(date):
                errors.append("invalid_date")
            if not self._validate_time(time):
                errors.append("invalid_time")

            if account_receiving_num_name == "Choose Account" and account_sending_num_name == "Choose Account":
                errors.append("no_account_chosen")

            elif account_sending_num_name == account_receiving_num_name:
                errors.append("equal_accounts")


            if not errors:

                if account_sending_num_name != "Choose Account":
                    account_sending_number = int(account_sending_num_name.split(".")[0])
                    account_sending = self.app.accounts_screen.accounts_dict[account_sending_number]
                else:
                    account_sending = None
                
                if account_receiving_num_name != "Choose Account":
                    account_receiving_number = int(account_receiving_num_name.split(".")[0])
                    account_receiving = self.app.accounts_screen.accounts_dict[account_receiving_number]
                else:
                    account_receiving = None

                date_object = self.date.parse_string(date + " " + time)

                new_transfer = Transfer(
                    date_object,
                    round(value, 2),
                    note,
                    account_sending,
                    account_receiving
                )

                self.app.records_screen.add_transfer(new_transfer)

                self.app.switch_screen("home_screen")(instance)

                self.app.transition_diagram.remove_node("add_transfer_screen")

                self.app.screen_manager.remove_widget(self.app.add_transfer_screen)
                


                







            if "invalid_value" in errors:
                if self.value_text_field.error == False:
                    self.value_text_field.error = True

            if "invalid_value" not in errors:
                if self.value_text_field.error == True:
                    self.value_text_field.error = False

            if "invalid_date" in errors:
                if self.date_text_field.error == False:
                    self.date_text_field.error = True

            if "invalid_date" not in errors:
                if self.date_text_field.error == True:
                    self.date_text_field.error = False

            if "invalid_time" in errors:
                if self.time_text_field.error == False:
                    self.time_text_field.error = True

            if "invalid_time" not in errors:
                if self.time_text_field.error == True:
                    self.time_text_field.error = False


            if "no_account_chosen" in errors:
                if self.error_accounts_label not in self.layout.children:
                    self.layout.add_widget(self.error_accounts_label)

            if "no_account_chosen" not in errors:
                if self.error_accounts_label in self.layout.children:
                    self.layout.remove_widget(self.error_accounts_label)

            if "equal_accounts" in errors:
                if self.error_equal_label not in self.layout.children:
                    self.layout.add_widget(self.error_equal_label)

            if "equal_accounts" not in errors:
                if self.error_equal_label in self.layout.children:
                    self.layout.remove_widget(self.error_equal_label)
            
            


        return add




    
        
        


    def cancel_pressed(self, app):
        def cancel(instance):
            app.switch_screen("home_screen")(instance)
            app.transition_diagram.remove_node("add_transfer_screen")
            app.screen_manager.remove_widget(app.add_transfer_screen)
        return cancel



    @staticmethod
    def _is_leap_year(year):
        # checks if a year int between 0 and 9999 is a leap year
        if year % 4 == 0:
            if year % 100 == 0:
                if year % 400 == 0:
                    return True
                return False
            return True
        return False


    
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
            
            if self._is_leap_year(year):
                if days < 1 or days > leap_calendar[month]:
                    return False

            if not self._is_leap_year(year):
                if days < 1 or days > calendar[month]:
                    return False
                
            return True           
            
        except:
            return False
    

    @staticmethod
    def _validate_time(time):
        # given a string returns true if it has the format "hh:mm:ss"
        split_time = time.split(":")
        try:
            hour = split_time[0]
            minutes = split_time[1]
            seconds = split_time[2]

            if len(hour) != 2 or len(minutes) != 2 or len(seconds) != 2:
                return False
             
            hour = int(hour)
            minutes = int(minutes)
            seconds = int(seconds)

            if hour < 0 or hour > 23:
                return False
            if minutes < 0 or minutes > 59:
                return False
            if seconds < 0 or seconds > 59:
                return False
            
            return True 
        except:
            return False