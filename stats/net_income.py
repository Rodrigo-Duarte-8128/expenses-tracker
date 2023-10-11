from datas.account import Account
from datas.date import Date
import asyncio
from kivy.storage.jsonstore import JsonStore


async def initialize_net_income_stats(date, account):
    net_income_stats = NetIncomeStats(date, account)
    if account != None:
        await net_income_stats._init()
    return net_income_stats

def create_net_income_stats(date, account):
    net_income_stats = asyncio.run(initialize_net_income_stats(date, account))
    return net_income_stats


class NetIncomeStats:
    def __init__(self, date: Date, account: Account):
        self.date = date
        self.account = account



        # the NetIncome class has read only access to stored transactions and transfers
        self.transfers_store = JsonStore("transfers.json")
        self.transactions_store = JsonStore("transactions.json")
        
    
    async def _init(self):
        
        task1 = asyncio.create_task(self.compute_transactions_net_income())
        task2 = asyncio.create_task(self.compute_transfers_net_income())

        transactions_data = await task1
        transfers_data = await task2

        months_net_income = {}
        for month_year in transactions_data[0]:
            months_net_income[month_year] = round(transactions_data[0][month_year] + transfers_data[0][month_year], 2)
        
        years_net_income = {}
        for year in transactions_data[1]:
            years_net_income[year] = round(transactions_data[1][year] + transfers_data[1][year], 2)
        
        current_year_net_income = round(transactions_data[2] + transfers_data[2], 2)

        self.months_net_income = months_net_income
        self.years_net_income = years_net_income
        self.current_year_net_income = current_year_net_income




    async def compute_transactions_net_income(self):
        '''
        returns (months_net_income, years_net_income, current_year_net_income)

        where months_net_income is a dictionary consisting of keys which are month_years and values which are the net_income, eg d[(10, 2023)] = 124.

        years_net_income is a dictionary with keys which are years and values which are net_incomes, eg d[2022] = 234.
        
        '''
        months_net_income = {}
        years_net_income = {}
        current_year_net_income = 0


        current_month_year = int(self.date.month), int(self.date.year)
        month_year = current_month_year
        counter = 1
        while counter <= 5:
            # decrement month_year
            if month_year[0] == 1:
                month_year = (12, month_year[1]-1)
            else:
                month_year = (month_year[0] - 1, month_year[1])
            
            # build months_net_income
            months_net_income[month_year] = 0
            

            # increment counter
            counter += 1
        
        y_counter = 1
        year = current_month_year[1]
        while y_counter <= 5:
            year -= 1
            years_net_income[year] = 0
            y_counter += 1


        for transaction_simple_date in self.transactions_store.keys():
            transaction_info = self.transactions_store.get(transaction_simple_date)

            value = float(transaction_info["value"])
            account_number = int(transaction_info["account"])
            transaction_month_year = int(transaction_info["month"]), int(transaction_info["year"])

            if self.account.number == account_number:

                if transaction_month_year in months_net_income:
                    months_net_income[transaction_month_year] += value
                
                if transaction_month_year[1] in years_net_income:
                    years_net_income[transaction_month_year[1]] += value
                
                if transaction_month_year[1] == current_month_year[1]:
                    current_year_net_income += value
        
        return months_net_income, years_net_income, current_year_net_income
                
                


                
                


    
    async def compute_transfers_net_income(self):
        '''
        returns (months_net_income, years_net_income, current_year_net_income)

        where months_net_income is a dictionary eg d[(10, 2023)] = 124.

        years_net_income is a dictionary eg d[2022] = 234.
        
        '''
        months_net_income = {}
        years_net_income = {}
        current_year_net_income = 0


        current_month_year = int(self.date.month), int(self.date.year)
        month_year = current_month_year
        counter = 1
        while counter <= 5:
            # decrement month_year
            if month_year[0] == 1:
                month_year = (12, month_year[1]-1)
            else:
                month_year = (month_year[0] - 1, month_year[1])
            
            # build months_net_income
            months_net_income[month_year] = 0

            # increment counter
            counter += 1
        
        y_counter = 1
        year = current_month_year[1]
        while y_counter <= 5:
            year -= 1
            years_net_income[year] = 0
            y_counter += 1


        for transfer_simple_date in self.transfers_store.keys():
            transfer_info = self.transfers_store.get(transfer_simple_date)

            value = float(transfer_info["value"])
            if "account_sending" in transfer_info:
                account_sending_number = int(transfer_info["account_sending"])
            else:
                account_sending_number = None
            
            if "account_receiving" in transfer_info:
                account_receiving_number = int(transfer_info["account_receiving"])
            else:
                account_receiving_number = None

            
            transfer_month_year = int(transfer_info["month"]), int(transfer_info["year"])

            if self.account.number == account_sending_number:

                if transfer_month_year in months_net_income:
                    months_net_income[transfer_month_year] -= value
                
                if transfer_month_year[1] in years_net_income:
                    years_net_income[transfer_month_year[1]] -= value
                
                if transfer_month_year[1] == current_month_year[1]:
                    current_year_net_income -= value
            
            if self.account.number == account_receiving_number:

                if transfer_month_year in months_net_income:
                    months_net_income[transfer_month_year] += value
                
                if transfer_month_year[1] in years_net_income:
                    years_net_income[transfer_month_year[1]] += value
                
                if transfer_month_year[1] == current_month_year[1]:
                    current_year_net_income += value

        
        return months_net_income, years_net_income, current_year_net_income





