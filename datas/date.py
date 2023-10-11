

class Date:
    '''
    date_string has the format: "yyyy-mm-dd hh:mm:ss.mmmmmm"

    A Date object has the following attributes (all strings):
        - year
        - month
        - day
        - hour
        - minutes
        - seconds (format is "ss") (this is rounded down from ss.mmmmmm)
        

    Dates are stored in memory in the format of date_string
    
    '''
    def __init__(self, date_string):
        self.date_string = date_string 


        # get the year, month, day, hour, second, milisecond from date_string and create an attribute

        year = date_string[:4]
        self.year = year

        month = date_string[5:7]
        self.month = month

        day = date_string[8:10]
        self.day = day

        hour = date_string[11: 13]
        self.hour = hour

        minutes = date_string[14: 16]
        self.minutes = minutes

        seconds = date_string[17:19]
        self.seconds = seconds

       
    def parse_string(self, simple_date_string):
        '''
        simple_date_string has the format "dd/mm/yyyy hh:mm:ss"

        this function takes a simple_date_string, converts it into a date_string format and returns a Date object with the passed date_string
        '''
        
        days = simple_date_string[:2]
        month = simple_date_string[3:5]
        year = simple_date_string[6:10]
        hour = simple_date_string[11:13]
        minutes = simple_date_string[14:16]
        seconds = simple_date_string[17:]

        date_string = f"{year}-{month}-{days} {hour}:{minutes}:{seconds}.000000"

        new_date = Date(date_string)

        return new_date


    def get_date_simple_string(self):
        simple_string = f"{self.day}/{self.month}/{self.year} {self.hour}:{self.minutes}:{self.seconds}"
        return simple_string
    



def get_date_from_simple_date(simple_date_string):
    '''
    simple_date_string has the format "dd/mm/yyyy hh:mm:ss"

    this function takes a simple_date_string, converts it into a date_string format and returns a Date object with the passed date_string
    '''
    
    days = simple_date_string[:2]
    month = simple_date_string[3:5]
    year = simple_date_string[6:10]
    hour = simple_date_string[11:13]
    minutes = simple_date_string[14:16]
    seconds = simple_date_string[17:]

    date_string = f"{year}-{month}-{days} {hour}:{minutes}:{seconds}.000000"

    new_date = Date(date_string)

    return new_date



def month_year_to_simple_date(month_day, month_year):
    '''
    takes a month_day int and a month_year = (month_int, year_int) and converts it to the simple date "dd/mm/yyyy 00:00:00"
    '''

    day_str = str(month_day)
    month_str = str(month_year[0])
    year_str = str(month_year[1])

    if len(day_str) < 2:
        day_str = f"0{day_str}"

    if len(month_str) == 1:
        month_str = f"0{month_str}"

    if len(year_str) == 1:
        year_str = f"000{year_str}"
    elif len(year_str) == 2:
        year_str = f"00{year_str}"
    elif len(year_str) == 3:
        year_str = f"0{year_str}"
    
    return f"{day_str}/{month_str}/{year_str} 00:00:00"



def last_day(month_year):
    '''
    Given a month_year = (month_int, year_int) returns the last day int of that month
    
    Eg last_day((12, 2023)) == 31 
        last_day((2, 2020)) == 29
    '''
    reference = {
        1: 31,
        2: 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31
    }

    if is_leap_year(month_year[1]) and month_year[0] == 2:
        return 29
    
    return reference[month_year[0]]





def is_leap_year(year):
    #year is a natural number (incl zero)
        if year % 4 == 0:
            if year % 100 == 0:
                if year % 400 == 0:
                    return True
                return False
            return True
        return False



def compare_dates(date_simple_string1, date_simple_string2):
        '''
        date_simple_string should have the format "dd/mm/yyyy hh:mm:ss"

        returns true if date1 is smaller or equal to date2 (meaning date1 occured before date2)
        '''
        year1 = int(date_simple_string1[6:10])
        year2 = int(date_simple_string2[6:10])

        month1 = int(date_simple_string1[3:5])
        month2 = int(date_simple_string2[3:5])

        day1 = int(date_simple_string1[:2])
        day2 = int(date_simple_string2[:2])

        hour1 = int(date_simple_string1[11:13])
        hour2 = int(date_simple_string2[11:13])

        minutes1 = int(date_simple_string1[14:16])
        minutes2 = int(date_simple_string2[14:16])

        seconds1 = int(date_simple_string1[17:])
        seconds2 = int(date_simple_string2[17:])

        if year1 > year2:
            return False
        if year1 < year2:
            return True

        if month1 > month2:
            return False
        if month1 < month2:
            return True
        
        if day1 > day2:
            return False
        if day1 < day2:
            return True
        
        if hour1 > hour2:
            return False
        if hour1 < hour2:
            return True
        
        if minutes1 > minutes2:
            return False
        if minutes1 < minutes2:
            return True
        
        if seconds1 > seconds2:
            return False
        return True



def date_is_in_interval(simple_date, start_simple_date, end_simple_date):
        '''
        the dates have the form "dd/mm/yyyy". The end_simple_date can be None. In that case the function returns
        whether or not the simple_date is at or after the start_simple_date
        '''

       
        year = int(simple_date[6:])
        year1 = int(start_simple_date[6:])

        month = int(simple_date[3:5])
        month1 = int(start_simple_date[3:5])

        day = int(simple_date[:2])
        day1 = int(start_simple_date[:2])
        

        if end_simple_date == None:
            if year < year1:
                 return False
            if year > year1:
                 return True
            
            if month < month1:
                 return False
            if month > month1:
                 return True
            
            if day < day1:
                 return False
            return True
            
        year2 = int(end_simple_date[6:])
        if not year1 <= year <= year2:
             return False
        
        month2 = int(end_simple_date[3:5])
        if (year == year1 and month < month1) or (year == year2 and month > month2):
             return False
        
        day2 = int(end_simple_date[:2])
        if (year == year1 and month == month1 and day < day1) or (year == year2 and month == month2 and day > day2):
             return False
        
        return True



def absolute_date(simple_date_string):
        ''' 
        returns the amount of time in seconds from january first of the year zero to the given date

        the simle_date_string must have the form "dd/mm/yyyy hh:mm:ss"

        '''
        calendar = {1 : 31, 2 : 28, 3 : 31, 4 : 30, 5 : 31,
            6 : 30, 7 : 31, 8 : 31, 9 : 30, 10 : 31,
            11 : 30, 12 : 31}
        
        leap_calendar = {1 : 31, 2 : 29, 3 : 31, 4 : 30, 5 : 31,
            6 : 30, 7 : 31, 8 : 31, 9 : 30, 10 : 31,
            11 : 30, 12 : 31}
        
        year = int(simple_date_string[6: 10])
        month = int(simple_date_string[3:5])
        day = int(simple_date_string[:2])
        hour = int(simple_date_string[11:13])
        minutes = int(simple_date_string[14:16])
        seconds = int(simple_date_string[17:])

        total_days = 0

        for num in range(year):
            total_days += 365 + int(is_leap_year(num))

        for mon in range(1, month):
            if not is_leap_year(year):
                total_days += calendar[mon]
            else:
                total_days += leap_calendar[mon] 
        total_days += day
        return total_days * 86400 + hour*3600 + minutes*60 + seconds






    


if __name__ == "__main__":

    # date = get_date_from_simple_date(month_year_to_simple_date(1, (9, 2023)))

    # print(date.day, date.month, date.year, date.hour, date.minutes, date.seconds)



    print(date_is_in_interval("11/08/2022", "10/08/2022", None))