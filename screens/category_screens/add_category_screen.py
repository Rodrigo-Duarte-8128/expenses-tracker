from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex
from kivymd.uix.screen import MDScreen
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from datas.category import Category
from dropdown.custom_dropdown import CustomDropDown

red = hex("#E63946")
cream = hex("#F1FAEE")
light_teal = hex("#A8DADC")
blue = hex("#457B9D")
dark_blue = hex("#1D3557")
green = hex("#84a98c")



class AddCategoryScreen(MDScreen):
    def __init__(self, app, **kwargs):
        super(AddCategoryScreen, self).__init__(**kwargs)

        self.layout = MDFloatLayout()

        self.window_width, self.window_height = Window.size


        # Create Add Category Label
        self.add_category_label = MDLabel(
            text="Add Category", 
            pos_hint = {"x": 0.3, "y": 0.85},
            size_hint = (0.4, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.add_category_label)


        # Create Text Fields
        self.name_text_field = MDTextField(
            hint_text = "Enter the Category Name",
            mode = "rectangle",
            helper_text = "Category name already exists.",
            helper_text_mode = "on_error",
            pos_hint = {"x": 0.1, "y": 0.6},
            size_hint = (0.8, 0.2)
        )
        self.layout.add_widget(self.name_text_field)




        # Create dropdown

        self.dropdown = CustomDropDown(
            "Select Category Kind",
            {"x": 0.1, "y": 0.4},
            (0.8, 0.05),
            [
                "Expense",
                "Income",
            ],
            blue,
            self.window_height * 0.05
        )
        self.layout.add_widget(self.dropdown.dropdown_label)

      



        # Create error message
        self.error_kind_label = MDLabel(
            text="Please choose a kind.", 
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
            on_press = self.cancel_pressed(app)
        )
        self.layout.add_widget(self.cancel_btn)


        self.add_category_btn = MDRaisedButton(
            text="Add", 
            md_bg_color = blue, 
            size_hint=(0.45, 0.04),
            pos_hint={"x": 0.525, "y": 0.005},
            on_press = self.add_category(app)
        )
        self.layout.add_widget(self.add_category_btn)



        # Add layout to Add Account Screen
        self.add_widget(self.layout)



    def add_category(self, app):
        def add(instance):
            errors = []
            name = self.name_text_field.text 
            kind = self.dropdown.dropdown_label.text


            if name in app.categories_screen.categories_dict:
                errors.append("name_already_exists")

            if kind not in ["Expense", "Income", "Transfer"]:
                errors.append("invalid_kind")

            
           
            if not errors:


                # add new category instance to categories_dict
                new_category = Category(name, kind, {})
                app.categories_screen.add_category(new_category)

                
                # clear text field entries
                self.name_text_field.text = ""
                self.dropdown.dropdown_label.text = "Select Category Kind"


                # move screen to accounts_screen
                app.switch_screen("categories_screen")(instance)

                # remove add category screen
                app.screen_manager.remove_widget(app.add_category_screen)

                app.transition_diagram.remove_node("add_category_screen")



            if "name_already_exists" in errors:
                if self.name_text_field.error == False:
                    self.name_text_field.error = True

            if "name_already_exists" not in errors:
                if self.name_text_field.error == True:
                    self.name_text_field.error = False

            
            if "invalid_kind" in errors:
                if self.error_kind_label not in self.layout.children:
                    self.layout.add_widget(self.error_kind_label)

            if "invalid_kind" not in errors:
                if self.error_kind_label in self.layout.children:
                    self.layout.remove_widget(self.error_kind_label)

        return add
        
        
    


    def cancel_pressed(self, app):
        def cancel(instance):
            app.switch_screen("categories_screen")(instance)
            app.transition_diagram.remove_node("add_category_screen")
            app.screen_manager.remove_widget(app.add_category_screen)
        return cancel
        
            

