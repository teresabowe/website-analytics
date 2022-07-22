# Website Analytics

Website Analytics is a command-line application that manages data relating to an organization's website performance.  The user can interact with the application by entering the daily website data.  The application processes the entered and historical data and provides the user with insights relating to website performance.

You can use the live application [here](https://website-analytics-reporting.herokuapp.com/).

## User Experience

### User Stories

As a user I would like to be able to:

- Enter new data for visits, page views, orders, and revenue.
- Have the application give me feedback when I enter incorrect data.
- Update a data repository with the entered data.
- Delete old data from the repository.
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

![Orders not Zero](/docs/orders-not-zero.png)

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

The idea for the application stems from a desire to introduce automation into data analytics reporting tasks repeated at regular intervals.  While the calculations for pages per visit and conversion rates are present, I feel that many other features could be added.  These could include but are not limited to the following:

- Increasing the number of data fields analysed.  For example, cart abandonment data.

- Replace the manual entry of visits, pageviews, etc., with an API to load the daily data automatically.

- Prepare an automated daily email commentary for a wider audience.

- Change the style and layout of the commentary text regularly.

## Design

<details>
  <summary>Flow Chart</summary>
  
  ![Flow Chart](/docs/flow-diagram-analytics.png)
</details>

## Technologies Used

### Languages

- Python 3.8.11

### Frameworks, Libraries and Programs

- [Google Sheets](https://www.google.com/sheets/about/): The external data store for this project is Google Sheets, an online spreadsheet editor.

- [Google Sheets API](https://developers.google.com/sheets/api): This API facilitates read, write, and formatting functionality between Python and Google Sheets.

- [Google Drive API](https://developers.google.com/drive/api): The Drive API is used to interact with Google Drive storage.

- [Python gspread API](https://docs.gspread.org/en/latest/): Python API for Google Sheets.

- [Python google-auth Library](https://pypi.org/project/google-auth/): The Google auth library for Python enables the interaction between Python and Google Sheets.

- [Python time Library](https://docs.python.org/3/library/time.html): The time library was used to temporarily measure how long it took to run functions.

- [Python tabulate Library](https://pypi.org/project/tabulate/): The tabulate library was used to present a table of historical data in the Python terminal.

- [Python textwrap Library](https://docs.python.org/3/library/textwrap.html): The textwrap library was used along with Python fill to wrap long sentences.

- [Git](https://github.com/git/git): Git was used when implementing version control for the application.

- [Github](https://github.com/): Github was used to host and manage the application repository up to the time of deployment.

- [Heroku](https://www.heroku.com/): The final version of the application was deployed on the Heroku platform. 


## Testing

Application features were manually tested from the command line in the terminal window during the development phase.

### Features Testing

<details>
  <summary>Test results.</summary>

| Given                                    | When                | Then                       | Outcome      |
| :---                                     |   :---              |   :---                     |  :---        |
| Application is deployed                  |  3500 entered       |  Moves to next input       | As expected  |
| Authentication to Google is complete     |                     |                            |              |
| Application is running                   |                     |                            |              |
| Enter visits                             |  35000 entered      |  Custom Error              | As expected  |
|                                          |                     |  The value you entered     |              |
|                                          |                     |  is outside the normal     |              |
|                                          |                     |  range, please try again.  |              |
|                                          |  3,500 entered      |  ValueError                | As expected  |
|                                          |                     |  invalid literal for       |              |
|                                          |                     |  int() with base 10:       |              |
|                                          |                     |  '3,500', please try       |              |
|                                          |                     |  again                     |              |
|                                          |  3500.00 entered    |  ValueError                | As expected  |
|                                          |                     |  invalid literal for       |              |
|                                          |                     |  int() with base 10:       |              |
|                                          |                     |  '3500.00', please try     |              |
|                                          |                     |  again                     |              |
|                                          |                     |                            |              |
| Application is deployed                  |  4500 entered       |  Moves to next input       | As expected  |
| Authentication to Google is complete     |                     |                            |              |
| Application is running                   |                     |                            |              |
| Visits input successful                  |  45000 entered      |  Custom Error              | As expected  |
| Enter pageviews                          |                     |  The value you entered     |              |
|                                          |                     |  is outside the normal     |              |
|                                          |                     |  range, please try again.  |              |
|                                          |  4,500 entered      |  ValueError                | As expected  |
|                                          |                     |  invalid literal for       |              |
|                                          |                     |  int() with base 10:       |              |
|                                          |                     |  '4,500', please try       |              |
|                                          |                     |  again                     |              |
|                                          |  4500.00 entered    |  ValueError                | As expected  |
|                                          |                     |  invalid literal for       |              |
|                                          |                     |  int() with base 10:       |              |
|                                          |                     |  '4500.00', please try     |              |
|                                          |                     |  again                     |              |
| Application is deployed                  |  150  entered       |  Moves to next input       | As expected  |
| Authentication to Google is complete     |                     |                            |              |
| Application is running                   |                     |                            |              |
| Visits input successful                  |  1500 entered       |  Custom Error              | As expected  |
| Pageviews input successful               |                     |  The value you entered     |              |
| Enter orders                             |                     |  is outside the normal     |              |
|                                          |                     |  range, please try again.  |              |
|                                          |  1,500 entered      |  ValueError                | As expected  |
|                                          |                     |  invalid literal for       |              |
|                                          |                     |  int() with base 10:       |              |
|                                          |                     |  '1,500', please try       |              |
|                                          |                     |  again                     |              |
|                                          |  4500.00 entered    |  ValueError                | As expected  |
|                                          |                     |  invalid literal for       |              |
|                                          |                     |  int() with base 10:       |              |
|                                          |                     |  '4500.00', please try     |              |
|                                          |                     |  again                     |              |
|                                          |                     |                            |              |
|                                          |  0 entered          |  Moves to next input       | As expected  |
| Application is deployed                  |  9000 entered       |  Moves to next input       | As expected  |
| Authentication to Google is complete     |                     |                            |              |
| Application is running                   |                     |                            |              |
| Visits input successful                  |  0 entered          |  Custom Error              | As expected  |
| Pageviews input successful               |                     |  The value you entered     |              |
| Orders input 1-200                       |                     |  is outside the normal     |              |
| Enter revenue                            |                     |  range, please try again.  |              |
|                                          |                     |  The revenue data can be   |              | 
|                                          |                     |  between 1 and 10000.      |              |
|                                          |  1500.00 entered    |  Value Error               | As expected  |
|                                          |                     |  invalid literal for       |              |
|                                          |                     |  int() with base 10:       |              |
|                                          |                     |  '1500.00', please try     |              |
|                                          |                     |  again.                    |              |
|                                          |  15000 entered      |  Custom Error              | As expected  |
|                                          |                     |  The value you entered     |              |
|                                          |                     |  is outside the normal     |              |
|                                          |                     |  range, please try again.  |              |
|                                          |                     |  The revenue data can be   |              | 
|                                          |                     |  between 1 and 10000.      |              |
| Application is deployed                  |  0 entered          |  Moves to next input       | As expected  |
| Authentication to Google is complete     |                     |                            |              |
| Application is running                   |                     |                            |              |
| Visits input successful                  |  9000 entered       |  Custom Error              | As expected  |
| Pageviews input successful               |                     |  The value you entered     |              |
| Orders input 0                           |                     |  is outside the normal     |              |
| Enter revenue                            |                     |  range, please try again.  |              |
|                                          |                     |  The revenue data can be   |              | 
|                                          |                     |  between 0 and 0.          |              |
|                                          |  9000.00 entered    |  Value Error               | As expected  |
|                                          |                     |  invalid literal for       |              |
|                                          |                     |  int() with base 10:       |              |
|                                          |                     |  '9000.00', please try     |              |
|                                          |                     |  again.                    |              |
|                                          |                     |  The revenue data can be   |              | 
|                                          |                     |  between 0 and 0.          |              |
| Message is "Press Enter to continue..."  |  Enter entered      |  Program continues         | As expected  |
|                                          |  Any other key is   |  The program waits for the | As expected  |
|                                          |  entered            |  Enter key to be pressed   |              |

</details>

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

_Testing on Mobile Devices_

This application was not tested on mobile devices.

## Deployment

<details>
  <summary>Clone the repository</summary>

- Go to https://github.com/teresabowe/website-analytics.
- Click on the 'code' button and copy the URL with the HTTPS option underlined.
- Open Git Bash.
- Type 'git clone' along with the copied URL in the directory where the clone is to be stored.
- Press Enter.

</details>


<details>
  <summary>Create the Google Sheet</summary>

- From a Google user account, go to Google Sheets.
- Click on the + (plus) on the bottom right-hand corner.
- Rename the worksheet to 'dataset'.
- Add six columns, visits, pageviews, orders, revenue, pages per visit, and conversion rate.
- Enter 14 lines of data similar to that shown in the table of the 'existing features' section of this document.

</details>

<details>
  <summary>Setup the Google Drive API</summary>

- From the Google Cloud Platform, go to the Manage Resource Page (https://console.cloud.google.com/cloud-resource-manager?_ga=2.95512412.1123028329.1658133535-1458248895.1656531052)
- Enter the project name and click Create
- Then select the project to open the Dashboard.
- Click on the APIs and Services tab on the left side and Enable APIs and Services.
- Type in 'Google Drive API' into the search bar
- Select the Google Drive API and click on 'enable'.
- Click on 'create credentials' on the top right side.
- The Google Drive API should be pre-selected.
- Click on the 'Application Data' radio button.
- For 'Applications running on GCE, GKE, GAE, and GCF', select 'No, I'm not using them'.
- Click 'next'.
- Enter a 'Service Account Name' and 'Create and Continue'.
- Select the role 'Basic' and 'Editor' for the service account
- Click 'Continue'.
- Select 'Done' in the 'Grant users access to this service account' section.
- Find the Service Accounts section and click on the name of the service account just created.
- Click on the 'KEYS' tab and 'ADD KEY'.
- Select 'JSON' and 'Create'.
- The new key is copied to the local computer.
- Rename this file to creds.json.
- Copy the creds.json to the local clone.
- Open the creds.json file and copy the client-email address.
- Go back to the worksheet created on Google Drive and click 'Share' on the top right-hand corner.
- Paste the email address and ensure that the 'Editor' permission is selected.

</details>

<details>
  <summary>Enable Google Sheets API</summary>

- From the project dashboard, choose 'Library'.
- Enter 'Google Sheets API' in the search bar.
- Click on the Google Sheets API and then 'Enable'.

</details>

<details>
  <summary>Install the gspread library in Python</summary>

- Enter 'pip3 install gspread google-auth' in the terminal window.

</details>

<details>
  <summary>Deploy the application to Heroku</summary>

- In advance of the deployment enter 'pip3 freeze > requirements.txt' in the terminal window. This command creates a list of items to be installed by pip.
- Login to Heroku or create a new account.
- Select 'New' in the top right-hand corner and then 'create new app'.
- Enter the name of the app and select the region.
- Click on the Settings tab and 'Reveal Config Vars'.
- Enter 'CREDS' into the key section.
- Enter the contents of the creds.json file into the value section.
- Click on Add.
- Enter 'PORT' into the key section.
- Enter '8000' into the value section.
- Click on Add.
- Go to the Buildpacks section and click on 'Add buildpack'.
- Select Python and 'save changes'.
- Click on 'Add buildpack' again.
- Select node.js.
- Make sure that the Python buildpack is on top.
- Select the Deploy tab and select Github as the deployment method.
- Authorise the connection and enter the name of the repository e.g. website-analytics.
- Enter the name of the repository.  
- Choose between Automatic and Manual deploy options. 
- The application can be opened from the configuration page by clicking on the 'Open App' button on the top right.

</details>

## Credits

### Code

- Converting a list of lists to an integer [Stack Overflow](https://stackoverflow.com/questions/42376696/converting-specific-elements-in-a-list-of-lists-from-a-string-to-an-integer).

- How to print a table in Python from [Towards Data Science](https://towardsdatascience.com/how-to-easily-create-tables-in-python-2eaea447d8fd).

- How to add a Unicode string for arrows from [Stack Overflow](https://stackoverflow.com/questions/37130884/how-to-display-the-arrow-symbol-in-python-tkmessagebox).

- How to split a list in half from [Stack Overflow](https://stackoverflow.com/questions/752308/split-list-into-smaller-lists-split-in-half). 

- Add column to a list of lists from [w3Resource](https://www.w3resource.com/python-exercises/list/python-data-type-list-exercise-142.php).

- Wrapping text to 80 columns using textwrap and fill from [Towards Data Science](https://towardsdatascience.com/6-fancy-built-in-text-wrapping-techniques-in-python-a78cc57c2566).


### Content

The content for the Google Sheet is ficticious.


