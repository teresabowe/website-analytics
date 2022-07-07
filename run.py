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

    def get_calculated_as_list(self):
        return[self.pages_per_visit, self.conversion_rate]
        
def get_data_item(type, lower, higher):
    """
    Get input from user for data.
    Call validate function to check data.
    """
    while True:
        input_data = input(f"Enter your {type} data here:\n")
        if validate_data(input_data, lower, higher):
            print("Data is valid!")
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
    print(f"{worksheet} worksheet updated successfully\n")


day_of_data = gather_data()
list_entered = day_of_data.get_entered_as_list()
list_calculated = day_of_data.do_calculated_fields().get_calculated_as_list()
list_for_sheet = list_entered + list_calculated
print(list_for_sheet)
update_worksheet(list_for_sheet, "dataset")

