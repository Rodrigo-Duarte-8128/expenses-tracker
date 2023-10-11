from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from row_widgets.category_row_widget import SubCategoryRowWidget
from screens.category_screens.edit_subcategory_screen import EditSubCategoryScreen
from screens.category_screens.add_subcategory_screen import AddSubCategoryScreen
from dropdown.custom_dropdown import CustomDropDown
from datas.transaction import RecurringTransaction



red = hex("#E63946")
cream = hex("#F1FAEE")
light_teal = hex("#A8DADC")
blue = hex("#457B9D")
dark_blue = hex("#1D3557")
green = hex("#84a98c")



class EditCategoryScreen(MDScreen):
    def __init__(self, category, app, **kwargs):
        super(EditCategoryScreen, self).__init__(**kwargs)

        self.app = app
        self.category = category

        self.layout = MDFloatLayout()

        self.window_width, self.window_height = Window.size


        # Create Labels
        self.edit_category_label = MDLabel(
            text="Edit Category", 
            pos_hint = {"x": 0.3, "y": 0.85},
            size_hint = (0.4, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.edit_category_label)


        # Create Text Fields
        self.name_text_field = MDTextField(
            hint_text = "Enter the Category Name",
            mode = "rectangle",
            helper_text = "Category name already exists.",
            helper_text_mode = "on_error",
            pos_hint = {"x": 0.1, "y": 0.7},
            size_hint = (0.8, 0.1)
        )
        self.layout.add_widget(self.name_text_field)
        self.name_text_field.text = category.name


        


        # create dropdown
        kind_shown = ""
        if category.kind == "Expense":
            kind_shown = "Income"
        elif category.kind == "Income":
            kind_shown = "Expense"


        self.dropdown = CustomDropDown(
            category.kind,
            {"x": 0.1, "y": 0.6},
            (0.8, 0.05),
            [
               kind_shown
            ],
            blue,
            self.window_height*0.05
        )
        self.layout.add_widget(self.dropdown.dropdown_label)



        # Create Categories Scroll View Headers
        self.subcategory_name_label = MDRaisedButton(
            text = "Subcategory Name",
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            md_bg_color_disabled = blue,
            size_hint = (1, 0.04),
            pos_hint = {"x": 0, "y": 0.505},
            elevation = 0,
            _radius = 0
        )
        self.layout.add_widget(self.subcategory_name_label)


        
        # Create Grid Layout that holds the Scroll View
        self.scroll_layout = MDGridLayout(
            cols=1,
            size_hint_y = None,
            size = (self.window_width, self.window_height * 0.395),
        )
        self.scroll_layout.bind(
            minimum_height=self.scroll_layout.setter("height")
        )
        self.scroll_layout.height = self.scroll_layout.minimum_height

        # build subcategories dictionary from storage, build row_widgets and scroll view
        self.row_widgets = {}
        
        subcategory_names_list = list(category.subcategories.keys())
        subcategory_names_list.sort()

        for subcategory_name in subcategory_names_list:
            

            row = SubCategoryRowWidget(subcategory_name)

            # create edit subcategory btn functionality
            row.name_btn.bind(on_press=self.edit_subcategory_clicked(subcategory_name))

            
            self.row_widgets[subcategory_name] = row
            self.scroll_layout.add_widget(row)
        

        # Create Scroll View
        self.scroll_view = MDScrollView(
            size_hint = (1, 0.395),
            pos_hint = {"x": 0, "y": 0.11},
            bar_width = 10
        )
        self.scroll_view.add_widget(self.scroll_layout)
        self.layout.add_widget(self.scroll_view)

        


        # Create Buttons
        self.remove_btn = MDRaisedButton(
            text="Remove Category", 
            md_bg_color = red, 
            size_hint=(0.5, 0.04), 
            pos_hint={"x": 0.25, "y": 0.805},
            on_press = self.remove_btn_pressed()
        )
        self.layout.add_widget(self.remove_btn)

        self.remove_dialog = MDDialog(
            title = "Remove Category?",
            text = "This will remove all subcategories and set the category of associated transactions to None.",
            buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_press = lambda x: self.remove_dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="REMOVE",
                        text_color=red,
                        on_press = self.remove_category_confirmed()
                    ),
                ],
        )




        self.add_subcategory_btn = MDRaisedButton(
            text="Add Subcategory", 
            md_bg_color = dark_blue, 
            size_hint=(0.5, 0.04), 
            pos_hint={"x": 0.25, "y": 0.06},
            on_press = self.add_subcategory_clicked()
        )
        self.layout.add_widget(self.add_subcategory_btn)


        self.cancel_btn = MDRaisedButton(
            text="Cancel", 
            md_bg_color = blue, 
            size_hint=(0.45, 0.04), 
            pos_hint={"x": 0.025, "y": 0.005},
            on_press = self.cancel_pressed()
        )
        self.layout.add_widget(self.cancel_btn)


        self.save_changes_btn = MDRaisedButton(
            text="Confirm", 
            md_bg_color = blue, 
            size_hint=(0.45, 0.04),
            pos_hint={"x": 0.525, "y": 0.005},
            on_press = self.save_changes()
        )
        self.layout.add_widget(self.save_changes_btn)



        # Add layout to Add Account Screen
        self.add_widget(self.layout)


    def add_subcategory_clicked(self):
        def add(instance):
            self.app.add_subcategory_screen = AddSubCategoryScreen(self.category, self.app, name="add_subcategory_screen")
            self.app.screen_manager.add_widget(self.app.add_subcategory_screen)

            self.app.transition_diagram.add_node(
                "add_subcategory_screen",
                root_screen_node = self.app.categories_screen_node,
                left_node_name = "edit_category_screen"
            )

            self.app.switch_screen("add_subcategory_screen")(instance)
        return add


    def edit_subcategory_clicked(self, subcategory_name):
        def edit(instance):
            # create edit subcategory screen
            self.app.edit_subcategory_screen = EditSubCategoryScreen(self.category, subcategory_name, self.app, name="edit_subcategory_screen")
            self.app.screen_manager.add_widget(self.app.edit_subcategory_screen)

            self.app.transition_diagram.add_node(
                "edit_subcategory_screen",
                root_screen_node = self.app.categories_screen_node,
                left_node_name = "edit_category_screen"
            )

            # move screen
            self.app.switch_screen("edit_subcategory_screen")(instance)
        return edit
    

    def remove_category_confirmed(self):
        def remove(instance):
            # close dialog
            self.remove_dialog.dismiss()

            # remove category
            self.app.categories_screen.remove_category(self.category)

            # move screen to accounts_screen
            self.app.switch_screen("categories_screen")(instance)

            self.app.transition_diagram.remove_node("edit_category_screen")

            # remove edit category screen from the screen manager
            self.app.screen_manager.remove_widget(self.app.edit_category_screen)
        return remove



    def remove_btn_pressed(self):
        def remove(instance):
            self.remove_dialog.open()
        return remove
    

    def remove_subcategory(self, subcategory_name):

        # update related transactions. We set transaction.subcategory = None and we update transaction.old_subcategory_name
        dates_list = []
        for transaction_simple_date, transaction_info in self.app.records_screen.transactions_store.find(category=self.category.name):
            if transaction_info["subcategory"] == subcategory_name:
                dates_list.append(transaction_simple_date)

        for transaction_simple_date in dates_list:
            if transaction_simple_date in self.app.records_screen.acts_in_use_dict:
                transaction = self.app.records_screen.acts_in_use_dict[transaction_simple_date]
                self.app.records_screen.edit_transaction(
                    transaction,
                    {
                        "subcategory": None,
                        "old_subcategory_name": subcategory_name
                    }
                )
            else:
                transaction = self.app.records_screen.get_transaction_from_storage(transaction_simple_date)
                self.app.records_screen.edit_transaction(
                    transaction,
                    {
                        "subcategory": None,
                        "old_subcategory_name": subcategory_name
                    }
                )

        # update related recurring transactions
        for recurring_transaction_name in self.app.recurring_acts_screen.recurring_acts_dict:
            recurring_transaction = self.app.recurring_acts_screen.recurring_acts_dict[recurring_transaction_name]
            if type(recurring_transaction) == RecurringTransaction:
                if recurring_transaction.category == self.category and recurring_transaction.subcategory != None:
                    if recurring_transaction.subcategory.name == subcategory_name:
                        recurring_transaction.subcategory = None
                        recurring_transaction.old_subcategory_name = subcategory_name
                        self.app.recurring_acts_screen.recurring_transactions_store.delete(recurring_transaction.name)
                        self.app.recurring_acts_screen.store_recurring_transaction(recurring_transaction)


        del self.category.subcategories[subcategory_name]

        self.app.categories_screen.categories_store.delete(self.category.name)

        subcategories_dict = {}
        for name in self.category.subcategories:
            subcategories_dict[name] = {
                "name": self.category.subcategories[name].name,
                "essential": str(self.category.subcategories[name].essential)
            }

        self.app.categories_screen.categories_store.put(
            self.category.name,
            kind = self.category.kind,
            subcategories = subcategories_dict
        )



        # remove row from scroll view in edit category screen
        self.scroll_layout.remove_widget(self.row_widgets[subcategory_name])

        del self.row_widgets[subcategory_name]

        



    def save_changes(self):
        def save(instance):
            errors = []
            new_name = self.name_text_field.text 
            new_kind = self.dropdown.dropdown_label.text
            
            if new_name in self.app.categories_screen.categories_dict and new_name != self.category.name:
                errors.append("name_already_exists")


           
            if not errors:

             

                if new_name != self.category.name:
                    self.app.categories_screen.edit_category(
                        self.category,
                        {
                            "name": new_name,
                            "kind": new_kind
                        }
                    )
                else:
                    self.app.categories_screen.edit_category(
                        self.category,
                        {
                            "kind": new_kind
                        }
                    )

             
                
                # move screen to categories_screen
                self.app.switch_screen("categories_screen")(instance)

                self.app.transition_diagram.remove_node("edit_category_screen")

                # remove edit category screen from the screen manager
                self.app.screen_manager.remove_widget(self.app.edit_category_screen)



            if "name_already_exists" in errors:
                if self.name_text_field.error == False:
                    self.name_text_field.error = True

            if "name_already_exists" not in errors:
                if self.name_text_field.error == True:
                    self.name_text_field.error = False


        return save
    



    def cancel_pressed(self):
        def cancel(instance):
            self.app.switch_screen("categories_screen")(instance)
            self.app.transition_diagram.remove_node("edit_category_screen")
            self.app.screen_manager.remove_widget(self.app.edit_category_screen)
        return cancel