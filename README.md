## Instructions

### How to run the test
Before running the test. Make sure to install all the required packages to the project
* pip install -r requirements. txt in your terminal
* Last python version used is 3.12.4

Navigate to root folder and run
* $ pytest --html=reports/report.html
* Default Browser is firefox
  * add --browser option to run a different browser e.g. --browser edge
* Browser Options:
  * chrome
  * edge
  * firefox
* To run specific marked tests
  * pytest --html=reports/report.html -m smoke
