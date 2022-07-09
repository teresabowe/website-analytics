import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('website_data')

class TimePeriod:
    """
    Represent website analytics data for a time period.
    """
    def __init__(self, visits, pageviews, orders, revenue):
        self.visits = visits
        self.orders = orders
        self.pageviews = pageviews
        self.revenue = revenue

    def __str__(self):
         return 'For this time period, the data are visits: ' + str(self.visits) + ', pageviews: ' + str(self.pageviews) + ', orders: ' + str(self.orders) + ', and revenue: ' + str(self.revenue)+'.\n'
       
    def get_entered_as_list(self):
        return[self.visits, self.pageviews, self.orders, self.revenue]
  
    def do_calculated_fields(self):
        """
        Calculate pages per visits and conversion rate.
        """
        pages_per_visit = round(self.pageviews / self.visits, 2)
        conversion_rate = round(self.orders / self.visits * 100, 2)

        return Calculated(pages_per_visit, conversion_rate)

class Calculated:
    """
    Represent pages per visit and conversion rate.
    """
    def __init__(self, pages_per_visit, conversion_rate):
        self.pages_per_visit = pages_per_visit
        self.conversion_rate = conversion_rate
    
    def __str__(self):
         return 'We calculated pages per visit of ' + str(self.pages_per_visit)+ ', and a conversion rate of ' + str(self.conversion_rate) + '%.\n'

    def get_calculated_as_list(self):
        return[self.pages_per_visit, self.conversion_rate]
        
def get_data_item(type, lower, higher):
    """
    Get input from user for data.
    Call validate function to check data.
    """
    while True:
        print(f"The {type} data are usually between {lower} and {higher}.")
        input_data = input(f"Enter your {type} data here:\n")
        if validate_data(input_data, lower, higher):
            print("Data is valid!\n")
            break

    return(int(input_data))

def validate_data(values, lower, higher):
    """
    Inside try, converts values to integers.
    Raises ValueError if data is outside the range
    or cannot be interpreted.
    """
    try:
        if int(values) < lower or int(values) > higher:
            raise ValueError(
              "Value is outside the normal range"
              )
    except ValueError as e:
        print(f"Invalid data {e}:, please try again.\n")
        return False
        
    return True

def gather_data():
    """
    Assign variable to data collection function.
    """
    visits_data = get_data_item("visits", 500, 5000)
    pageviews_data = get_data_item("pageviews", 500, 30000)
    orders_data = get_data_item("orders", 0, 200)
    revenue_data = get_data_item("revenue", 0, 3000)

    return TimePeriod(visits_data, pageviews_data, orders_data, revenue_data)

def update_worksheet(data, worksheet):
    """
    Receives a list of values to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"The {worksheet} worksheet has been updated successfully.\n")

def get_historical_entries_dataset(param1, param2):
    """
    Collects columns of data from the dataset worksheet
    and returns the data as a list of lists.
    """
   
    seven_days = SHEET.worksheet("dataset")

    columns = []
    for ind in range(1, 5):
        column = seven_days.col_values(ind)
        columns.append(column[param1:param2])

    return columns

def gather_historical_data():
    """
    Assign variable to historical data collection function.
    """
    print(f"Reading historical data...\n")
    hist_data_14_days = get_historical_entries_dataset(-14, -7)
    hist_data_14_days = [[int(float(j)) for j in i] for i in hist_data_14_days]
    hist_data_14_days = [sum(sl) for sl in hist_data_14_days]
    visits_14, pageviews_14, orders_14, revenue_14 = [hist_data_14_days[i] for i in (0, 1, 2, 3)]
    hist_data_7_days = get_historical_entries_dataset(-7, None)
    hist_data_7_days = [[int(float(j)) for j in i] for i in hist_data_7_days]
    hist_data_7_days = [sum(sl) for sl in hist_data_7_days]
    visits_7, pageviews_7, orders_7, revenue_7 = [hist_data_7_days[i] for i in (0, 1, 2, 3)]

    return (TimePeriod(visits_14, pageviews_14, orders_14, revenue_14), TimePeriod(visits_7, pageviews_7, orders_7, revenue_7))

def main():
    """
    Run program functions
    """
    day_of_data = gather_data()
    print(str(day_of_data))
    print(str(day_of_data.do_calculated_fields()))
    list_entered = day_of_data.get_entered_as_list()
    list_calculated = day_of_data.do_calculated_fields().get_calculated_as_list()
    list_for_sheet = list_entered + list_calculated
    update_worksheet(list_for_sheet, "dataset")
    historical_data = gather_historical_data()
    data_14_days = historical_data[0].get_entered_as_list()
    data_14_days_calc = historical_data[0].do_calculated_fields().get_calculated_as_list()
    print(data_14_days)
    print(data_14_days_calc)
    data_7_days = historical_data[1].get_entered_as_list()
    data_7_days_calc = historical_data[1].do_calculated_fields().get_calculated_as_list()
    print(data_7_days)
    print(data_7_days_calc)

main()
