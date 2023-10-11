from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button


class CustomDropDown(DropDown):
    def __init__(self, main_text, pos_hint, size_hint, text_list, color, height, **kwargs):
        super(CustomDropDown, self).__init__(**kwargs)
        self.height = height
        self.color = color

        self.dropdown = DropDown()

        for text in text_list:
            btn = Button(
                text = text,
                size_hint_y = None,
                height = height,
                color = (1, 1, 1, 1),
                background_color = color,
                background_normal = ""
            )
            
            btn.bind(on_release=self.btn_pressed())
            self.dropdown.add_widget(btn)

        
        self.dropdown_label = Button(
            text = main_text,
            size_hint = size_hint,
            pos_hint = pos_hint,
            color = (1, 1, 1, 1),
            background_color = color,
            background_normal = ""
        )
        self.dropdown_label.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.dropdown_label, 'text', x))


    def btn_pressed(self):
        def press(btn):
            self.dropdown.select(btn.text)
            if btn.text == "Yes":
                btn.text = "No"

            elif btn.text == "No":
                btn.text = "Yes"


            elif btn.text == "Income":
                self.dropdown.clear_widgets()
                

                new_btn = Button(
                text = "Expense",
                size_hint_y = None,
                height = self.height,
                color = (1, 1, 1, 1),
                background_color = self.color,
                background_normal = ""
                )
                new_btn.bind(on_release=self.btn_pressed())
                self.dropdown.add_widget(new_btn)
                
            elif btn.text == "Expense":
                self.dropdown.clear_widgets()

                new_btn = Button(
                text = "Income",
                size_hint_y = None,
                height = self.height,
                color = (1, 1, 1, 1),
                background_color = self.color,
                background_normal = ""
                )
                new_btn.bind(on_release=self.btn_pressed())
                self.dropdown.add_widget(new_btn)

            elif btn.text == "Essential":
                self.dropdown.clear_widgets()

                new_btn = Button(
                text = "Non-essential",
                size_hint_y = None,
                height = self.height,
                color = (1, 1, 1, 1),
                background_color = self.color,
                background_normal = ""
                )
                new_btn.bind(on_release=self.btn_pressed())
                self.dropdown.add_widget(new_btn)

            elif btn.text == "Non-essential":
                self.dropdown.clear_widgets()

                new_btn = Button(
                text = "Essential",
                size_hint_y = None,
                height = self.height,
                color = (1, 1, 1, 1),
                background_color = self.color,
                background_normal = ""
                )
                new_btn.bind(on_release=self.btn_pressed())
                self.dropdown.add_widget(new_btn)



        return press

