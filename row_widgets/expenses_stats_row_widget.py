from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex
from kivy.uix.button import Button
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar




red = hex("#E63946")
cream = hex("#F1FAEE")
light_teal = hex("#A8DADC")
blue = hex("#457B9D")
dark_blue = hex("#1D3557")
green = hex("#84a98c")
light_grey = hex("#e0e0e0")


class ExpensesStatsRowWidget(MDRelativeLayout):
    def __init__(self, expenses_stats, category, subcategory, **kwargs):
        super(ExpensesStatsRowWidget, self).__init__(**kwargs)

        self.expenses_stats = expenses_stats
        self.category = category
        self.subcategory = subcategory

        self.window_height = Window.size[1]

        self.size_hint_y = None


        self.height = self.window_height * 0.1


        
        if subcategory == None:
            cat_total = self.expenses_stats.get_category_expenses(self.category, None)
            total = self.expenses_stats.get_total_expenses()
            if cat_total == int(cat_total):
                cat_total = int(cat_total)
            if total == int(total):
                total = int(total)


            if total == 0:
                display = "N/A"
            else:
                p = round(cat_total/total * 100, 2)
                if p == int(p):
                    p = int(p)
                display = f"{self.category.name}: \u20ac{cat_total} ({p}%)"

            


            self.category_name_btn = Button(
                text = display,
                color = (0, 0, 0, 1),
                background_color = light_grey,
                pos_hint = {"x": 0.1 ,"y": 0.55},
                size_hint = (0.8, 0.4),
                background_normal = "",
                halign = "left",
            )
            self.add_widget(self.category_name_btn)



            # Create progress bar
            if total == 0:
                percentage = 0
            else:
                percentage = int(round(cat_total / total * 100, 0))


            self.progress_bar = MDProgressBar(
                value = percentage,
                pos_hint = {"x": 0.1, "y": 0.15},
                size_hint = (0.8, 0.35),
                color = dark_blue
            )
            self.add_widget(self.progress_bar)


        if subcategory != None:
            cat_total = self.expenses_stats.get_category_expenses(self.category, self.subcategory)
            total = self.expenses_stats.get_total_expenses()
            if cat_total == int(cat_total):
                cat_total = int(cat_total)
            if total == int(total):
                total = int(total)



            if total == 0:
                display = "N/A"
            else:
                p = round(cat_total / total * 100, 2)
                if p == int(p):
                    p = int(p)
                display = f"{self.category.name}/{self.subcategory.name}: \u20ac{cat_total} ({p}%)"

           


            self.category_name_btn = Button(
                text = display,
                color = (0, 0, 0, 1),
                background_color = light_grey,
                pos_hint = {"x": 0.1 ,"y": 0.55},
                size_hint = (0.8, 0.4),
                background_normal = "",
            )
            self.add_widget(self.category_name_btn)



            # Create progress bar
            if total == 0:
                percentage = 0
            else:
                percentage = int(round(cat_total / total * 100, 0))

            self.progress_bar = MDProgressBar(
                value = percentage,
                pos_hint = {"x": 0.1, "y": 0.15},
                size_hint = (0.8, 0.35),
                color = dark_blue
            )
            self.add_widget(self.progress_bar)

