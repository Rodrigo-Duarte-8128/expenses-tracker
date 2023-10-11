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


class CategoryRowWidget(MDRelativeLayout):
    def __init__(self, category, **kwargs):
        super(CategoryRowWidget, self).__init__(**kwargs)

        self.category = category

        self.window_height = Window.size[1]


        self.size_hint_y = None

       
        self.height = self.window_height * 0.07

        self.name_btn = Button(
            text = category.name,
            color = (0, 0, 0, 1),
            background_color = light_grey,
            size_hint = (0.6, 0.9),
            pos_hint = {"x": 0, "y": 0},
            background_normal = ""
        )
        self.add_widget(self.name_btn)

        if category.kind == "Expense":
            color = red
        elif category.kind == "Income":
            color = green

        self.kind_label = MDRaisedButton(
            text = category.kind,
            disabled = True,
            halign = "center",
            disabled_color = color,
            md_bg_color_disabled = light_grey,
            size_hint = (0.4, 0.9),
            pos_hint = {"x": 0.6, "y": 0},
            elevation = 0,
            _radius = 0
        )
        self.add_widget(self.kind_label)



class CategoryRowWidgetOnlyName(MDRelativeLayout):
    def __init__(self, category, **kwargs):
        super(CategoryRowWidgetOnlyName, self).__init__(**kwargs)

        self.category = category

        self.window_height = Window.size[1]


        self.size_hint_y = None

        
        self.height = self.window_height * 0.07

      


        self.name_btn = Button(
            text = category.name,
            color = (0, 0, 0, 1),
            background_color = light_grey,
            size_hint = (1, 0.9),
            pos_hint = {"x": 0, "y": 0},
            background_normal = ""
        )
        self.add_widget(self.name_btn)


        

    
class SubCategoryRowWidget(MDRelativeLayout):
    def __init__(self, subcategory_name, **kwargs):
        super(SubCategoryRowWidget, self).__init__(**kwargs)

        self.window_height = Window.size[1]


        self.size_hint_y = None

        
        self.height = self.window_height * 0.07
        
       

        self.name_btn = Button(
            text = subcategory_name,
            color = (0, 0, 0, 1),
            background_color = light_grey,
            size_hint = (1, 0.9),
            pos_hint = {"x": 0, "y": 0},
            background_normal = ""
        )
        self.add_widget(self.name_btn)


        