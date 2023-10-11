

class Account:
    '''
    An account has a balance with the total amount of money deposited and has a name. 
    Transactions add or subtract from the balance of an account.

    The account balance is automatically rounded to 2 decimal digits.

    An account also has a number. An account is completely characterized by its number. This means that there can be
    different accounts with the same name or with the same balance, but not with the same number. 

    Account numbers are useful for sorting accounts in order of importance.

    current specifies if this account is to be considered the current account. This attribute defaults to False
    '''

    def __init__(self, name: str, balance: float, number: int, current=False):
        self.name = name
        self.balance = balance
        self.number = number
        self.current = current