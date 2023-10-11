from kivy.storage.jsonstore import JsonStore
from datas.date import Date
from datas.account import Account
from datas.transaction import RecurringTransaction


class ExpensesStats:
    def __init__(self, date: Date, account: Account, recurring_acts_dict: dict ):
        self.date = date
        self.account = account
        self.recurring_acts_dict = recurring_acts_dict

        self.transactions_store = JsonStore("transactions.json")


    def get_total_expenses(self):
        '''
        returns the sum of values for transactions that are expenditures from the current month. Includes recurring_transactions that haven't occured yet
        '''
        total = 0       
        for _, transaction_info in self.transactions_store.find(month=self.date.month, year=self.date.year):
            value = float(transaction_info["value"])
            if self.account.number == int(transaction_info["account"]) and value < 0:
                total += -value

        for recurring_act_name in self.recurring_acts_dict:
            recurring_act = self.recurring_acts_dict[recurring_act_name]
            if type(recurring_act) == RecurringTransaction and recurring_act.month_day > int(self.date.day):
                if recurring_act.account == self.account:
                    if recurring_act.value < 0:
                        total += -recurring_act.value

        return round(total, 2)
    


    def get_category_expenses(self, category, subcategory):
        '''
        if subcategory is None, this returns all the expenses from the category
        otherwise it returns only expenses from the correct subcategory
        
        category has to be a Category object
        
        subcategory is a SubCategory object or None
        '''
        total = 0
        for _, transaction_info in self.transactions_store.find(month=self.date.month, year=self.date.year):
            value = float(transaction_info["value"])
            if self.account.number == int(transaction_info["account"]) and value < 0 and category.name == transaction_info["category"]:
                if subcategory == None:
                    total += -value
                else:
                    if subcategory.name == transaction_info["subcategory"]:
                        total += -value

        
    
        for recurring_act_name in self.recurring_acts_dict:
            recurring_act = self.recurring_acts_dict[recurring_act_name]
            if type(recurring_act) == RecurringTransaction and recurring_act.month_day > int(self.date.day):
                if recurring_act.account == self.account:
                    if recurring_act.value < 0 and recurring_act.category == category:
                        if subcategory == None:
                            total += -recurring_act.value
                        else:
                            if recurring_act.subcategory == subcategory:
                                total += -recurring_act.value

        return round(total, 2)



        