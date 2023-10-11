from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex
from kivy.uix.button import Button
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel




red = hex("#E63946")
cream = hex("#F1FAEE")
light_teal = hex("#A8DADC")
blue = hex("#457B9D")
dark_blue = hex("#1D3557")
green = hex("#84a98c")
light_grey = hex("#e0e0e0")


class TransactionRowWidget(MDRelativeLayout):
    def __init__(self, transaction, **kwargs):
        super(TransactionRowWidget, self).__init__(**kwargs)

        self.act = transaction

        self.window_height = Window.size[1]

        self.size_hint_y = None

        
        
        self.height = self.window_height * 0.1


        calendar = {
            1: "Jan",
            2: "Feb",
            3: "Mar",
            4: "Apr",
            5: "May",
            6: "Jun",
            7: "Jul",
            8: "Aug",
            9: "Sep",
            10: "Oct",
            11: "Nov",
            12: "Dec"
        }



        day_month = f"{int(transaction.date.day)} {calendar[int(transaction.date.month)]}"

        hour_minutes = f"{int(transaction.date.hour)}:{transaction.date.minutes}"


        self.date_label = MDRaisedButton(
            text = day_month,
            halign = "center",
            disabled = True,
            disabled_color = (0, 0, 0, 1),
            md_bg_color_disabled = light_grey,
            size_hint = (0.2, 0.5),
            pos_hint = {"x": 0, "y": 0.45},
            elevation = 0,
            _radius = 0
        )
        self.add_widget(self.date_label)


        self.time_label = MDRaisedButton(
            text = hour_minutes,
            halign = "center",
            disabled = True,
            disabled_color = (0, 0, 0, 1),
            md_bg_color_disabled = light_grey,
            size_hint = (0.2, 0.4),
            pos_hint = {"x": 0, "y": 0.05},
            elevation = 0,
            _radius = 0
        )
        self.add_widget(self.time_label)

        if transaction.category != None:
            display_category = transaction.category.name       
            if transaction.subcategory != None:
                display_category += f" / {transaction.subcategory.name}"
            elif transaction.old_subcategory_name != None:
                display_category += f" / {transaction.old_subcategory_name}"
        else:
            if transaction.old_category_name != None:
                display_category = transaction.old_category_name
                if transaction.old_subcategory_name != None:
                    display_category += f" / {transaction.old_subcategory_name}"

        self.category_btn = Button(
            text=display_category, 
            color = (0, 0, 0, 1),
            background_color=light_grey, 
            size_hint=(0.6, 0.9), 
            pos_hint={"x": 0.2, "y": 0.05},
            background_normal = "",
        )
        self.add_widget(self.category_btn)



        self.note_label = MDLabel(
            text = self.act.note,
            halign = "center",
            pos_hint = {"x": 0.2, "y": 0.05},
            size_hint = (0.6, 0.35),
            font_style = "Body2"
        )
        self.add_widget(self.note_label)


        


        if transaction.value < 0:
            value_color = red
        else:
            value_color = green

        display_value = str(transaction.value)
        if transaction.value == int(transaction.value):
            display_value = str(int(transaction.value)) # if value ends in .0 remove it

        if transaction.value >= 0:
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
        


    