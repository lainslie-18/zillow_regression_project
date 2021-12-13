# zillow_regression_project

## About the project

### Project Goals

* To build a model that accurately predicts the property tax assessed values of single family properties that had a transaction during 2017

### Project Description

Accurately predicting property tax assessed values is important because it provides valuable information to our users and helps predict home values with greater accuracy. The model selected will be evaluated by how well it performs over the baseline and previous models.

### Initial Hypotheses/Questions

* Does location affect property tax value?

* Does number of bedrooms affect property tax value?

* Does number of bathrooms affect property tax value?

* What features do have the highest correlation with property tax value?

### Data dictionary

|   Column_Name   | Description | Type      |
|   -----------   | ----------- | ---------- |
| bathrooms | number of bathrooms | float |
| bedrooms   | numeric representation of internet service type | int64  |
| area      | numeric representation of contract type  | int64 |
| lot_area      | number of square feet | int64 |
| taxvalue   | indicates customer's gender        | int64    | 
| age      | indicates if customer is senior citizen      | int64 |
| county   | indicates if customer has a partner       |  object |

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
* Create wrangle.py to save these functions for importing
* Test functions
* Get familiar with data
* Document takeaways & things to address during cleaning 

**Preparation**
* Create function that cleans data
  * Convert data types
  * Handle missing values
  * Dropped observations with less than 2 or more than 5 bedrooms or more than $200,000 from the Zillow median home price for California in 2017
    * This was done to make the process relevant to the largest subset of our users
  * Create dummy variables for columns with object datatype
  * Drop columns that contain duplicate information or are unnecessary
  * Rename columns 
* Create function that splits data into train, validate, and test samples
  * Split 20% (test), 24% (validate), and 56% (train)
* Create function that scales the data
* Test functions
* Create wrangle.py to save these functions for importing

**Exploration**
* Ask questions/form hypotheses
  * Does location affect property tax value?
  * Does number of bedrooms affect property tax value?
  * Does number of bathrooms affect property tax value?
  * What features do have the highest correlation with property tax value?
* Create visualizations to help identify drivers
* Use statistical tests to test hypotheses
* Document answers to questions and takeaways
  * Property tax values are somewhat higher for Orange County but otherwise similar.
  * Even though not visible in the chart, there does appear to be a linear relationship between number of bedrooms and property tax value.
  * Statistical testing confirms, there does appear to be a linear relationship between number of bathrooms and property tax value.
  * Area has the highest correlation with property tax value at 0.3 followed by # of bathrooms at 0.23.
  * Key takeaway is that area, bathrooms, and bedrooms are the key drivers of property tax value

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
* Download the wrangle.py file to your working directory
* Download the zillow_regression_project_final notebook to your working directory
* Read this README.md
* Run the zillow_regression_project_final.ipynb notebook

### Recommendations and Next Steps
* Improve methods of data collection so that features that were not used because of null values may be implemented

* With more time and resources, I would like to conduct more feature engineering and explore the relationships between property tax value and features which initially may not seem important
