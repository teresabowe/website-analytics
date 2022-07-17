# Website Analytics

Website Analytics is a command-line application that manages data relating to an organization's website performance.  The user can interact with the application by entering the daily website data.  The application processes the entered and historical data and provides the user with insights relating to website performance.

You can use the live application [here](https://website-analytics-reporting.herokuapp.com/).

## User Experience

### User Stories

As a user I would like to be able to:

- Enter new data for visits, page views, orders, and revenue.
- Have the application give me feedback when I enter incorrect data.
- Update a data repository with the entered data.
- Delete old data.
- View the most up-to-date data in the repository.
- Calculate pages per visit and conversion rate.
- Run historical reporting showing week-on-week comparisons.

## Features

### Existing Features

When the website analytics application launches, the user is presented with a terminal window.  The text explains the purpose of the application and a brief description of what the user needs to do next.

![Start](/docs/start.png)

First, the user must enter data.  The application raises a ValueError if the number entered is outside the thresholds recommended or an integer has not been input.

![Value Error](/docs/value-error.png)

If the user enters zero orders, the application expects zero revenue. 

![Orders Zero](/docs/orders-zero.png)

If the user enters one or more orders, the application expects a non-zero value for revenue.

![Orders not Zero](/docs/orders-zero.png)

The user receives feedback regarding the new calculated fields of pages per visit and conversion rate.

![Calculated Fields](/docs/calculated-fields.png)

The worksheet is updated, and the user receives feedback to say the update has been successful.

![Update Worksheet](/docs/update-worksheet.png)

A table of 14 days of data is presented to the user.  It includes the most recent data entered in the current session.

![Table](/docs/create-table.png)

Finally, the report with commentary is created.  Also, the user sees that the ‘run program’ button is available to enter new data.

![Report](/docs/data-analysis-report.png)
![Run Program](/docs/run-program.png)
![End of Report](/docs/end-of-report.png)

### Future Features

## Design

### Technologies Used

## Testing

### Manual Testing


### Features Testing

### Validator Testing

The Python code was checked using the PEP8 online tool.  The main errors included white space and the line lengths over 79 columns.  There are currently no errors showing in the application. 

![Pep8 Validator Test](/docs/pep8-result.png)

### Bugs and Fixes

_Text Wrapping and Filling_

Because the application is a reporting application, there are several long lines of text, including literal strings and many with concatenation.  The Python terminal is 80 columns wide in Heroku.  When the application was deployed, the text wrapped onto the following line and split the words.  

Initially, I thought the best solution would be to widen the terminal to 120 columns.  While this change did improve the overall presentation of the reporting, I felt that a terminal-based application should be 80 columns wide.  The solution was to import the textwrap library and use it, along with the fill function, to fix the word splitting issue.

_Performance Improvement_

Initially, the application made two remote procedure calls to the Google worksheet.  Once, to read the data for the current week and then again for last week.  As I had applied data cleaning on the worksheet and also needed to import the headers for presenting the table, I decided to implement one remote procedure call to gather all the data.  There was now a possibility that this change might deliver a performance improvement, so I placed a timer on the two functions and verified that the two functions were gathering the same data.  

The new function is consistently up to 3 seconds faster than the old one.  The image below shows a copy of the output from the code with the performance counters applied to both functions.

![PerformanceCounter](/docs/function-performance-counter.png)

_Testing on Devices_



## Deployment

## Credits

### Code

- Converting a list of lists to an integer [Stack Overflow](https://stackoverflow.com/questions/42376696/converting-specific-elements-in-a-list-of-lists-from-a-string-to-an-integer).

- How to print a table in Python from [Towards Data Science](https://towardsdatascience.com/how-to-easily-create-tables-in-python-2eaea447d8fd).

- How to add a Unicode string for arrows from [Stack Overflow](https://stackoverflow.com/questions/37130884/how-to-display-the-arrow-symbol-in-python-tkmessagebox).

- How to split a list in half from [Stack Overflow](https://stackoverflow.com/questions/752308/split-list-into-smaller-lists-split-in-half). 

- Add column to a list of lists from [w3Resource](https://www.w3resource.com/python-exercises/list/python-data-type-list-exercise-142.php).

- Wrapping text to 80 columns using textwrap and fill from [Towards Data Science](https://towardsdatascience.com/6-fancy-built-in-text-wrapping-techniques-in-python-a78cc57c2566).


### Content




