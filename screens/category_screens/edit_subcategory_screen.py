from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex
from kivymd.uix.screen import MDScreen
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from row_widgets.category_row_widget import SubCategoryRowWidget
from dropdown.custom_dropdown import CustomDropDown
from datas.transaction import RecurringTransaction



red = hex("#E63946")
cream = hex("#F1FAEE")
light_teal = hex("#A8DADC")
blue = hex("#457B9D")
dark_blue = hex("#1D3557")
green = hex("#84a98c")



class EditSubCategoryScreen(MDScreen):
    def __init__(self, category, subcategory_name, app, **kwargs):
        super(EditSubCategoryScreen, self).__init__(**kwargs)

        self.category = category 
        self.subcategory_name = subcategory_name
        self.app = app

        self.layout = MDFloatLayout()

        self.window_width, self.window_height = Window.size


        # Create Edit Category Label
        self.edit_subcategory_label = MDLabel(
            text="Edit Subcategory", 
            pos_hint = {"x": 0.3, "y": 0.85},
            size_hint = (0.4, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.edit_subcategory_label)


        # Create Text Fields
        self.name_text_field = MDTextField(
            hint_text = "Enter the Subcategory Name",
            mode = "rectangle",
            helper_text = "Subcategory name already exists.",
            helper_text_mode = "on_error",
            pos_hint = {"x": 0.1, "y": 0.6},
            size_hint = (0.8, 0.1)
        )
        self.layout.add_widget(self.name_text_field)
        self.name_text_field.text = subcategory_name


        if category.subcategories[subcategory_name].essential:
            show = "Essential"
            lst = ["Non-essential"]
        else:
            show = "Non-essential"
            lst = ["Essential"]

        if category.kind == "Expense":
            self.dropdown = CustomDropDown(
            show,
            {"x": 0.1, "y": 0.4},
            (0.8, 0.05),
            lst,
            blue,
            self.window_height * 0.05
            )
            self.layout.add_widget(self.dropdown.dropdown_label)

            # create error message
            self.error_essential_option = MDLabel(
            text="Please choose one option.", 
            theme_text_color = "Custom",
            halign = "center",
            text_color = red,
            size_hint=(0.7, 0.05), 
            pos_hint={"x": 0.15, "y": 0.3},
            )


        
        
        
        # Create Buttons
        self.remove_btn = MDRaisedButton(
            text="Remove Subcategory", 
            md_bg_color = red, 
            size_hint=(0.5, 0.04), 
            pos_hint={"x": 0.25, "y": 0.75},
            on_press = self.remove_btn_pressed()
        )
        self.layout.add_widget(self.remove_btn)


        self.remove_dialog = MDDialog(
            title = "Remove Subcategory?",
            text = "This will set the subcategory of associated transactions to None.",
            buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_press = lambda x: self.remove_dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="REMOVE",
                        text_color=red,
                        on_press = self.remove_subcategory_confirmed(subcategory_name, app)
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
            on_press = self.save_changes(category, subcategory_name, app)
        )
        self.layout.add_widget(self.save_changes_btn)



        # Add layout to Add Account Screen
        self.add_widget(self.layout)


    def remove_subcategory_confirmed(self, subcategory_name, app):
        def remove(instance):
            # close dialog
            self.remove_dialog.dismiss()

            app.edit_category_screen.remove_subcategory(subcategory_name)

            # move screen to edit_category_screen
            app.switch_screen("edit_category_screen")(instance)

            app.transition_diagram.remove_node("edit_subcategory_screen")

            app.screen_manager.remove_widget(app.edit_subcategory_screen)

        return remove
    

    def remove_btn_pressed(self):
        def pressed(instance):
            self.remove_dialog.open()
        return pressed
            



    def save_changes(self, category, subcategory_name, app):
        def save(instance):
            errors = []
            new_name = self.name_text_field.text 
            
            
            # check if the given number already exists in accounts_dict
            if new_name in category.subcategories and new_name != subcategory_name:
                errors.append("name_already_exists")

            if category.kind == "Expense":
                if self.dropdown.dropdown_label.text == "Essential":
                    is_essential = True
                if self.dropdown.dropdown_label.text == "Non-essential":
                    is_essential = False
                if self.dropdown.dropdown_label.text not in ["Essential", "Non-essential"]:
                    errors.append("invalid_essential_option")
            else:
                is_essential = True


            if not errors:

                subcategory = category.subcategories[subcategory_name]

                subcategory.name = new_name 
                subcategory.essential = is_essential

                # change subcategory location in category.subcategories
                del category.subcategories[subcategory_name]
                category.subcategories[new_name] = subcategory


                if new_name != subcategory_name:
                    # update all associated transactions
                    simple_dates = []
                    for transaction_simple_date, transaction_info in app.records_screen.transactions_store.find(category=category.name):
                        if transaction_info["subcategory"] == subcategory_name:
                            simple_dates.append(transaction_simple_date)

                    for transaction_simple_date in simple_dates:
                        if transaction_simple_date in app.records_screen.acts_in_use_dict:
                            transaction = app.records_screen.acts_in_use_dict[transaction_simple_date]
                            app.records_screen.edit_transaction(
                                transaction,
                                {
                                    "subcategory": new_name
                                }
                            )
                        else:
                            transaction = app.records_screen.get_transaction_from_storage(transaction_simple_date)
                            app.records_screen.edit_transaction(
                                transaction,
                                {
                                    "subcategory": new_name
                                }
                            )

                    # update name of all associated recurring transactions
                    for recurring_transaction_name in self.app.recurring_acts_screen.recurring_acts_dict:
                        recurring_transaction = self.app.recurring_acts_screen.recurring_acts_dict[recurring_transaction_name]
                        if type(recurring_transaction) == RecurringTransaction:
                            if recurring_transaction.category == category:
                                if recurring_transaction.subcategory == subcategory:
                                    self.app.recurring_acts_screen.recurring_transactions_store.delete(recurring_transaction.name)
                                    self.app.recurring_acts_screen.store_recurring_transaction(recurring_transaction)
                

                # save changes in storage
                app.categories_screen.categories_store.delete(category.name)

                subcategories_dict = {}
                for name in category.subcategories:
                    subcategories_dict[name] = {
                        "name": category.subcategories[name].name,
                        "essential": str(category.subcategories[name].essential)
                    }

                app.categories_screen.categories_store.put(
                    category.name,
                    kind = category.kind,
                    subcategories = subcategories_dict
                )

                # update edit_category_screen
                app.edit_category_screen.scroll_layout.remove_widget(app.edit_category_screen.row_widgets[subcategory_name])
                del app.edit_category_screen.row_widgets[subcategory_name]

                new_row = SubCategoryRowWidget(new_name)

                new_row.name_btn.bind(on_press=app.edit_category_screen.edit_subcategory_clicked(new_name))

                app.edit_category_screen.row_widgets[new_name] = new_row
                app.edit_category_screen.scroll_layout.add_widget(new_row)


                


                # move screen to edit_category_screen
                app.switch_screen("edit_category_screen")(instance)

                app.transition_diagram.remove_node("edit_subcategory_screen")

                # remove edit subcategory screen from the screen manager
                app.screen_manager.remove_widget(app.edit_subcategory_screen)


            if "name_already_exists" in errors:
                if self.name_text_field.error == False:
                    self.name_text_field.error = True

            if "name_already_exists" not in errors:
                if self.name_text_field.error == True:
                    self.name_text_field.error = False

            if category.kind == "Expense":
                if "invalid_essential_option" in errors:
                    if self.error_essential_option not in self.layout.children:
                        self.layout.add_widget(self.error_essential_option)

                if "invalid_essential_option" not in errors:
                    if self.error_essential_option in self.layout.children:
                        self.layout.remove_widget(self.error_essential_option)

        return save
    



    def cancel_pressed(self, app):
        def cancel(instance):
            app.switch_screen("edit_category_screen")(instance)
            app.transition_diagram.remove_node("edit_subcategory_screen")
            app.screen_manager.remove_widget(app.edit_subcategory_screen)
        return cancel