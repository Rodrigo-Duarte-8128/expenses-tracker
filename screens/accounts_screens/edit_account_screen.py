from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex
from kivymd.uix.screen import MDScreen
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from dropdown.custom_dropdown import CustomDropDown


red = hex("#E63946")
cream = hex("#F1FAEE")
light_teal = hex("#A8DADC")
blue = hex("#457B9D")
dark_blue = hex("#1D3557")
green = hex("#84a98c")



class EditAccountScreen(MDScreen):
    def __init__(self, account, app, **kwargs):
        super(EditAccountScreen, self).__init__(**kwargs)

        self.layout = MDFloatLayout()

        self.window_width, self.window_height = Window.size


        # Create Edit Account Label
        self.edit_account_label = MDLabel(
            text="Edit Account", 
            pos_hint = {"x": 0.3, "y": 0.825},
            size_hint = (0.4, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.edit_account_label)


        # Create Text Fields
        self.number_text_field = MDTextField(
            hint_text = "Enter the Account Number",
            mode = "rectangle",
            helper_text = "Account number must be a positive whole number.",
            helper_text_mode = "on_error",
            pos_hint = {"x": 0.1, "y": 0.6},
            size_hint = (0.8, 0.1)
        )
        self.layout.add_widget(self.number_text_field)
        self.number_text_field.text = str(account.number)


        self.name_text_field = MDTextField(
            hint_text = "Enter the Account Name",
            mode = "rectangle",
            pos_hint = {"x": 0.1, "y": 0.475},
            size_hint = (0.8, 0.1)
        )
        self.layout.add_widget(self.name_text_field)
        self.name_text_field.text = account.name


        self.balance_text_field = MDTextField(
            hint_text = "Enter the Current Account Balance",
            mode = "rectangle",
            helper_text = "Account balance must be a decimal number.",
            helper_text_mode = "on_error",
            pos_hint = {"x": 0.1, "y": 0.35},
            size_hint = (0.8, 0.1)
        )
        self.layout.add_widget(self.balance_text_field)
        self.balance_text_field.text = str(account.balance)


        # create dropdown menu

        self.current_label = MDLabel(
            text="Set as current?", 
            pos_hint = {"x": 0.05, "y": 0.2},
            size_hint = (0.4, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.current_label)
        
        if account.current:
            default = "Yes"
            lst = ["No"]
        else:
            default = "No"
            lst = ["Yes"]

        self.dropdown = CustomDropDown(
            default,
            {"x": 0.55, "y": 0.2},
            (0.4, 0.05),
            lst,
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
            pos_hint={"x": 0.15, "y": 0.1},
        )
        
        

        # Create Buttons
        self.remove_btn = MDRaisedButton(
            text="Remove Account", 
            md_bg_color = red, 
            size_hint=(0.5, 0.04), 
            pos_hint={"x": 0.25, "y": 0.75},
            on_press = self.remove_btn_pressed()
        )
        self.layout.add_widget(self.remove_btn)


        self.remove_dialog = MDDialog(
            title = "Remove Account?",
            text = "This will permanently delete all associated transactions.",
            buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_press = lambda x: self.remove_dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="REMOVE",
                        text_color=red,
                        on_press = self.remove_account_confirmed(account, app)
                    ),
                ],
        )


        self.cancel_btn = MDRaisedButton(
            text="Cancel", 
            md_bg_color = blue, 
            size_hint=(0.45, 0.04), 
            pos_hint={"x": 0.025, "y": 0.005},
            on_press = self.cancel_pressed(app)
        )
        self.layout.add_widget(self.cancel_btn)


        self.save_changes_btn = MDRaisedButton(
            text="Confirm", 
            md_bg_color = blue, 
            size_hint=(0.45, 0.04),
            pos_hint={"x": 0.525, "y": 0.005},
            on_press = self.save_changes(account, app)
        )
        self.layout.add_widget(self.save_changes_btn)



        # Add layout to Add Account Screen
        self.add_widget(self.layout)



    def remove_account_confirmed(self, account, app):
        def remove(instance):

            # close dialog
            self.remove_dialog.dismiss()

            # remove account
            app.accounts_screen.remove_account(account)

            # move screen to accounts_screen
            app.switch_screen("accounts_screen")(instance)

            app.transition_diagram.remove_node("edit_account_screen")

            # remove edit account screen from the screen manager
            app.screen_manager.remove_widget(app.edit_account_screen)
        return remove



    def remove_btn_pressed(self):
        def remove(instance):
            self.remove_dialog.open()
        return remove



    def save_changes(self, account, app):
        def save(instance):
            errors = []
            new_name = self.name_text_field.text 
            new_balance = self.balance_text_field.text
            new_number = self.number_text_field.text
            new_current_answer = self.dropdown.dropdown_label.text

            if new_current_answer == "Yes":
                new_current = True
                

            if new_current_answer == "No":
                new_current = False

            try:
                new_number = int(new_number)
                if new_number <= 0:
                    errors.append("invalid_number")
                else:
                    # check if the given number already exists in accounts_dict
                    if new_number in app.accounts_screen.accounts_dict and new_number != account.number:
                        errors.append("number_already_exists")
            except:
                errors.append("invalid_number")


            try:
                new_balance = float(new_balance)
                new_balance = round(new_balance, 2)

            except:
                errors.append("invalid_balance")

            if not errors:

                # edit account
                app.accounts_screen.edit_account(
                    account,
                    {
                        "name": new_name,
                        "balance": new_balance,
                        "number": new_number,
                        "current": new_current
                    }
                )

               
                
                # move screen to accounts_screen
                app.switch_screen("accounts_screen")(instance)

                app.transition_diagram.remove_node("edit_account_screen")

                # remove edit account screen from the screen manager
                app.screen_manager.remove_widget(app.edit_account_screen)



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
        return save
    



    def cancel_pressed(self, app):
        def cancel(instance):
            app.switch_screen("accounts_screen")(instance)
            app.transition_diagram.remove_node("edit_account_screen")
            app.screen_manager.remove_widget(app.edit_account_screen)
        return cancel