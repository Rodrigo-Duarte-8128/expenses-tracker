from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex
from kivymd.uix.screen import MDScreen
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from datas.category import SubCategory
from row_widgets.category_row_widget import SubCategoryRowWidget
from dropdown.custom_dropdown import CustomDropDown



red = hex("#E63946")
cream = hex("#F1FAEE")
light_teal = hex("#A8DADC")
blue = hex("#457B9D")
dark_blue = hex("#1D3557")
green = hex("#84a98c")



class AddSubCategoryScreen(MDScreen):
    def __init__(self, category, app, **kwargs):
        super(AddSubCategoryScreen, self).__init__(**kwargs)
        self.app = app 
        self.category = category
        
        self.layout = MDFloatLayout()

        self.window_width, self.window_height = Window.size


        # Create Add Category Label
        self.add_subcategory_label = MDLabel(
            text="Add Subcategory", 
            pos_hint = {"x": 0.3, "y": 0.85},
            size_hint = (0.4, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.add_subcategory_label)


        # Create Text Fields
        self.name_text_field = MDTextField(
            hint_text = "Enter the Subcategory Name",
            mode = "rectangle",
            helper_text = "Subcategory name already exists.",
            helper_text_mode = "on_error",
            pos_hint = {"x": 0.1, "y": 0.6},
            size_hint = (0.8, 0.2)
        )
        self.layout.add_widget(self.name_text_field)

        if category.kind == "Expense":
            self.dropdown = CustomDropDown(
            "Essential Expenses?",
            {"x": 0.1, "y": 0.4},
            (0.8, 0.05),
            [
                "Essential",
                "Non-essential",
            ],
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
        self.cancel_btn = MDRaisedButton(
            text="Cancel", 
            md_bg_color = blue, 
            size_hint=(0.45, 0.04), 
            pos_hint={"x": 0.025, "y": 0.005},
            on_press = self.cancel_pressed(category, app)
        )
        self.layout.add_widget(self.cancel_btn)


        self.add_category_btn = MDRaisedButton(
            text="Add", 
            md_bg_color = blue, 
            size_hint=(0.45, 0.04),
            pos_hint={"x": 0.525, "y": 0.005},
            on_press = self.add_subcategory(category, app)
        )
        self.layout.add_widget(self.add_category_btn)



        # Add layout to Add Account Screen
        self.add_widget(self.layout)



    def add_subcategory(self, category, app):
        def add(instance):
            errors = []
            new_name = self.name_text_field.text 
            
            if category.kind == "Expense":
                if self.dropdown.dropdown_label.text == "Essential":
                    is_essential = True
                if self.dropdown.dropdown_label.text == "Non-essential":
                    is_essential = False
                if self.dropdown.dropdown_label.text not in ["Essential", "Non-essential"]:
                    errors.append("invalid_essential_option")
            else:
                is_essential = True


            if new_name in category.subcategories:
                errors.append("name_already_exists")

            


                       
            if not errors:

                new_subcategory = SubCategory(
                    new_name,
                    category.name,
                    essential = is_essential
                )

                category.subcategories[new_name] = new_subcategory

                self.app.categories_screen.edit_category(
                    category,
                    {
                        "subcategories": category.subcategories
                    }
                )

                

                # add new row to scroll view in edit category screen
                new_row = SubCategoryRowWidget(new_name)

                # create edit subcategory btn functionality
                new_row.name_btn.bind(on_press=app.edit_category_screen.edit_subcategory_clicked(new_name))

                
                app.edit_category_screen.row_widgets[new_name] = new_row
                app.edit_category_screen.scroll_layout.add_widget(new_row)

                # move screen to accounts_screen
                app.switch_screen("edit_category_screen")(instance)

                app.transition_diagram.remove_node("add_subcategory_screen")

                app.screen_manager.remove_widget(app.add_subcategory_screen)



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


        return add
        
        
    


    def cancel_pressed(self, category, app):
        def cancel(instance):
            # clear text field entries
            self.name_text_field.text = ""
            if category.kind == "Expense":
                self.dropdown.dropdown_label.text = "Essential Expenses?"

                if self.error_essential_option in self.layout.children:
                    self.layout.remove_widget(self.error_essential_option)


            if self.name_text_field.error == True:
                self.name_text_field.error = False

                            

            app.switch_screen("edit_category_screen")(instance)
            app.transition_diagram.remove_node("add_subcategory_screen")
            app.screen_manager.remove_widget(app.add_subcategory_screen)
        return cancel