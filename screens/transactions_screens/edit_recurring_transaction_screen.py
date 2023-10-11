from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from row_widgets.category_row_widget import CategoryRowWidgetOnlyName
from screens.transactions_screens.edit_recurring_transaction_options_screen import EditRecurringTransactionOptionsScreen


red = hex("#E63946")
cream = hex("#F1FAEE")
light_teal = hex("#A8DADC")
blue = hex("#457B9D")
dark_blue = hex("#1D3557")
green = hex("#84a98c")



class EditRecurringTransactionScreen(MDScreen):
    def __init__(self, app, recurring_transaction, **kwargs):
        super(EditRecurringTransactionScreen, self).__init__(**kwargs)

        self.layout = MDFloatLayout()

        self.app = app
        self.recurring_transaction = recurring_transaction

        self.note = recurring_transaction.note  

        self.window_width, self.window_height = Window.size

        self.start_date = recurring_transaction.start_date
        self.end_date = recurring_transaction.end_date


        # Create Edit Recurring Transaction Label
        self.edit_recurring_transaction_label = MDLabel(
            text="Edit Recurring Transaction", 
            pos_hint = {"x": 0.3, "y": 0.875},
            size_hint = (0.4, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.edit_recurring_transaction_label)


        # Create Text Fields

        self.name_text_field = MDTextField(
            hint_text = "Name",
            mode = "rectangle",
            helper_text = "Name already exists.",
            helper_text_mode = "on_error",
            pos_hint = {"x": 0.1, "y": 0.8},
            size_hint = (0.8, 0.05)
        )
        self.name_text_field.text = self.recurring_transaction.name
        self.layout.add_widget(self.name_text_field)


        self.value_text_field = MDTextField(
            hint_text = "Value",
            mode = "rectangle",
            helper_text = "Invalid Number",
            helper_text_mode = "on_error",
            pos_hint = {"x": 0.1, "y": 0.72},
            size_hint = (0.8, 0.05)
        )
        self.value_text_field.text = str(abs(self.recurring_transaction.value))
        self.layout.add_widget(self.value_text_field)

        self.month_day_text_field = MDTextField(
            hint_text = "Month Day",
            mode = "rectangle",
            helper_text = "Invalid Day",
            helper_text_mode = "on_error",
            pos_hint = {"x": 0.25, "y": 0.64},
            size_hint = (0.5, 0.05)
        )
        self.month_day_text_field.text = str(self.recurring_transaction.month_day)
        self.layout.add_widget(self.month_day_text_field)

        


        # Create category and subcategory Labels
        self.choose_category_label = MDLabel(
            text="Choose Category", 
            pos_hint = {"x": 0.25, "y": 0.58},
            size_hint = (0.5, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.choose_category_label)

        self.choose_subcategory_label = MDLabel(
            text="Choose Subcategory", 
            pos_hint = {"x": 0.25, "y": 0.58},
            size_hint = (0.5, 0.05),
            halign = "center"
        )


        
        # Create Grid Layout that holds the Scroll View
        self.scroll_layout = MDGridLayout(
            cols=1,
            size_hint_y = None,
            size = (self.window_width, self.window_height * 0.3),
        )
        self.scroll_layout.bind(
            minimum_height=self.scroll_layout.setter("height")
        )
        self.scroll_layout.height = self.scroll_layout.minimum_height



        # build categories dictionary from storage, build row_widgets and scroll view
        
        self.categories_row_widgets = {}
        self.subcategories_row_widgets = {}

      

        category_names = list(app.categories_screen.categories_dict)
        category_names.sort()

        for category_name in category_names:
            category = app.categories_screen.categories_dict[category_name]

            row = CategoryRowWidgetOnlyName(category)

            # create edit category btn functionality
            row.name_btn.bind(on_press=self.category_clicked(category))

            
            self.categories_row_widgets[category_name] = row
            self.scroll_layout.add_widget(row)
        

        # Create Scroll View
        self.scroll_view = MDScrollView(
            size_hint = (1, 0.3),
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
            text = self.recurring_transaction.category.name if self.recurring_transaction.category != None else "", 
            pos_hint = {"x": 0.5, "y": 0.22},
            size_hint = (0.5, 0.05),
            halign = "center"
        )
        if self.recurring_transaction.category != None:
            self.layout.add_widget(self.chosen_category_label)
        

        self.chosen_subcategory_label = MDLabel(
            text=self.recurring_transaction.subcategory.name if self.recurring_transaction.subcategory != None else "", 
            pos_hint = {"x": 0.5, "y": 0.17},
            size_hint = (0.5, 0.05),
            halign = "center"
        )
        if self.recurring_transaction.subcategory != None:
            self.layout.add_widget(self.chosen_subcategory_label)
        


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
        self.chosen_account_label.text = f"{self.recurring_transaction.account.number}. {self.recurring_transaction.account.name}"
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


        self.confirm_changes_btn = MDRaisedButton(
            text="Confirm", 
            md_bg_color = blue, 
            size_hint=(0.45, 0.04),
            pos_hint={"x": 0.525, "y": 0.005},
            on_press = self.confirm_changes()
        )
        self.layout.add_widget(self.confirm_changes_btn)


        self.options_btn = MDRaisedButton(
            text = "Options",
            md_bg_color = dark_blue,
            size_hint = (0.4, 0.05),
            pos_hint = {"x": 0.3, "y": 0.06},
            on_press = self.options_clicked()
        )
        self.layout.add_widget(self.options_btn)



        # Add layout to Add Account Screen
        self.add_widget(self.layout)


    def confirm_changes(self):
        def confirm(instance):
            errors = []

            name = self.name_text_field.text
            if name in self.app.recurring_acts_screen.recurring_acts_dict and name != self.recurring_transaction.name:
                errors.append("name_already_exists")


            value = self.value_text_field.text
           
            try:
                value = float(value)
                if value < 0:
                    errors.append("invalid_value")
            except:
                errors.append("invalid_value")


            month_day = self.month_day_text_field.text
            try:
                month_day = int(month_day)
                if month_day < 1 or month_day > 28:
                    errors.append("invalid_month_day")
            except:
                errors.append("invalid_month_day")



            if self.chosen_category_label not in self.layout.children:
                errors.append("no_category_chosen")


            if self.chosen_account_label not in self.layout.children:
                errors.append("no_account_chosen")



            if not errors:
                
                category_name = self.chosen_category_label.text 
                subcategory_name = None
                if self.chosen_subcategory_label in self.layout.children:
                    subcategory_name = self.chosen_subcategory_label.text

                category = self.app.categories_screen.categories_dict[category_name]
                if subcategory_name != None:
                    subcategory = category.subcategories[subcategory_name]
                else:
                    subcategory = None
                
                value = round(value, 2)
                if category.kind == "Expense":
                    value = -value

               
                

                account_number = int(self.chosen_account_label.text.split(".")[0])
                account = self.app.accounts_screen.accounts_dict[account_number]

                old_name = self.recurring_transaction.name
                if name != old_name:
                    del self.app.recurring_acts_screen.recurring_acts_dict[old_name]
                    if old_name in self.app.recurring_acts_screen.displayed_recurring_acts_dict:
                        del self.app.recurring_acts_screen.displayed_recurring_acts_dict[old_name]
                        self.app.recurring_acts_screen.displayed_recurring_acts_dict[name] = self.recurring_transaction
                    self.app.recurring_acts_screen.recurring_acts_dict[name] = self.recurring_transaction

                self.recurring_transaction.name = name
                self.recurring_transaction.start_date = self.start_date
                self.recurring_transaction.end_date = self.end_date
                self.recurring_transaction.month_day = month_day
                self.recurring_transaction.value = value
                self.recurring_transaction.category = category
                self.recurring_transaction.subcategory = subcategory
                self.recurring_transaction.note = self.note
                self.recurring_transaction.account = account

                # update in storage
                self.app.recurring_acts_screen.recurring_transactions_store.delete(old_name)
                self.app.recurring_acts_screen.store_recurring_transaction(self.recurring_transaction)
                


                self.app.recurring_acts_screen.refresh_row_widgets()

                

                self.app.switch_screen("recurring_acts_screen")(instance)

                self.app.transition_diagram.remove_node("edit_recurring_transaction_screen")

                self.app.screen_manager.remove_widget(self.app.edit_recurring_transaction_screen)



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

            if "invalid_month_day" in errors:
                if self.month_day_text_field.error == False:
                    self.month_day_text_field.error = True

            if "invalid_month_day" not in errors:
                if self.month_day_text_field.error == True:
                    self.month_day_text_field.error = False

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
        return confirm
    






    def options_clicked(self):
        def click(instance):
            self.app.edit_recurring_transaction_options_screen = EditRecurringTransactionOptionsScreen(self.app, self.recurring_transaction, name="edit_recurring_transaction_options_screen")
            self.app.screen_manager.add_widget(self.app.edit_recurring_transaction_options_screen)

            self.app.transition_diagram.add_node(
                "edit_recurring_transaction_options_screen",
                root_screen_node = self.app.recurring_acts_screen_node,
                left_node_name = "edit_recurring_transaction_screen"
            )

            self.app.switch_screen("edit_recurring_transaction_options_screen")(instance)
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
    



    

    
        
        


    def cancel_pressed(self, app):
        def cancel(instance):
            app.switch_screen("recurring_acts_screen")(instance)
            app.transition_diagram.remove_node("edit_recurring_transaction_screen")
            app.screen_manager.remove_widget(app.edit_recurring_transaction_screen)
        return cancel