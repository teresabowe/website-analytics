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
        
def get_data_item(type):
    """
    Get input from user for data.
    """
    input_data = input(f"Enter your {type} data here:\n")
    return(int(input_data))

def gather_data():
    """
    Assign variable to data collection function.
    """
    visits_data = get_data_item("visits")
    pageviews_data = get_data_item("pageviews")
    orders_data = get_data_item("orders")
    revenue_data = get_data_item("revenue")

    return TimePeriod(visits_data, pageviews_data, orders_data, revenue_data)

day_of_data = gather_data()
list_entered = day_of_data.get_entered_as_list()
list_calculated = day_of_data.do_calculated_fields().get_calculated_as_list()
print(list_entered)
print(list_calculated)

