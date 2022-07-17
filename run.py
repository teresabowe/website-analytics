import textwrap as tr
from tabulate import tabulate
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


def display_greeting():
    """
    Welcome message.
    """
    print(tr.fill(("Hello! This reporting application provides insights \
                    regarding your website performance."), width=80))
    print(tr.fill(("You will shortly be prompted to enter visits, pageviews, \
                    orders, and revenue for today."), width=80))
    print("")


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
        return 'For this period, the data are visits: ' \
            + str(self.visits) + ', pageviews: ' + str(self.pageviews)\
            + ', orders: ' + str(self.orders) + ', and revenue: ' \
            + str(self.revenue)+'.\n'

    def get_entered_as_list(self):
        """
        Return list.
        """
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
         + ' and a conversion rate of ' + str(self.conversion_rate) + '%.\n'

    def get_calculated_as_list(self):
        """
        Return list.
        """
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
              "The value you entered is outside the normal range"
              )
    except ValueError as e:
        print(f"Oops! {e}, please try again.\n")
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
    input("Press Enter to update the worksheet...\n")
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"The {worksheet} worksheet has been updated successfully.\n")


def delete_row(worksheet):
    """
    Delete row 1
    """
    print(f"Deleting {worksheet} row 1 to tidy up...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.delete_rows(2)
    print(f"The {worksheet} row 1 has been deleted successfully.\n")


def sum_column(nums, C):
    """
    Function to add specific column in list of lists
    """
    result = sum(row[C] for row in nums)
    return result


def gather_all_historical_data():
    """
    Gather all data from Google worksheet.
    Print data in tabular format.
    Convert the data to integers.
    Split the data between this week and this week.
    Sum the data for visits, pageviews, orders and revenue for the two weeks.
    Return the data to the TimePeriod class.
    """
    input("Press Enter to continue...\n")
    print("Reading all data from the worksheet...\n")
    all_data = SHEET.worksheet("dataset").get_all_values()
    print("*** Website Data - 14 Days ***\n")
    print("** The data entered today is at the bottom of the table **\n")
    print(tabulate(all_data, headers='firstrow'))
    all_data = [sublist[:4] for sublist in all_data]
    all_data.pop(0)
    all_data_int = [[int(float(item)) if item.isnumeric()
                    else item for item in sub_list] for sub_list in all_data]
    lastweek = all_data_int[:len(all_data_int)//2]
    thisweek = all_data_int[len(all_data_int)//2:]

    lastweek_visits = (sum_column(lastweek, 0))
    lastweek_pageviews = (sum_column(lastweek, 1))
    lastweek_orders = (sum_column(lastweek, 2))
    lastweek_revenue = (sum_column(lastweek, 3))
    thisweek_visits = (sum_column(thisweek, 0))
    thisweek_pageviews = (sum_column(thisweek, 1))
    thisweek_orders = (sum_column(thisweek, 2))
    thisweek_revenue = (sum_column(thisweek, 3))

    return (TimePeriod(lastweek_visits, lastweek_pageviews,
            lastweek_orders, lastweek_revenue),
            TimePeriod(thisweek_visits, thisweek_pageviews,
            thisweek_orders, thisweek_revenue))


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
    print("")
    input("Press Enter to continue with the analysis...\n")
    print("*** Data Analysis Report ***\n")
    print(tr.fill(("We aggregated data for this week. " +
          str(data[1]) + str(data[1].do_calculated_fields())), width=80))

    print(tr.fill(("We have also aggregated data for last week. ") +
          (str(data[0]) + str(data[0].do_calculated_fields())), width=80))

    input("Press Enter to continue with the analysis...\n")

    last_week = data[0].get_entered_as_list() + \
        data[0].do_calculated_fields().get_calculated_as_list()

    this_week = data[1].get_entered_as_list() + \
        data[1].do_calculated_fields().get_calculated_as_list()

    visits_change = calculate_percentage_change(this_week[0],
                                                last_week[0])

    pageviews_change = calculate_percentage_change(this_week[1],
                                                   last_week[1])

    pages_per_visit_change = this_week[4] - last_week[4]

    orders_change = calculate_percentage_change(this_week[2],
                                                last_week[2])

    conversion_rate_change = this_week[5] - last_week[5]

    revenue_change = calculate_percentage_change(this_week[3],
                                                 last_week[3])

    print("** Visits Analysis **\n")
    if round(visits_change, 2) > 0:
        print(tr.fill((f"Total visits for this week was {this_week[0]}, ") +
              (f"while last week the visits total was {last_week[0]}, ") +
              (f"an increase of {round(visits_change,2)}%.") +
              (" \u2191"), width=80))
    elif round(visits_change, 2) == 0:
        print(tr.fill((f"Total visits for this week was {this_week[0]}, ") +
              (f"while last week the visits total was {last_week[0]}, ") +
              ("on par with this week."), width=80))
    else:
        print(tr.fill((f"Total visits for this week was {this_week[0]}, ") +
              (f"while last week the visits total was {last_week[0]}, ") +
              (f"a reduction of {round(-visits_change,2)}%.") +
              (" \u2193"), width=80))

    input("Press Enter to continue...\n")

    print("** Pageviews and Pages Per Visit Analysis **\n")
    if round(pageviews_change, 2) > 0:
        print(tr.fill((f"Pageviews for this week was {this_week[1]}, ") +
              (f"while last week shows {last_week[1]}, ") +
              (f"an increase of {round(pageviews_change,2)}%.") +
              (" \u2191"), width=80))
    elif round(pageviews_change, 2) == 0:
        print(tr.fill((f"Pageviews for this week was {this_week[1]}, ") +
              (f"while last week shows {last_week[1]}. ") +
              ("This is on par with this week."), width=80))
    else:
        print(tr.fill((f"Pageviews for this week was {this_week[1]}, ") +
              (f"while last week shows {last_week[1]}, ") +
              (f"a reduction of {round(-pageviews_change,2)}%.") +
              (" \u2193"), width=80))

    if round(pages_per_visit_change, 2) > 0:
        print(tr.fill(("The overview of pages per visit for this week was ") +
              (f"{this_week[4]}, while last week it was ") +
              (f"{last_week[4]}, a positive difference of ") +
              (f"{round(pages_per_visit_change,2)}.") +
              (" \u2191"), width=80))
    elif round(pages_per_visit_change, 2) == 0:
        print(tr.fill(("The overview of pages per visit for this week was ") +
              (f"{this_week[4]}, and last week was the same at ") +
              (f"{last_week[4]}."), width=80))
    else:
        print(tr.fill(("The overview of pages per visit for this week was ") +
              (f"{this_week[4]}, while last week it was ") +
              (f"{last_week[4]}, a change of ") +
              (f"{round(-pages_per_visit_change,2)}. ") +
              ("The customer opened fewer pages per visit this week.") +
              (" \u2193"), width=80))

    input("Press Enter to continue...\n")

    print("** Orders and Conversion Rate Analysis **\n")
    if round(orders_change, 2) > 0:
        print(tr.fill((f"Total orders for this week were {this_week[2]}, ") +
              (f"while last week they were {last_week[2]}, ") +
              (f"a {round(orders_change,2)}% increase.") +
              (" \u2191"), width=80))
    elif round(orders_change, 2) == 0:
        print(tr.fill((f"Total orders for this week were {this_week[2]}, ") +
              (f"while last week they were {last_week[2]}, ") +
              ("on par with this week."), width=80))
    else:
        print(tr.fill((f"Total orders for this week were {this_week[2]}, ") +
              (f"while last week they were {last_week[2]}, ") +
              (f"a reduction of {round(-orders_change,2)}%.") +
              (" \u2193"), width=80))

    if round(conversion_rate_change, 2) > 0:
        print(tr.fill(("The overall conversion rate for this week was ") +
              (f"{this_week[5]}%, while last week was ") +
              (f"{last_week[5]}%, a positive difference of " +
              (f"{round(conversion_rate_change,2)}%.") +
              (" \u2191")), width=80))
    elif round(conversion_rate_change, 2) == 0:
        print(tr.fill(("The overall conversion rate for this week was ") +
              (f"{this_week[5]}%, and last week was the same at ") +
              (f"{last_week[5]}%."), width=80))
    else:
        print(tr.fill(("The overall conversion rate for this week was ") +
              (f"{this_week[5]}%, while last week it was ") +
              (f"{last_week[5]}%, a difference of ") +
              (f"{round(-conversion_rate_change,2)}%.") +
              (" \u2193"), width=80))

    input("Press Enter to continue...\n")

    print("** Revenue Analysis **\n")
    if round(revenue_change, 2) > 0:
        print(tr.fill((f"Total revenue for this week was {this_week[3]}, ") +
              (f"while last week they were {last_week[3]}, ") +
              (f"a {round(revenue_change,2)}% increase.") +
              (" \u2191"), width=80))
    elif round(revenue_change, 2) == 0:
        print(tr.fill((f"Total revenue for this week was {this_week[3]}, ") +
              (f"while last week they were {last_week[3]}, ") +
              ("on par with this week."), width=80))
    else:
        print(tr.fill((f"Total revenue for this week was {this_week[3]}, ") +
              (f"while last week they were {last_week[3]}, ") +
              (f"a reduction of {round(-revenue_change,2)}%.") +
              (" \u2193"), width=80))

    print("")
    print("* End of the report. Select RUN PROGRAM above to enter new data. *")


def main():
    """
    Run program functions
    """
    display_greeting()
    day_of_data = gather_data()
    print(tr.fill(str(day_of_data), width=80))
    print(tr.fill(str(day_of_data.do_calculated_fields()), width=80))
    list_for_sheet = day_of_data.get_entered_as_list() + day_of_data.\
        do_calculated_fields().get_calculated_as_list()
    update_worksheet(list_for_sheet, "dataset")
    delete_row("dataset")
    historical_data_all = gather_all_historical_data()
    generate_report(historical_data_all)


main()
