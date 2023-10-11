from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex
from kivymd.uix.screen import MDScreen
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from datas.account import Account
from dropdown.custom_dropdown import CustomDropDown


red = hex("#E63946")
cream = hex("#F1FAEE")
light_teal = hex("#A8DADC")
blue = hex("#457B9D")
dark_blue = hex("#1D3557")
green = hex("#84a98c")



class AddAccountScreen(MDScreen):
    def __init__(self, app, **kwargs):
        super(AddAccountScreen, self).__init__(**kwargs)

        self.layout = MDFloatLayout()

        self.window_width, self.window_height = Window.size


        # Create Add Account Label
        self.add_account_label = MDLabel(
            text="Add Account", 
            pos_hint = {"x": 0.3, "y": 0.85},
            size_hint = (0.4, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.add_account_label)


        # Create Text Fields
        self.number_text_field = MDTextField(
            hint_text = "Enter the Account Number",
            mode = "rectangle",
            helper_text = "Account number must be a positive whole number.",
            helper_text_mode = "on_error",
            pos_hint = {"x": 0.1, "y": 0.75},
            size_hint = (0.8, 0.1)
        )
        self.layout.add_widget(self.number_text_field)


        self.name_text_field = MDTextField(
            hint_text = "Enter the Account Name",
            mode = "rectangle",
            pos_hint = {"x": 0.1, "y": 0.65},
            size_hint = (0.8, 0.1)
        )
        self.layout.add_widget(self.name_text_field)


        self.balance_text_field = MDTextField(
            hint_text = "Enter the Current Account Balance",
            mode = "rectangle",
            helper_text = "Account balance must be a decimal number.",
            helper_text_mode = "on_error",
            pos_hint = {"x": 0.1, "y": 0.55},
            size_hint = (0.8, 0.1)
        )
        self.layout.add_widget(self.balance_text_field)


        # create dropdown menu

        self.current_label = MDLabel(
            text="Set as current?", 
            pos_hint = {"x": 0.05, "y": 0.45},
            size_hint = (0.4, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.current_label)


       

        self.dropdown = CustomDropDown(
            "No",
            {"x": 0.55, "y": 0.45},
            (0.4, 0.05),
            [
                "Yes",
            ],
            blue,
            self.window_height * 0.05
        )
        self.layout.add_widget(self.dropdown.dropdown_label)


        # Create error message
        self.error_number_label = MDLabel(
            text="Account number already exists.", 
            theme_text_color = "Custom",
            halign = "center",
            text_color = red,
            size_hint=(0.7, 0.05), 
            pos_hint={"x": 0.15, "y": 0.7},
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


        self.add_account_btn = MDRaisedButton(
            text="Add", 
            md_bg_color = blue, 
            size_hint=(0.45, 0.04),
            pos_hint={"x": 0.525, "y": 0.005},
            on_press = self.add_account(app)
        )
        self.layout.add_widget(self.add_account_btn)



        # Add layout to Add Account Screen
        self.add_widget(self.layout)

        
        
    def add_account(self, app):
        def add(instance):
            errors = []
            name = self.name_text_field.text 
            balance = self.balance_text_field.text
            number = self.number_text_field.text
            current_answer = self.dropdown.dropdown_label.text

            if current_answer == "Yes":
                for account_number in app.accounts_screen.current_account_dict:
                    old_current_account = app.accounts_screen.current_account_dict[account_number]

                    app.accounts_screen.edit_account(old_current_account, {"current": False})


                current = True

            if current_answer == "No":
                current = False

            try:
                number = int(number)
                if number <= 0:
                    errors.append("invalid_number")
                else:
                    # check if the given number already exists in accounts_dict
                    if number in app.accounts_screen.accounts_dict:
                        errors.append("number_already_exists")
            except:
                errors.append("invalid_number")


            try:
                balance = float(balance)
                balance = round(balance, 2)

            except:
                errors.append("invalid_balance")

            if not errors:

                # add new account instance to accounts_dict
                new_account = Account(name, balance, number, current=current)
                app.accounts_screen.add_account(new_account)

                
                # clear text field entries
                self.number_text_field.text = ""
                self.name_text_field.text = ""
                self.balance_text_field.text = ""
                self.dropdown.dropdown_label.text = "No"


                # move screen to accounts_screen
                app.switch_screen("accounts_screen")(instance)

                app.transition_diagram.remove_node("add_account_screen")

                # remove add account screen
                app.screen_manager.remove_widget(app.add_account_screen)



            if "invalid_number" in errors:
                if self.number_text_field.error == False:
                    self.number_text_field.error = True

            if "invalid_number" not in errors:
                if self.number_text_field.error == True:
                    self.number_text_field.error = False



            if "invalid_balance" in errors:
                if self.balance_text_field.error == False:
                    self.balance_text_field.error = True 
            
            if "invalid_balance" not in errors:
                if self.balance_text_field.error == True:
                    self.balance_text_field.error = False 



            if "number_already_exists" in errors:
                if self.error_number_label not in self.layout.children:
                    self.layout.add_widget(self.error_number_label)

            if "number_already_exists" not in errors:
                if self.error_number_label in self.layout.children:
                    self.layout.remove_widget(self.error_number_label)
        
        return add

        


    def cancel_pressed(self, app):
        def cancel(instance):
            app.switch_screen("accounts_screen")(instance)
            app.transition_diagram.remove_node("add_account_screen")
            app.screen_manager.remove_widget(app.add_account_screen)
        return cancel
        
            


