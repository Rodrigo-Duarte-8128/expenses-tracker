from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex
from kivy.uix.button import Button
from kivymd.uix.screen import MDScreen
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from screens.accounts_screens.choose_account_screen import ChooseAccountScreen


red = hex("#E63946")
cream = hex("#F1FAEE")
light_teal = hex("#A8DADC")
blue = hex("#457B9D")
dark_blue = hex("#1D3557")
green = hex("#84a98c")



class EditRecurringTransferScreen(MDScreen):
    def __init__(self, app, recurring_transfer, **kwargs):
        super(EditRecurringTransferScreen, self).__init__(**kwargs)

        self.layout = MDFloatLayout()

        self.app = app
        self.recurring_transfer = recurring_transfer
       

        self.window_width, self.window_height = Window.size


        # Create edit recurring transfer Label
        self.edit_recurring_transfer_label = MDLabel(
            text="Edit Recurring Transfer", 
            pos_hint = {"x": 0.3, "y": 0.85},
            size_hint = (0.4, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.edit_recurring_transfer_label)


        # Create Text Fields

        self.name_text_field = MDTextField(
            hint_text = "Name",
            mode = "rectangle",
            helper_text = "Name already exists.",
            helper_text_mode = "on_error",
            pos_hint = {"x": 0.1, "y": 0.78},
            size_hint = (0.8, 0.05)
        )
        self.layout.add_widget(self.name_text_field)
        self.name_text_field.text = recurring_transfer.name


        self.value_text_field = MDTextField(
            hint_text = "Value",
            mode = "rectangle",
            helper_text = "Invalid Number",
            helper_text_mode = "on_error",
            pos_hint = {"x": 0.1, "y": 0.68},
            size_hint = (0.8, 0.05)
        )
        self.layout.add_widget(self.value_text_field)
        self.value_text_field.text = str(recurring_transfer.value)



        self.start_date_text_field = MDTextField(
            hint_text = "Start Date (dd/mm/yyyy)",
            mode = "rectangle",
            helper_text = "Invalid Date",
            helper_text_mode = "on_error",
            pos_hint = {"x": 0.1, "y": 0.58},
            size_hint = (0.8, 0.1)
        )
        day = self.recurring_transfer.start_date.day
        month = self.recurring_transfer.start_date.month
        year = self.recurring_transfer.start_date.year
        self.start_date_text_field.text = f"{day}/{month}/{year}"
        self.layout.add_widget(self.start_date_text_field)



        self.end_date_text_field = MDTextField(
            hint_text = "End Date (dd/mm/yyyy)",
            mode = "rectangle",
            helper_text = "Invalid Hour",
            helper_text_mode = "on_error",
            pos_hint = {"x": 0.1, "y": 0.48},
            size_hint = (0.8, 0.1)
        )
        
        self.end_date_text_field.text = ""
        if self.recurring_transfer.end_date != None:
            day = self.recurring_transfer.end_date.day
            month = self.recurring_transfer.end_date.month
            year = self.recurring_transfer.end_date.year
            self.end_date_text_field.text = f"{day}/{month}/{year}"

        self.layout.add_widget(self.end_date_text_field)




        self.month_day_text_field = MDTextField(
            hint_text = "Month Day",
            mode = "rectangle",
            helper_text = "Invalid Day",
            helper_text_mode = "on_error",
            pos_hint = {"x": 0.1, "y": 0.38},
            size_hint = (0.8, 0.1)
        )
        self.month_day_text_field.text = str(recurring_transfer.month_day)
        self.layout.add_widget(self.month_day_text_field)



        self.note_text_field = MDTextField(
            hint_text = "Note",
            mode = "rectangle",
            pos_hint = {"x": 0.1, "y": 0.28},
            size_hint = (0.8, 0.1)
        )
        self.note_text_field.text = recurring_transfer.note
        self.layout.add_widget(self.note_text_field)



        







        # create account option
        self.account_sending_label = MDLabel(
            text="Account Sending:", 
            pos_hint = {"x": 0, "y": 0.21},
            size_hint = (0.5, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.account_sending_label)

        account_sending_text = "Choose Account"
        if recurring_transfer.account_sending != None:
            account_sending_text = f"{recurring_transfer.account_sending.number}. {recurring_transfer.account_sending.name}"

        self.choose_account_sending_btn = Button(
            text = account_sending_text,
            color = (1, 1, 1, 1),
            background_color = blue,
            pos_hint = {"x": 0.525, "y": 0.21},
            size_hint = (0.45, 0.05),
            background_normal = ""
        )
        self.layout.add_widget(self.choose_account_sending_btn)
        self.choose_account_sending_btn.bind(on_press=self.change_account())



        
        
        self.account_receiving_label = MDLabel(
            text="Account Receiving:", 
            pos_hint = {"x": 0, "y": 0.155},
            size_hint = (0.5, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.account_receiving_label)


        account_receiving_text = "Choose Account"
        if recurring_transfer.account_receiving != None:
            account_receiving_text = f"{recurring_transfer.account_receiving.number}. {recurring_transfer.account_receiving.name}"

        self.choose_account_receiving_btn = Button(
            text = account_receiving_text,
            color = (1, 1, 1, 1),
            background_color = blue,
            pos_hint = {"x": 0.525, "y": 0.155},
            size_hint = (0.45, 0.05),
            background_normal = ""
        )
        self.layout.add_widget(self.choose_account_receiving_btn)
        self.choose_account_receiving_btn.bind(on_press=self.change_account())

        
        


        # create error messages 
        self.error_account_label = MDLabel(
            text="No accounts chosen.", 
            theme_text_color = "Custom",
            halign = "center",
            text_color = red,
            size_hint=(0.5, 0.05), 
            pos_hint={"x": 0.25, "y": 0.1175},
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


        self.confirm_changes_btn = MDRaisedButton(
            text="Confirm", 
            md_bg_color = blue, 
            size_hint=(0.45, 0.04),
            pos_hint={"x": 0.525, "y": 0.005},
            on_press = self.confirm_changes()
        )
        self.layout.add_widget(self.confirm_changes_btn)


        self.remove_btn = MDRaisedButton(
            text="Remove Recurring Transfer", 
            md_bg_color = red, 
            size_hint=(0.5, 0.04),
            pos_hint={"x": 0.25, "y": 0.075},
            on_press = self.remove_act(app)
        )
        self.layout.add_widget(self.remove_btn)


        


        # Add layout to Add Account Screen
        self.add_widget(self.layout)




    def remove_act(self, app):
        def remove(instance):
            app.recurring_acts_screen.remove_recurring_act(self.recurring_transfer)
            app.switch_screen("recurring_acts_screen")(instance)
            app.transition_diagram.remove_node("edit_recurring_transfer_screen")
            app.screen_manager.remove_widget(app.edit_recurring_transfer_screen)
        return remove




    def change_account(self):
        def change(instance):
            self.app.choose_account_screen = ChooseAccountScreen(self.app, "edit_recurring_transfer_screen", instance, name="choose_account_screen")
            self.app.screen_manager.add_widget(self.app.choose_account_screen)

            # add screen to transition diagram
            self.app.transition_diagram.add_node("choose_account_screen", root_screen_node = self.app.home_screen_node, left_node = self.app.home_screen_node)

            self.app.switch_screen("choose_account_screen")(instance)
        return change




    

    def confirm_changes(self):
        def confirm(instance):
            errors = []

            new_name = self.name_text_field.text
            if new_name in self.app.recurring_acts_screen.recurring_acts_dict:
                if new_name != self.recurring_transfer.name:
                    errors.append("name_already_exists")
            
            value = self.value_text_field.text
            try:
                value = float(value)
                value = round(value, 2)
                if value < 0:
                    errors.append("invalid_value")
            except:
                errors.append("invalid_value")

            simple_start_date = self.start_date_text_field.text
            if not self._validate_date(simple_start_date):
                errors.append("invalid_start_date")
            
            simple_end_date = self.end_date_text_field.text
            if simple_end_date != "" and not self._validate_date(simple_end_date):
                errors.append("invalid_end_date")

            month_day = self.month_day_text_field.text
            try:
                month_day = int(month_day)
                if month_day < 1 or month_day > 28:
                    errors.append("invalid_month_day")
            except:
                errors.append("invalid_month_day")

            note = self.note_text_field.text

            if self.choose_account_sending_btn.text == "Choose Account" and self.choose_account_receiving_btn.text == "Choose Account":
                errors.append("no_accounts_chosen")


            if not errors:
                

                # create new recurring_transfer object
                if simple_end_date != "":
                    end_date = self.app.home_screen.date.parse_string(simple_end_date + " 00:00:00")
                else:
                    end_date = None

                if self.choose_account_sending_btn.text != "Choose Account":
                    account_sending = self.app.accounts_screen.accounts_dict[int(self.choose_account_sending_btn.text.split(".")[0])]
                else:
                    account_sending = None

                if self.choose_account_receiving_btn.text != "Choose Account":
                    account_receiving = self.app.accounts_screen.accounts_dict[int(self.choose_account_receiving_btn.text.split(".")[0])]
                else:
                    account_receiving = None

                old_name = self.recurring_transfer.name
                if new_name != self.recurring_transfer.name:
                    # update recurring_act location in recurring_acts_dict
                    del self.app.recurring_acts_screen.recurring_acts_dict[self.recurring_transfer.name]
                    if self.recurring_transfer.name in self.app.recurring_acts_screen.displayed_recurring_acts:
                        del self.app.recurring_acts_screen.displayed_recurring_acts[self.recurring_transfer.name]
                        self.app.recurring_acts_screen.displayed_recurring_acts[new_name] = self.recurring_transfer

                    self.recurring_transfer.name = new_name

                    self.app.recurring_acts_screen.recurring_acts_dict[new_name] = self.recurring_transfer

                self.recurring_transfer.value = value
                self.recurring_transfer.start_date = self.app.home_screen.date.parse_string(simple_start_date + " 00:00:00")
                self.recurring_transfer.end_date = end_date
                self.recurring_transfer.month_day = month_day
                self.recurring_transfer.note = note
                self.recurring_transfer.account_sending = account_sending
                self.recurring_transfer.account_receiving = account_receiving

                # modify recurring transfer in storage

                self.app.recurring_acts_screen.recurring_transfers_store.delete(old_name)
                
                self.app.recurring_acts_screen.store_recurring_transfer(self.recurring_transfer)

                

                self.app.recurring_acts_screen.refresh_row_widgets()


                self.app.switch_screen("recurring_acts_screen")(instance)
                self.app.transition_diagram.remove_node("edit_recurring_transfer_screen")
                self.app.screen_manager.remove_widget(self.app.edit_recurring_transfer_screen)





            if "name_already_exists" in errors:
                if self.name_text_field.error == False:
                    self.name_text_field.error = True

            if "name_already_exists" not in errors:
                if self.name_text_field.error == True:
                    self.name_text_field.error = False


            if "invalid_value" in errors:
                if self.value_text_field.error == False:
                    self.value_text_field.error = True

            if "invalid_value" not in errors:
                if self.value_text_field.error == True:
                    self.value_text_field.error = False

            
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


            if "invalid_month_day" in errors:
                if self.month_day_text_field.error == False:
                    self.month_day_text_field.error = True

            if "invalid_month_day" not in errors:
                if self.month_day_text_field.error == True:
                    self.month_day_text_field.error = False


            if "no_accounts_chosen" in errors:
                if self.error_account_label not in self.layout.children:
                    self.layout.add_widget(self.error_account_label)

            if "no_accounts_chosen" not in errors:
                if self.error_account_label in self.layout.children:
                    self.layout.remove_widget(self.error_account_label)


            
        return confirm

    
        
        


    def cancel_pressed(self, app):
        def cancel(instance):
            app.switch_screen("recurring_acts_screen")(instance)
            app.transition_diagram.remove_node("edit_recurring_transfer_screen")
            app.screen_manager.remove_widget(app.edit_recurring_transfer_screen)
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


