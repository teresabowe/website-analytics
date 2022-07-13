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
        return 'For this time period, the data are visits: ' \
            + str(self.visits) + ', pageviews: ' + str(self.pageviews)\
            + ', orders: ' + str(self.orders) + ', and revenue: ' \
            + str(self.revenue)+'.\n'

    def get_entered_as_list(self):
        return[self.visits, self.pageviews, self.orders, self.revenue]

    def do_calculated_fields(self):
        """
        Calculate pages per visits and conversion rate.
        """
        pages_per_visit = round(self.pageviews / self.visits, 2)
        conversion_rate = round((self.orders / self.visits) * 100, 2)

        return Calculated(pages_per_visit, conversion_rate)


class Calculated:
    """
    Represent pages per visit and conversion rate.
    """
    def __init__(self, pages_per_visit, conversion_rate):
        self.pages_per_visit = pages_per_visit
        self.conversion_rate = conversion_rate

    def __str__(self):
        return 'We calculated pages per visit of ' + str(self.pages_per_visit)\
         + ', and a conversion rate of ' + str(self.conversion_rate) + '%.\n'

    def get_calculated_as_list(self):
        return [self.pages_per_visit, self.conversion_rate]


def get_data_item(data_type, lower, higher):
    """
    Get input from user for data.
    Call validate function to check data.
    """
    while True:
        print(f"The {data_type} data can be between {lower} and {higher}.")
        input_data = input(f"Enter your {data_type} data here:\n")
        if validate_data(input_data, lower, higher):
            print("Data is valid!\n")
            break

    return int(input_data)


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
    if orders_data == 0:
        revenue_data = get_data_item("revenue", 0, 0)
    else:
        revenue_data = get_data_item("revenue", 1, 10000)

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


def delete_row(worksheet):
    """
    Delete row 1
    """
    print(f"Deleting {worksheet} row 1...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.delete_rows(2)
    print(f"The {worksheet} row 1 has been deleted successfully.\n")


def get_historical_entries_dataset(cols, days1, days2):
    """
    Collects columns of data from the dataset worksheet
    and returns the data as a list of lists.
    """
    seven_days = SHEET.worksheet("dataset")

    columns = []
    for ind in range(1, cols):
        column = seven_days.col_values(ind)
        columns.append(column[days1:days2])

    return columns


def gather_historical_data():
    """
    Assign variable to historical data collection function.
    """
    print("Reading historical data...\n")

    hist_14_days = get_historical_entries_dataset(5, -14, -7)
    print(hist_14_days)
    print(min(hist_14_days[2]))
    input("Press Enter to continue...")
    hist_14_days = [[int(float(j)) for j in i] for i in hist_14_days]
    hist_14_days = [sum(sl) for sl in hist_14_days]
    visits_14, pageviews_14, orders_14, revenue_14 = [hist_14_days[i] for i in
                                                      (0, 1, 2, 3)]

    hist_7_days = get_historical_entries_dataset(5, -7, None)
    print(hist_7_days)
    print(min(hist_7_days[2]))
    input("Press Enter to continue...")
    hist_7_days = [[int(float(j)) for j in i] for i in hist_7_days]
    hist_7_days = [sum(sl) for sl in hist_7_days]
    visits_7, pageviews_7, orders_7, revenue_7 = [hist_7_days[i] for i in
                                                  (0, 1, 2, 3)]

    return (TimePeriod(visits_14, pageviews_14, orders_14, revenue_14),
            TimePeriod(visits_7, pageviews_7, orders_7, revenue_7))


def calculate_percentage_change(last, previous):
    """
    Calculate the percentage change
    """
    percentage_change = (((last-previous)/previous)*100)

    return percentage_change


def generate_report(data):
    """
    Report generator for website analytics.
    """
    print("*** Data Analysis Report ***\n")
    print(("We have aggregated data for the previous 8 to 14 days. ") +
          (str(data[0]) + str(data[0].do_calculated_fields())))
    print(("We also aggregated data for the previous 1 to 7 days. " +
          str(data[1]) + str(data[1].do_calculated_fields())))

    input("Press Enter to continue...")

    data_14_days = data[0].get_entered_as_list() + \
        data[0].do_calculated_fields().get_calculated_as_list()

    data_7_days = data[1].get_entered_as_list() + \
        data[1].do_calculated_fields().get_calculated_as_list()

    visits_change = calculate_percentage_change(data_7_days[0],
                                                data_14_days[0])

    pageviews_change = calculate_percentage_change(data_7_days[1],
                                                   data_14_days[1])

    pages_per_visit_change = data_7_days[4] - data_14_days[4]

    orders_change = calculate_percentage_change(data_7_days[2],
                                                data_14_days[2])

    conversion_rate_change = data_7_days[5] - data_14_days[5]

    revenue_change = calculate_percentage_change(data_7_days[3],
                                                 data_14_days[3])

    print()
    print("** Visits Analysis**\n")
    if round(visits_change, 2) > 0:
        print((f"Total visits for last week was {data_7_days[0]}, ") +
              (f"while the previous week was {data_14_days[0]}, ") +
              (f"a {round(visits_change,2)}% increase.\n"))
    elif round(visits_change, 2) == 0:
        print((f"Total visits for last week was {data_7_days[0]}, ") +
              (f"while the previous week was {data_14_days[0]}, ") +
              ("on par with last week.\n"))
    else:
        print((f"Total visits for last week was {data_7_days[0]}, ") +
              (f"while the previous week was {data_14_days[0]}, ") +
              (f"a reduction of {round(visits_change,2)}%.\n"))

    input("Press Enter to continue...")

    print("** Pageviews and Pages Per Visit Analysis**\n")
    if round(pageviews_change, 2) > 0:
        print((f"Customer pageviews for last week was {data_7_days[1]}, ") +
              (f"while the previous week shows {data_14_days[1]}, ") +
              (f"a {round(pageviews_change,2)}% increase.\n"))
    elif round(pageviews_change, 2) == 0:
        print((f"Customer pageviews for last week was {data_7_days[1]}, ") +
              (f"while the previous week shows {data_14_days[1]}, ") +
              ("on par with last week.\n"))
    else:
        print((f"Customer pageviews for last week was {data_7_days[1]}, ") +
              (f"while the previous week shows {data_14_days[1]}, ") +
              (f"a reduction of {round(pageviews_change,2)}%.\n"))

    if round(pages_per_visit_change, 2) > 0:
        print(("The weekly overview of pages per visit for last week was ") +
              (f"{data_7_days[4]}, while the previous week it was ") +
              (f"{data_14_days[4]}, a positive difference of ") +
              (f"{round(pages_per_visit_change,2)}.\n"))
    elif round(pages_per_visit_change, 2) == 0:
        print(("The weekly overview of pages per visit for last week was ") +
              (f"{data_7_days[4]}, and the previous week was the same at ") +
              (f"{data_14_days[4]}.\n"))
    else:
        print(("The weekly overview of pages per visit for last week was ") +
              (f"{data_7_days[4]}, while the previous week was ") +
              (f"{data_14_days[4]} a change of ") +
              (f"{round(pages_per_visit_change,2)}. ") +
              ("The customer opened less pages per visit last week.\n"))

    input("Press Enter to continue...")

    print("** Orders and Conversion Rate Analysis**\n")
    if round(orders_change, 2) > 0:
        print((f"Total orders for last week was {data_7_days[2]}, ") +
              (f"while the previous week was {data_14_days[2]}, ") +
              (f"a {round(orders_change,2)}% increase.\n"))
    elif round(orders_change, 2) == 0:
        print((f"Total orders for last week was {data_7_days[2]}, ") +
              (f"the previous week was {data_14_days[2]}, ") +
              ("on par with last week.\n"))
    else:
        print((f"Total orders for last week was {data_7_days[2]}, ") +
              (f"while the previous week they were {data_14_days[2]}, ") +
              (f"a reduction of {round(orders_change,2)}%.\n"))

    if round(conversion_rate_change, 2) > 0:
        print(("The weekly overview of conversion rate for last week was ") +
              (f"{data_7_days[5]}%, while the previous week was ") +
              (f"{data_14_days[5]}%, a positive difference of " +
              (f"{round(conversion_rate_change,2)}%.\n")))
    elif round(conversion_rate_change, 2) == 0:
        print(("The weekly overview of conversion rate for last week was ") +
              (f"{data_7_days[5]}%, and the previous week was the same at ") +
              (f"{data_14_days[5]}%.\n"))
    else:
        print(("The weekly overview of conversion rate for last week was ") +
              (f"{data_7_days[5]}%, while the previous week was ") +
              (f"{data_14_days[5]}%, a difference of ") +
              (f"{round(conversion_rate_change,2)}%.\n"))

    input("Press Enter to continue...")

    print("** Revenue Analysis**\n")
    if round(revenue_change, 2) > 0:
        print((f"Total revenue for last week was {data_7_days[3]}, ") +
              (f"while the previous week it was {data_14_days[3]}, ") +
              (f"a {round(revenue_change,2)}% increase.\n"))
    elif round(revenue_change, 2) == 0:
        print((f"Total revenue for last week was {data_7_days[3]}, ") +
              (f"while the previous week it was {data_14_days[3]}, ") +
              ("on par with last week.\n"))
    else:
        print((f"Total revenue for last week was {data_7_days[3]}, ") +
              (f"while the previous week it was {data_14_days[3]}, ") +
              (f"a reduction of {round(revenue_change,2)}%.\n"))


def main():
    """
    Run program functions
    """
    day_of_data = gather_data()
    print(str(day_of_data))
    print(str(day_of_data.do_calculated_fields()))
    input("Press Enter to continue...")
    list_for_sheet = day_of_data.get_entered_as_list() + day_of_data.\
        do_calculated_fields().get_calculated_as_list()
    update_worksheet(list_for_sheet, "dataset")
    delete_row("dataset")
    historical_data = gather_historical_data()
    generate_report(historical_data)


main()
