from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex
from kivy.uix.button import Button
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.button import MDRaisedButton





red = hex("#E63946")
cream = hex("#F1FAEE")
light_teal = hex("#A8DADC")
blue = hex("#457B9D")
dark_blue = hex("#1D3557")
green = hex("#84a98c")
light_grey = hex("#e0e0e0")


class RecurringTransactionRowWidget(MDRelativeLayout):
    def __init__(self, recurring_transaction, **kwargs):
        super(RecurringTransactionRowWidget, self).__init__(**kwargs)

        self.recurring_transaction = recurring_transaction

        self.window_height = Window.size[1]

        self.size_hint_y = None

        
        
        self.height = self.window_height * 0.1




        self.name_label = MDRaisedButton(
            text = recurring_transaction.name,
            halign = "center",
            disabled = True,
            disabled_color = (0, 0, 0, 1),
            md_bg_color_disabled = light_grey,
            size_hint = (0.2, 0.9),
            pos_hint = {"x": 0, "y": 0.05},
            elevation = 0,
            _radius = 0
        )
        self.add_widget(self.name_label)



        if recurring_transaction.category != None:
            display_category = recurring_transaction.category.name       
            if recurring_transaction.subcategory != None:
                display_category += f" / {recurring_transaction.subcategory.name}"
            elif recurring_transaction.old_subcategory_name != None:
                display_category += f" / {recurring_transaction.old_subcategory_name}"
        else:
            if recurring_transaction.old_category_name != None:
                display_category = recurring_transaction.old_category_name
                if recurring_transaction.old_subcategory_name != None:
                    display_category += f" / {recurring_transaction.old_subcategory_name}"

        self.category_btn = Button(
            text=display_category, 
            color = (0, 0, 0, 1),
            background_color=light_grey, 
            size_hint=(0.6, 0.9), 
            pos_hint={"x": 0.2, "y": 0.05},
            background_normal = "",
        )
        self.add_widget(self.category_btn)


        
     


        if recurring_transaction.value < 0:
            value_color = red
        else:
            value_color = green

        display_value = str(recurring_transaction.value)
        if recurring_transaction.value == int(recurring_transaction.value):
            display_value = str(int(recurring_transaction.value)) # if value ends in .0 remove the decimal part

        if recurring_transaction.value >= 0:
            display_value = f"+{display_value}\u20ac"
        else:
            display_value = f"{display_value}\u20ac"

        self.value_label = MDRaisedButton(
            text = display_value,
            disabled = True,
            halign = "left",
            disabled_color = value_color,
            md_bg_color_disabled = light_grey,
            size_hint = (0.2, 0.9),
            pos_hint = {"x": 0.8, "y": 0.05},
            elevation = 0,
            _radius = 0
        )
        self.add_widget(self.value_label)
        


    