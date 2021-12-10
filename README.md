# zillow_regression_project

## About the project

### Project Goals

* To build a model that accurately predicts the property tax assessed values of single family properties that had a transaction during 2017

### Project Description

Accurately predicting property tax assessed values is important because it provides valuable information to our users and helps predict home values with greater accuracy. The model selected will be evaluated by how well it performs over the baseline and previous models.

### Initial Hypotheses/Questions

* Do customers with month-to-month contracts churn at a higher rate? What are the churn rates with other contract types?

* Is there a certain tenure length where month-to-month customers are more likely to churn? What about customers with contracts?

* Is any specific service associated with higher churn rates?

* Is it higher monthly charges that are causing churn? If so, what is that threshold where most customers churn for their specific service?

### Data dictionary

|   Column_Name   | Description | Type      |
|   -----------   | ----------- | ---------- |
| payment_type_id | numeric representation of payment type | int64 |
| internet_service_type_id   | numeric representation of internet service type | int64  |
| contract_type_id      | numeric representation of contract type  | int64 |
| customer_id      | unique value associated with customer | int64 |
| gender   | indicates customer's gender        | object    | 
| senior_citizen      | indicates if customer is senior citizen      | int64 |
| partner   | indicates if customer has a partner       |  object |
| dependents      | indicates if customer has dependents  | object
| tenure   | indicates number of months customer has had service        | int64        | 
| phone_service   | indicates if customer has phone service | object | 
| multiple_lines      | indicates if customer has multiple lines | object
| online_security   | indicates if customer has online security | object | 
| online_backup      | indicates if customer has online backup | object |
| device_protection   | indicates if customer has device protection | object  |
| tech_support      | indicates if customer has tech support| object |
| streaming_tv   | indicates if customer has streaming tv | object  |
| streaming_movies   | indicates if customer has streaming movies | object   |
| paperless_billing      | indicates if customer has paperless billing | object |
| monthly_charges   | customer's monthly charges | float64 |
| total_charges      | customer's total accumulated charges       | float64 |
| churn   | indicates if customer has churned | object   |
| contract_type   | indicates customer's contract type (month-to-month, one year, or two year)| object        |
| internet_service_type      | indicates customer's internet service type (no internet, fiber optic, or DSL) | object
| payment_type   | indicates customer's payment type (electronic check, mailed check, bank transfer (automatic), or credit card (automatic) | object        |

### Project Planning

**Planning**

* Define goals
* Determine audience and delivery format
* What is my MVP?
* Ask questions/formulate hypotheses

**Acquisition**
* Create function for establishing connection to zillow db
* Create function for SQL query and reading in results
* Create function for caching data
* Create acquire.py to save these functions for importing
* Test functions
* Get familiar with data
* Document takeaways & things to address during cleaning 

**Preparation**
* Create function that cleans data
  * Convert data types
  * Handle missing values
  * -
  * Create dummy variables for columns with object datatype
  * Drop columns that contain duplicate information or are unnecessary
  * Rename columns 
* Create function that splits data into train, validate, and test samples
  * Split 20% (test), 24% (validate), and 56% (train)
* Create prepare.py to save these functions for importing
* Create function that scales the data
* Test functions

**Exploration**
* Ask questions/form hypotheses
  * Do customers with month-to-month contracts churn more than other contract types?
  * Is there a tenure length where customers are more likely to churn?
  * Is a specific internet service type associated with higher churn rates?
  * Is it higher monthly charges that are causing churn?
* Create visualizations to help identify drivers
* Use statistical tests to test hypotheses
* Document answers to questions and takeaways
  * Month-to-month customers churn at almost 5x the rate of those with contracts.
  * The largest portion of customers who churn do so within the first 6 months.
  * Both the chart and test show that fiber optic customers are more likely to churn.
  * Both the chart and test show that churn is associated with higher monthly charges.
  * Key takeaway is that customers are unhappy with the higher prices associated with fiber optic service and/or the quality of fiber optic service

**Modeling**
* Identify, select, and create features
* Establish a baseline
* Build, fit and use models to make predictions
* Compute evaluation metrics to evaluate models' performance
* Select best model and use on test dataset

**Delivery**
* Report will be in Jupyter Notebook
* Present via Zoom
* Audience will be the Zillow data science team

### To Recreate This Project:
* You will need an env file with your database credentials (user, password, hostname) saved to your working directory
* Create a gitignore and add your env file to prevent your credentials from getting pushed to Github
* Download the aquire.py and prepare.py files to your working directory
* Download the zillow_regression_project_final notebook to your working directory
* Read this README.md
* Run the zillow_regression_project_final.ipynb notebook

### Recommendations and Next Steps
* Reduce monthly price for fiber optic internet service

* Send out quarterly customer satisfaction surveys for better insights

* With more time and resources, would like to collect and explore customer satisfaction data
