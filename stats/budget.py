from kivy.storage.jsonstore import JsonStore
from datas.account import Account
from datas.transaction import RecurringTransaction, RecurringTransfer
from datas.date import Date, date_is_in_interval
import asyncio



async def initialize_current_month_budget(date, account, recurring_acts_dict):
    current_month_budget = CurrentMonthBudget(date, account, recurring_acts_dict)
    if account != None:
        await current_month_budget._init()
    return current_month_budget

def create_current_month_budget(date, account, recurring_acts_dict):
    current_month_budget = asyncio.run(initialize_current_month_budget(date, account, recurring_acts_dict))
    return current_month_budget


class CurrentMonthBudget:
    def __init__(self, date: Date, account: Account, recurring_acts_dict: dict):
        '''
        date is a Date object

        account should be an Account object

        recurring_acts_dict has keys which are act_simple_dates ("dd/mm/yyyy hh:mm:ss"), and the values are either a RecurringTransaction object or a RecurringTransfer object

        This class has READ ONLY access to transactions.json and transfers.json
        '''

        self.date = date
        # build month_year from date (month_year is a tuple (month, year) with both ints)
        self.month_year = int(date.month), int(date.year)
        self.account = account
        self.recurring_acts_dict = recurring_acts_dict

        if account == None:
            return 

        # keep only recurring_acts that are relevant for this account
        kept_recurring_acts_dict = {}
        for recurring_act_simple_date in recurring_acts_dict:
            recurring_act = recurring_acts_dict[recurring_act_simple_date]
            if type(recurring_act) == RecurringTransaction:
                if recurring_act.account == account:
                    kept_recurring_acts_dict[recurring_act_simple_date] = recurring_act 
            
            elif type(recurring_act) == RecurringTransfer:
                if recurring_act.account_receiving == account or recurring_act.account_sending == account:
                    kept_recurring_acts_dict[recurring_act_simple_date] = recurring_act

        self.recurring_acts_dict = kept_recurring_acts_dict


        # the budget has read only access to stored transactions and transfers
        self.transfers_store = JsonStore("transfers.json")
        self.transactions_store = JsonStore("transactions.json")




    async def _init(self):
        # build info about budget
        task1 = asyncio.create_task(self.compute_transaction_data())
        task2 = asyncio.create_task(self.compute_transfers_data())
        task3 = asyncio.create_task(self.compute_recurring_data())
        task4 = asyncio.create_task(self.compute_essential_expenses_stats())

        transaction_data = await task1
        transfers_data = await task2
        # received_income is the total amount already received. Does not take into account future income from recurring acts
        self.received_income = round(transaction_data[0] + transfers_data[0], 2)    
        # amount spent is the total amount already spent from transactions and transfers. Does not take into account future expenses from recurring acts
        self.amount_spent = round(transaction_data[1] + transfers_data[1], 2)   
        
        recurring_data = await task3
        # income is the total amount received from transactions and transfers plus the amount to be received from future recurring acts in the current month_year
        self.income = round(self.received_income + recurring_data[0], 2) 
        # expenses is the total amount spent from transactions and transfers plus the amount to be spent in the future from recurring acts in the current month_year
        self.expenses = round(self.amount_spent + recurring_data[1], 2) 
        self.recurring_income = round(recurring_data[2], 2)
        self.recurring_expenses = round(recurring_data[3], 2)

        essentials_data = await task4
        self.essential_expenses = round(essentials_data[0], 2)
        self.non_essentials_expenses = round(essentials_data[1], 2)
        self.average_essential_expenses = round(essentials_data[2], 2)


    async def compute_transaction_data(self):
        '''
        returns a tuple (transactions_received_income, transactions_amount_spent)
        '''
        transaction_received_income = 0     
        transaction_amount_spent = 0    
        for _, transaction_info in self.transactions_store.find(month=self.date.month, year=self.date.year):
            if int(transaction_info["account"]) == self.account.number:
                value = float(transaction_info["value"])
                if value > 0:
                    transaction_received_income += value
                else:
                    transaction_amount_spent += -value
        return transaction_received_income, transaction_amount_spent


    async def compute_transfers_data(self):
        '''
        returns a tuple (transfers_received_income, transfers_amount_spent)
        '''
        transfers_received_income = 0
        transfers_amount_spent = 0
        for _, transfer_info in self.transfers_store.find(month=self.date.month, year=self.date.year):
            if "account_receiving" in transfer_info:
                if int(transfer_info["account_receiving"]) == self.account.number:
                    value = float(transfer_info["value"])
                    transfers_received_income += value 

            if "account_sending" in transfer_info:
                if int(transfer_info["account_sending"]) == self.account.number:
                    value = float(transfer_info["value"])
                    transfers_amount_spent += value 
        return transfers_received_income, transfers_amount_spent


    async def compute_recurring_data(self):
        '''
        returns a tuple (future_income, future_expenses, recurring_income, recurring_expenses)
        '''
        future_income = 0
        future_expenses = 0
        recurring_income = 0
        recurring_expenses = 0
        for simple_date in self.recurring_acts_dict:
            recurring_act = self.recurring_acts_dict[simple_date]

            if date_is_in_interval(
                    self.date.get_date_simple_string()[:10], 
                    recurring_act.start_date.get_date_simple_string()[:10], 
                    recurring_act.end_date.get_date_simple_string()[:10] if recurring_act.end_date != None else None
            ):
                
                if int(self.date.day) < recurring_act.month_day:
                    if type(recurring_act) == RecurringTransaction:
                        if recurring_act.value > 0:
                            future_income += recurring_act.value
                        else:
                            future_expenses += -recurring_act.value
                    

                    elif type(recurring_act) == RecurringTransfer:
                        if recurring_act.account_receiving == self.account:
                            future_income += recurring_act.value
                        if recurring_act.account_sending == self.account:
                            future_expenses += recurring_act.value
                

                if type(recurring_act) == RecurringTransaction:
                    if recurring_act.value > 0:
                        recurring_income += recurring_act.value

                    if recurring_act.value <= 0:
                        recurring_expenses += -recurring_act.value
                

                elif type(recurring_act) == RecurringTransfer:
                    if recurring_act.account_receiving == self.account:
                        recurring_income += recurring_act.value

                    if recurring_act.account_sending == self.account:
                        recurring_expenses += recurring_act.value
            
        return future_income, future_expenses, recurring_income, recurring_expenses

    
    def get_progress_bar_percentage(self):
        if self.recurring_income <= self.recurring_expenses:
            if self.income == 0:
                return 0
            if self.income <= self.expenses:
                return 0
            return round(100*(self.income - self.expenses)/self.income, 0)
        
        if (self.income - self.expenses) >= (self.recurring_income - self.recurring_expenses):
            return 100
        
        return round(100*(self.income - self.expenses)/(self.recurring_income - self.recurring_expenses), 0)


    async def compute_essential_expenses_stats(self):
        '''
        returns a tuple (essential_expenses, non_essential_expenses, average_essential_expenses)

        essential_expenses is the amount spent in the current display month on essential subcategories

        non_essential_expenses is the amount spent in the current display month on non-essential subcategories

        average_essential_expenses is the average amount spent on essential subcategories in a given month out of the months of the last two years
        '''
        essential_expenses = 0
        non_essential_expenses = 0
        essential_expenses_dict = {} # keys are (month_int, year_int) pairs and the value are the corresponding total month essential expenses


        current_month_year = int(self.date.month), int(self.date.year)
        month_year = current_month_year
        counter = 1
        while counter <= 24:
            # decrement month_year
            if month_year[0] == 1:
                month_year = (12, month_year[1] - 1)
            else:
                month_year = (month_year[0] - 1, month_year[1])

            essential_expenses_dict[month_year] = 0

            # increment counter
            counter += 1

        

        for transaction_simple_date in self.transactions_store.keys():
            transaction_info = self.transactions_store.get(transaction_simple_date)
            
            value = float(transaction_info["value"])
            month = transaction_info["month"]
            year = transaction_info["year"]
            category = transaction_info["category"]
            subcategory = transaction_info["subcategory"]
            account_number = int(transaction_info["account"])
            
            if value < 0 and month == self.date.month and year == self.date.year and category != None and subcategory != None and account_number == self.account.number:
                value = -value

                essential = JsonStore("categories.json").get(category)["subcategories"][subcategory]["essential"]

                if essential == "True":
                    essential_expenses += value
                    
                
                elif essential == "False":
                    non_essential_expenses += value


            month_year = int(month), int(year)
            if month_year in essential_expenses_dict and month_year != current_month_year:
                if value < 0 and category != None and subcategory != None and account_number == self.account.number:
                    value = -value
                    essential = JsonStore("categories.json").get(category)["subcategories"][subcategory]["essential"]
                    
                    if essential == "True":
                        essential_expenses_dict[month_year] += value

            
        total_month_essential_expenses = sum([value for value in essential_expenses_dict.values()])
        number_of_valid_months = 0
        for month_year in essential_expenses_dict:
            if essential_expenses_dict[month_year] != 0:
                number_of_valid_months += 1

        average_essential_expenses = 0
        if number_of_valid_months != 0:
            average_essential_expenses = round(total_month_essential_expenses / number_of_valid_months, 2)

        return essential_expenses, non_essential_expenses, average_essential_expenses


    def compute_non_essentials_budget(self):
        '''
        returns the initial budget minus the average spent on essential expenses minus everything already spent on non essentials
        '''

        essentials_overflow = self.essential_expenses - self.average_essential_expenses

        if essentials_overflow < 0:
            return round(self.income - self.expenses + self.essential_expenses - self.average_essential_expenses, 2)
        
        else:
            return round(self.income - self.expenses, 2)









        










   










