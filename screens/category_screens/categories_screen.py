from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from datas.category import Category, SubCategory
from datas.transaction import RecurringTransaction
from row_widgets.category_row_widget import CategoryRowWidget
from screens.category_screens.edit_category_screen import EditCategoryScreen
from screens.category_screens.add_category_screen import AddCategoryScreen


red = hex("#E63946")
cream = hex("#F1FAEE")
light_teal = hex("#A8DADC")
blue = hex("#457B9D")
dark_blue = hex("#1D3557")
green = hex("#84a98c")








class CategoriesScreen(MDScreen):
    def __init__(self, app, **kwargs):
        super(CategoriesScreen, self).__init__(**kwargs)

        self.app = app

        self.layout = MDFloatLayout()

        self.window_width, self.window_height = Window.size

        # get stored categories
        self.categories_store = JsonStore("categories.json")

        # Create Grid Layout that holds the Scroll View
        self.scroll_layout = MDGridLayout(
            cols=1,
            size_hint_y = None,
            size = (self.window_width, self.window_height * 0.75),
        )
        self.scroll_layout.bind(
            minimum_height=self.scroll_layout.setter("height")
        )
        self.scroll_layout.height = self.scroll_layout.minimum_height

        # build categories dictionary from storage, build row_widgets and scroll view
        self.categories_dict = {}
        self.row_widgets = {}

        
        
        category_names_list = list(self.categories_store.keys())
        category_names_list.sort()

        for category_name in category_names_list:
            
            subcategories = {}
            subcategories_dict = self.categories_store.get(category_name)["subcategories"]
            for subcategory_name in subcategories_dict:
                essential_str = subcategories_dict[subcategory_name]["essential"]
                if essential_str == "True":
                    essential = True
                else:
                    essential = False

                subcategory = SubCategory(
                    subcategories_dict[subcategory_name]["name"],
                    category_name,
                    essential = essential
                )
                subcategories[subcategory_name] = subcategory

            category = Category(
                category_name,
                self.categories_store.get(category_name)["kind"],
                subcategories
            )

            self.categories_dict[category_name] = category

            row = CategoryRowWidget(category)

            # create edit category btn functionality
            row.name_btn.bind(on_press=self.edit_category_clicked(category))

            
            self.row_widgets[category_name] = row
            self.scroll_layout.add_widget(row)
        

        # Create Scroll View
        self.scroll_view = MDScrollView(
            size_hint = (1, 0.75),
            pos_hint = {"x": 0, "y": 0.05},
            bar_width = 10
        )
        self.scroll_view.add_widget(self.scroll_layout)
        self.layout.add_widget(self.scroll_view)
        

        

        
        # Create label for the categories list
        self.categories_label = MDLabel(
            text = "Categories",
            pos_hint = {"x": 0.3, "y": 0.85},
            size_hint = (0.4, 0.05),
            halign = "center"
        )
        self.layout.add_widget(self.categories_label)




        # Create Categories Scroll View Headers
        self.category_name_label = MDRaisedButton(
            text = "Category",
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            md_bg_color_disabled = blue,
            size_hint = (0.6, 0.05),
            pos_hint = {"x": 0, "y": 0.8},
            elevation = 0,
            _radius = 0
        )
        self.layout.add_widget(self.category_name_label)

        self.kind_label = MDRaisedButton(
            text = "Kind",
            disabled = True,
            disabled_color = (1, 1, 1, 1),
            md_bg_color_disabled = blue,
            size_hint = (0.4, 0.05),
            pos_hint = {"x": 0.6, "y": 0.8},
            elevation = 0,
            _radius = 0
        )
        self.layout.add_widget(self.kind_label)

                

        


        # Create new category button
        self.new_category_btn = MDRaisedButton(
            text = "New Category",
            size_hint = (0.4, 0.04),
            pos_hint = {"x": 0.3, "y": 0.005},
            md_bg_color = blue,
            on_press = self.new_category_clicked()
        )
        self.layout.add_widget(self.new_category_btn)

       
        self.add_widget(self.layout)


    def new_category_clicked(self):
        def new(instance):
            self.app.add_category_screen = AddCategoryScreen(self.app, name="add_category_screen")
            self.app.screen_manager.add_widget(self.app.add_category_screen)

            self.app.transition_diagram.add_node(
                "add_category_screen",
                root_screen_node = self.app.categories_screen_node,
                left_node = self.app.categories_screen_node
            )

            self.app.switch_screen("add_category_screen")(instance)
        return new



    def edit_category_clicked(self, category):
        def edit(instance):
            # create edit category screen
            self.app.edit_category_screen = EditCategoryScreen(category, self.app, name="edit_category_screen")
            self.app.screen_manager.add_widget(self.app.edit_category_screen)

            self.app.transition_diagram.add_node(
                "edit_category_screen",
                root_screen_node = self.app.categories_screen_node,
                left_node = self.app.categories_screen_node
            )

            # move screen
            self.app.switch_screen("edit_category_screen")(instance)
        return edit
    



    def refresh_screen(self):
        # re-build the scroll view holding the categories information based on the current categories dictionary
        displayed_category_names = list(self.row_widgets.keys())
        for category_name in displayed_category_names:
            self.scroll_layout.remove_widget(self.row_widgets[category_name])
            
        self.row_widgets = {}


        category_names_list = list(self.categories_dict.keys())
        category_names_list.sort()

        for category_name in category_names_list:
            category = self.categories_dict[category_name]
        
            row = CategoryRowWidget(category)

            # create edit account btn functionality
            row.name_btn.bind(on_press=self.edit_category_clicked(category))
            
            self.row_widgets[category_name] = row
            self.scroll_layout.add_widget(row)


    def add_category(self, category, refresh=True):
        # add new category to storage
        subcategories_dict = {}
        
        for subcategory_name in category.subcategories:
            subcategories_dict[subcategory_name] = {
                "name": category.subcategories[subcategory_name].name,
                "essential": str(category.subcategories[subcategory_name].essential)
            }

        self.categories_store.put(
            category.name,
            kind = category.kind,
            subcategories = subcategories_dict
        )

        # add new category instance to categories_dict
        self.categories_dict[category.name] = category

        # add new category to scroll view
        row = CategoryRowWidget(category)
        self.scroll_layout.add_widget(row)

        # create edit category btn functionality
        row.name_btn.bind(on_press=self.edit_category_clicked(category))

        # add new category to row_widgets
        self.row_widgets[category.name] = row

        if refresh:
            # refresh the scroll view in category_screen
            self.refresh_screen()



    def edit_category(self, category, changes_dict):
        '''
        changes_dict has the form
        {
            "name": new_category_name,
            "kind": new_category_kind,
            "subcategories": new_subcategory_dict (keys are subcategory names and values are SubCategory objects)
        }

        Notes: 
            - keys are optional
            - if the name changes then this updates all the related transactions, by changing the name of the category
            - if the subcategories change, this function does not affect the subcategory attributes of the transactions, this
              should be done in the edit_subcategory_screen, when editting a subcategory
        '''
        self.categories_store.delete(category.name)
        old_kind = category.kind
        if "kind" in changes_dict:
            new_kind = changes_dict["kind"]
            if old_kind != new_kind:
                category.kind = changes_dict["kind"]

                # flip the value of all transactions associated to this category
                dates_list = []
                for transaction_simple_date, _ in self.app.records_screen.transactions_store.find(category=category.name):
                    dates_list.append(transaction_simple_date)

                for transaction_simple_date in dates_list:
                    if transaction_simple_date in self.app.records_screen.acts_in_use_dict:
                        transaction = self.app.records_screen.acts_in_use_dict[transaction_simple_date]
                        
                        self.app.records_screen.edit_transaction(
                            transaction,
                            {
                                "value": -transaction.value,
                            }
                        )
                
                    else:
                        transaction = self.app.records_screen.get_transaction_from_storage(transaction_simple_date)
                        self.app.records_screen.edit_transaction(
                            transaction,
                            {
                                "value": -transaction.value,
                            }
                        )

                # flip value of related recurring transactions
                for recurring_transaction_name in self.app.recurring_acts_screen.recurring_acts_dict:
                    recurring_transaction = self.app.recurring_acts_screen.recurring_acts_dict[recurring_transaction_name]
                    if type(recurring_transaction) == RecurringTransaction:
                        if recurring_transaction.category == category:
                            recurring_transaction.value = -recurring_transaction.value
                            self.app.recurring_acts_screen.recurring_transactions_store.delete(recurring_transaction.name)
                            self.app.recurring_acts_screen.store_recurring_transaction(recurring_transaction)
        
        if "name" in changes_dict:
            # remove category from categories_dict since its position is changing
            del self.categories_dict[category.name]

            old_name = category.name

            category.name = changes_dict["name"]

            self.categories_dict[category.name] = category
            

            # change all the transactions associated to this category
            dates_list = []
            for transaction_simple_date, _ in self.app.records_screen.transactions_store.find(category = old_name):
                dates_list.append(transaction_simple_date)

            for transaction_simple_date in dates_list:
                if transaction_simple_date in self.app.records_screen.acts_in_use_dict:
                    transaction = self.app.records_screen.acts_in_use_dict[transaction_simple_date]
                    self.app.records_screen.edit_transaction(
                        transaction,
                        {
                            "category": changes_dict["name"],
                        }
                    )
                
                else:
                    transaction = self.app.records_screen.get_transaction_from_storage(transaction_simple_date)
                    self.app.records_screen.edit_transaction(
                        transaction,
                        {
                            "category": changes_dict["name"],
                        }
                    )

            
            # update category name in related recurring transaction
            for recurring_transaction_name in self.app.recurring_acts_screen.recurring_acts_dict:
                recurring_transaction = self.app.recurring_acts_screen.recurring_acts_dict[recurring_transaction_name]
                if type(recurring_transaction) == RecurringTransaction:
                    if recurring_transaction.category == category:
                        self.app.recurring_acts_screen.recurring_transactions_store.delete(recurring_transaction.name)
                        self.app.recurring_acts_screen.store_recurring_transaction(recurring_transaction)


        if "subcategories" in changes_dict:
            category.subcategories = changes_dict["subcategories"]

        
           

        
        subcategories_dict = {}
        for subcategory_name in category.subcategories:
            subcategories_dict[subcategory_name] = {
                "name": category.subcategories[subcategory_name].name,
                "essential": str(category.subcategories[subcategory_name].essential)
            }

        self.categories_store.put(
            category.name,
            kind=category.kind,
            subcategories=subcategories_dict
        )

        #if category.name not in self.categories_dict:
            

        self.refresh_screen()
        self.app.recurring_acts_screen.refresh_row_widgets()

        if old_kind != category.kind:
            self.app.home_screen.refresh_row_widgets()

        
        







    def remove_category(self, category, refresh=True):
        # set related transactions category attribute to None and update old_category_name and old_subcategory_name
        dates_list = []
        for transaction_simple_date, _ in self.app.records_screen.transactions_store.find(category=category.name):
            dates_list.append(transaction_simple_date)

        for transaction_simple_date in dates_list:
            if transaction_simple_date in self.app.records_screen.acts_in_use_dict:
                transaction = self.app.records_screen.acts_in_use_dict[transaction_simple_date]
                if transaction.subcategory != None:
                    old_subcategory_name = transaction.subcategory.name
                else:
                    old_subcategory_name = transaction.old_subcategory_name
                self.app.records_screen.edit_transaction(
                    transaction,
                    {
                        "category": None,
                        "subcategory": None,
                        "old_category_name": category.name,
                        "old_subcategory_name": old_subcategory_name
                    }
                )

            else:
                transaction = self.app.records_screen.get_transaction_from_storage(transaction_simple_date)
                if transaction.subcategory != None:
                    old_subcategory_name = transaction.subcategory.name
                else:
                    old_subcategory_name = transaction.old_subcategory_name
                self.app.records_screen.edit_transaction(
                    transaction,
                    {
                        "category": None,
                        "subcategory": None,
                        "old_category_name": category.name,
                        "old_subcategory_name": old_subcategory_name
                    }
                )

        # update related recurring transactions
        for recurring_transaction_name in self.app.recurring_acts_screen.recurring_acts_dict:
            recurring_transaction = self.app.recurring_acts_screen.recurring_acts_dict[recurring_transaction_name]
            if type(recurring_transaction) == RecurringTransaction:
                if recurring_transaction.category == category:
                    if recurring_transaction.subcategory != None:
                        old_subcategory_name = recurring_transaction.subcategory.name
                    else:
                        old_subcategory_name = recurring_transaction.old_subcategory_name
                    
                    recurring_transaction.category = None
                    recurring_transaction.subcategory = None
                    recurring_transaction.old_category_name = category.name
                    recurring_transaction.old_subcategory_name = old_subcategory_name

                    self.app.recurring_acts_screen.recurring_transactions_store.delete(recurring_transaction.name)
                    self.app.recurring_acts_screen.store_recurring_transaction(recurring_transaction)





        # remove category from storage and categories_dict
        self.categories_store.delete(category.name)
        del self.categories_dict[category.name]
        
        # remove category from scroll view
        category_row = self.row_widgets[category.name]
        self.scroll_layout.remove_widget(category_row)

        # remove cateogry from rows dict
        del self.row_widgets[category.name]

        if refresh:
            # refresh scroll view
            self.refresh_screen()







