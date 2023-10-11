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


class RecurringTransferRowWidget(MDRelativeLayout):
    def __init__(self, recurring_transfer, **kwargs):
        super(RecurringTransferRowWidget, self).__init__(**kwargs)
        '''
        status is a string which is either "sent" or "received", saying if this transfer was received or sent (influences value color and impact in account)
        '''
        self.recurring_transfer = recurring_transfer
        

        self.window_height = Window.size[1]

        self.size_hint_y = None

        
        
        self.height = self.window_height * 0.1



        self.name_label = MDRaisedButton(
            text = recurring_transfer.name,
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


      


        if recurring_transfer.account_sending != None and recurring_transfer.account_receiving != None:
            display_account = f"{recurring_transfer.account_sending.name} -> {recurring_transfer.account_receiving.name}"
        elif recurring_transfer.account_sending != None and recurring_transfer.account_receiving == None:
            display_account = f"{recurring_transfer.account_sending.name} -> Unknown"
        elif recurring_transfer.account_sending == None and recurring_transfer.account_receiving != None:
            display_account = f"Unknown -> {recurring_transfer.account_receiving.name}"



        self.account_btn = Button(
            text=display_account, 
            color = (0, 0, 0, 1),
            background_color=light_grey, 
            size_hint=(0.6, 0.9), 
            pos_hint={"x": 0.2, "y": 0.05},
            background_normal = "",
        )
        self.add_widget(self.account_btn)




        


        display_value = str(recurring_transfer.value)
        if recurring_transfer.value == int(recurring_transfer.value):
            display_value = str(int(recurring_transfer.value)) # if value ends in .0 remove decimal part
        display_value = f"{display_value}\u20ac"


        self.value_label = MDRaisedButton(
            text = display_value,
            disabled = True,
            halign = "left",
            disabled_color = (0, 0, 0, 1),
            md_bg_color_disabled = light_grey,
            size_hint = (0.2, 0.9),
            pos_hint = {"x": 0.8, "y": 0.05},
            elevation = 0,
            _radius = 0
        )
        self.add_widget(self.value_label)
        