from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex as hex
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.button import MDRaisedButton



red = hex("#E63946")
cream = hex("#F1FAEE")
light_teal = hex("#A8DADC")
blue = hex("#457B9D")
dark_blue = hex("#1D3557")
light_grey = hex("#e0e0e0")


class AccountRowWidget(MDRelativeLayout):
    def __init__(self, account, **kwargs):
        super(AccountRowWidget, self).__init__(**kwargs)

        self.account = account

        self.window_height = Window.size[1]

        self.size_hint_y = None

        
        self.height = self.window_height * 0.1


        self.number_label = MDRaisedButton(
            text = str(account.number),
            disabled = True,
            disabled_color = (0, 0, 0, 1),
            md_bg_color_disabled = light_grey,
            size_hint = (0.2, 0.9),
            pos_hint = {"x": 0, "y": 0},
            elevation = 0,
            _radius = 0
        )
        self.add_widget(self.number_label)


        

        self.account_name_btn = Button(
            text=account.name, 
            color = (0, 0, 0, 1),
            background_color=light_grey, 
            size_hint=(0.5, 0.9), 
            pos_hint={"x": 0.2, "y": 0},
            background_normal = "",
        )
        self.add_widget(self.account_name_btn)


        
        simpler_balance = account.balance
        if simpler_balance == int(simpler_balance):
            simpler_balance = int(simpler_balance)

        self.balance_label = MDRaisedButton(
            text = f"\u20ac {simpler_balance}",
            disabled = True,
            halign = "left",
            disabled_color = (0, 0, 0, 1),
            md_bg_color_disabled = light_grey,
            size_hint = (0.3, 0.9),
            pos_hint = {"x": 0.7, "y": 0},
            elevation = 0,
            _radius = 0
        )
        self.add_widget(self.balance_label)


    