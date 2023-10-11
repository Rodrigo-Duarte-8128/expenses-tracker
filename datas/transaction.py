
from datas.date import Date
class Transaction:
    '''
    A transaction can be an expenditure or an income. 
    A transaction has the following attributes:
        
        - value: the amount that was transacted.
            
        - kind: specifies if the transaction is an "Income" or "Expenditure". The type is "Income" if value >= 0, and the 
                type is "Expenditure" if value < 0.

        - category: Category object that this transaction belongs to.

        - subcategory: optional argument that defaults to None. Accepts a SubCategory object which specifies the subcategory. 
        
        - account: string specifying the Account object that this transaction will act on.

        - note: a string which defaults to "" which can be used to give additional information about the transaction.

        - recurrent: this specifies if this transaction occurs every month or if it is a one-time transaction. If recurrent == None,
                    then the transaction is considered to be a one-time transaction. Otherwise, recurrent should be a string containing
                    the day of the month when this transaction occurs, eg recurrent=="15" (recurrent cannot be larger than 28).

        - date: a transaction is completely characterized by its date, which is a Date object. The Date object has attributes for the 
                year, month, day, hour, minute and second when the transaction was added.


    Transactions are stored as follows:
    {"date_simple_string": {
        "month": month,
        "year": year,
        "value": value,
        "category": category_name,
        "subcategory": subcategory_name or None,
        "old_category_name": old_category_name or None,
        "old_subcategory_name": old_subcategory_name or None,
        "account": account_number,
        "note": note,
        "recurrent": recurring_day or None
        }
    }

         
    ''' 
    
    
    def __init__(self, date, value: float, category, account, note: str, subcategory=None, old_category_name: str = None, old_subcategory_name: str = None):
        
        self.date = date
        self.value = value
        self.category = category
        self.account = account 
        self.note = note
        self.subcategory = subcategory
        self.old_category_name = old_category_name
        self.old_subcategory_name = old_subcategory_name
        
        if self.value >= 0:
            self.kind = "Income"
        elif self.value < 0:
            self.kind = "Expenditure"
        


class Transfer:
    '''
    A transfer has the following attributes:
        - A date of type Date
        - A value which is a nonnegative float
        - A note which is a string
        - An account_sending which is of type Account. This can also be set to None if the account sending the value is unknown.
        - An account_receiving which is of type Account. This can also be set to None if the account receiving is unkown
          We can't have both account_sending and account_receiving being None

        - recurrent defaults to None. This can be set to be a day number if this transfer occurs every month on that day


    Transfers are stored as follows:
    {"date_simple_string": {
        "month": month,
        "year": year,
        "value": value,
        "note": note
        }
    }

    If account_sending is not None, then we store it as "account_sending": account_sending_number

    If account_receiving is not None, then we store it as "account_receiving": account_receiving_number

    If recurrent is not None, then we store it as "recurrent": day.
    '''
    def __init__(self, date, value, note, account_sending=None, account_receiving=None):
        self.date = date 
        self.value = value 
        self.note = note 
        self.account_sending = account_sending 
        self.account_receiving = account_receiving
        



class RecurringTransaction:
    '''
    A recurring transaction is completely determined by its name

    The instantiation dates list keeps track of all the simple_dates that characterize transactions that were created from this recurring transaction
    
    The identifier is an int between 0 and 86400 (number of seconds in a day), and no two different recurring acts can have the same identifier
    '''
    def __init__(self, 
                 identifier: int,
                 name: str, 
                 start_date: Date, 
                 month_day: int, 
                 value: float, 
                 category, 
                 note: str, 
                 account,
                 end_date: Date = None, 
                 subcategory=None, 
                 old_category_name: str = None, 
                 old_subcategory_name: str = None,
                 instantiation_dates_list: list = []
    ):
        self.identifier = identifier
        self.name = name
        self.start_date = start_date
        self.month_day = month_day
        self.value = value
        self.category = category
        self.note = note
        self.account = account
        self.end_date = end_date
        self.subcategory = subcategory
        self.old_category_name = old_category_name
        self.old_subcategory_name = old_subcategory_name
        self.instantiation_dates_list = instantiation_dates_list


class RecurringTransfer:
    def __init__(self, 
                 identifier: int,
                 name: str, 
                 start_date: Date, 
                 month_day: int, 
                 value: float, 
                 note: str, 
                 end_date: Date = None, 
                 account_sending=None, 
                 account_receiving=None, 
                 instantiation_dates_list: list = []
    ):
        self.identifier = identifier
        self.name = name
        self.start_date = start_date
        self.month_day = month_day
        self.value = value
        self.note = note
        self.end_date = end_date
        self.account_sending = account_sending
        self.account_receiving = account_receiving
        self.instantiation_dates_list = instantiation_dates_list






        