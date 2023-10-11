from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from row_widgets.account_row_widget import AccountRowWidget


red = hex("#E63946")
cream = hex("#F1FAEE")
light_teal = hex("#A8DADC")
blue = hex("#457B9D")
dark_blue = hex("#1D3557")
green = hex("#84a98c")



class EditRecurringTransactionOptionsScreen(MDScreen):
    def __init__(self, app, recurring_transaction, **kwargs):
        super(EditRecurringTransactionOptionsScreen, self).__init__(**kwargs)

        self.layout = MDFloatLayout()

        self.app = app
        self.recurring_transaction = recurring_transaction

        self.window_width, self.window_height = Window.size

        
        self.start_date = app.edit_recurring_transaction_screen.start_date
        self.end_date = app.edit_recurring_transaction_screen.end_date
        self.note = app.edit_recurring_transaction_screen.note


        # Create More Options Label
        self.more_options_label = MDLabel(
            text="More options", 
            pos_hint = {"x": 0.3, "y": 0.85},
            size_hint = (0.4, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.more_options_label)


        # Create Text Fields
        self.start_date_text_field = MDTextField(
            hint_text = "Start Date (dd/mm/yyyy)",
            mode = "rectangle",
            helper_text = "Invalid Date",
            helper_text_mode = "on_error",
            pos_hint = {"x": 0.1, "y": 0.775},
            size_hint = (0.35, 0.05)
        )
        self.start_date_text_field.text = f"{self.start_date.day}/{self.start_date.month}/{self.start_date.year}"
        self.layout.add_widget(self.start_date_text_field)


        self.end_date_text_field = MDTextField(
            hint_text = "End Date (dd/mm/yyyy)",
            mode = "rectangle",
            helper_text = "Invalid Date",
            helper_text_mode = "on_error",
            pos_hint = {"x": 0.55, "y": 0.775},
            size_hint = (0.35, 0.05)
        )
        self.end_date_text_field.text = ""
        if self.end_date != None:
            self.end_date_text_field.text = f"{self.end_date.day}/{self.end_date.month}/{self.end_date.year}"
        self.layout.add_widget(self.end_date_text_field)
        




        self.note_text_field = MDTextField(
            hint_text = "Note",
            mode = "rectangle",
            pos_hint = {"x": 0.1, "y": 0.67},
            size_hint = (0.8, 0.05)
        )
        self.note_text_field.text = self.note
        self.layout.add_widget(self.note_text_field)



        


        # create account option
        self.account_label = MDLabel(
            text="Choose Account", 
            pos_hint = {"x": 0, "y": 0.625},
            size_hint = (1, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.account_label)


        # Create Categories Scroll View Headers
        self.account_number_label = MDRaisedButton(
            text = "No.",
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            md_bg_color_disabled = blue,
            size_hint = (0.2, 0.05),
            pos_hint = {"x": 0, "y": 0.575},
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
            pos_hint = {"x": 0.2, "y": 0.575},
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
            pos_hint = {"x": 0.7, "y": 0.575},
            elevation = 0,
            _radius = 0
        )
        self.layout.add_widget(self.account_total_label)

        




        # Create Grid Layout that holds the Scroll View
        self.scroll_layout = MDGridLayout(
            cols=1,
            size_hint_y = None,
            size = (self.window_width, self.window_height * 0.455),
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
            size_hint = (1, 0.455),
            pos_hint = {"x": 0, "y": 0.12},
            bar_width = 10
        )
        self.scroll_view.add_widget(self.scroll_layout)
        self.layout.add_widget(self.scroll_view)



        self.account_label = MDLabel(
            text="Account:", 
            pos_hint = {"x": 0, "y": 0.06},
            size_hint = (0.5, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.account_label)

        
        self.chosen_account_label = MDLabel(
            text = "",
            pos_hint = {"x": 0.5, "y": 0.06},
            size_hint = (0.5, 0.05),
            halign = "center"
        )
        
        if app.edit_recurring_transaction_screen.chosen_account_label in app.edit_recurring_transaction_screen.layout.children:
            num_name = app.edit_recurring_transaction_screen.chosen_account_label.text
            self.chosen_account_label.text = num_name
            self.layout.add_widget(self.chosen_account_label)




        # create error messages 
        self.error_account_label = MDLabel(
            text="No account", 
            theme_text_color = "Custom",
            halign = "center",
            text_color = red,
            size_hint=(0.5, 0.05), 
            pos_hint={"x": 0.5, "y": 0.06},
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


        self.confirm_btn = MDRaisedButton(
            text="Confirm", 
            md_bg_color = blue, 
            size_hint=(0.45, 0.04),
            pos_hint={"x": 0.525, "y": 0.005},
            on_press = self.confirm_options(app)
        )
        self.layout.add_widget(self.confirm_btn)


        self.remove_btn = MDRaisedButton(
            text="Remove Recurring Act", 
            md_bg_color = red, 
            size_hint=(0.5, 0.04),
            pos_hint={"x": 0.25, "y": 0.11},
            on_press = self.remove_act(app)
        )
        self.layout.add_widget(self.remove_btn)



        # Add layout to Add Account Screen
        self.add_widget(self.layout)


    def remove_act(self, app):
        def remove(instance):
            app.recurring_acts_screen.remove_recurring_act(self.recurring_transaction)

            app.switch_screen("recurring_acts_screen")(instance)
            app.transition_diagram.remove_node("edit_recurring_transaction_options_screen")
            app.screen_manager.remove_widget(app.edit_recurring_transaction_options_screen)
            app.transition_diagram.remove_node("edit_recurring_transaction_screen")
            app.screen_manager.remove_widget(app.edit_recurring_transaction_screen)
        return remove


    def account_pressed(self, account):
        def press(instance):
            # if no account error is on screen remove it
            if self.error_account_label in self.layout.children:
                self.layout.remove_widget(self.error_account_label)

            if self.app.edit_recurring_transaction_screen.error_account_label in self.app.edit_recurring_transaction_screen.layout.children:
                self.app.edit_recurring_transaction_screen.layout.remove_widget(self.app.edit_recurring_transaction_screen.error_account_label)

            
            self.chosen_account_label.text = f"{account.number}. {account.name}"
            if self.chosen_account_label not in self.layout.children:
                self.layout.add_widget(self.chosen_account_label)
        return press



    def confirm_options(self, app):
        def confirm(instance):
            errors = []
            start_simple_date = self.start_date_text_field.text
            end_simple_date = self.end_date_text_field.text
            note = self.note_text_field.text

            

            if not self._validate_date(start_simple_date):
                errors.append("invalid_start_date")
            if end_simple_date != "" and not self._validate_time(end_simple_date):
                errors.append("invalid_end_date")

            if self.chosen_account_label not in self.layout.children:
                errors.append("no_account_chosen")



            if not errors:
                new_start_date = app.edit_recurring_transaction_screen.start_date.parse_string(f"{start_simple_date} 00:00:00")
                app.edit_recurring_transaction_screen.start_date = new_start_date

                if end_simple_date != "":
                    new_end_date = app.edit_recurring_transaction_screen.start_date.parse_string(f"{end_simple_date} 00:00:00")
                else:
                    new_end_date = None

                app.edit_recurring_transaction_screen.end_date = new_end_date

                app.edit_recurring_transaction_screen.note = note

                app.edit_recurring_transaction_screen.chosen_account_label.text = self.chosen_account_label.text
                if app.edit_recurring_transaction_screen.chosen_account_label not in app.edit_recurring_transaction_screen.layout.children:
                    app.edit_recurring_transaction_screen.layout.add_widget(app.edit_recurring_transaction_screen.chosen_account_label)

                app.switch_screen("edit_recurring_transaction_screen")(instance)
                app.transition_diagram.remove_node("edit_recurring_transaction_options_screen")
                app.screen_manager.remove_widget(app.edit_recurring_transaction_options_screen)



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

            if "no_account_chosen" in errors:
                if self.error_account_label not in self.layout.children:
                    self.layout.add_widget(self.error_account_label)

            if "no_account_chosen" not in errors:
                if self.error_account_label in self.layout.children:
                    self.layout.remove_widget(self.error_account_label)


        return confirm





    def cancel_pressed(self, app):
        def cancel(instance):
            app.switch_screen("edit_recurring_transaction_screen")(instance)
            app.transition_diagram.remove_node("edit_recurring_transaction_options_screen")
            app.screen_manager.remove_widget(app.edit_recurring_transaction_options_screen)
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