import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import sklearn.preprocessing
import os
import env


########## Acquire ##########

def get_connection(db, user=env.user, host=env.host, password=env.password):
    '''
    This function takes in user credentials from an env.py file and a database name and creates a connection to the Codeup database through a connection string 
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'


zillow_sql_query =  '''
                    select *
                    from properties_2017
                    join predictions_2017 using(parcelid)
                    join propertylandusetype using(propertylandusetypeid)
                    where propertylandusedesc = 'Single Family Residential'
                    and transactiondate like '2017%%';
                    '''

def query_zillow_data():
    '''
    This function uses the get_connection function to connect to the zillow database and returns the zillow_sql_query read into a pandas dataframe
    '''
    return pd.read_sql(zillow_sql_query,get_connection('zillow'))


def get_zillow_data():
    '''
    This function checks for a local zillow.csv file and reads it into a pandas dataframe, if it exists. If not, it uses the get_connection & query_zillow_data functions to query the data and write it locally to a csv file
    '''
    # If csv file exists locally, read in data from csv file.
    if os.path.isfile('zillow.csv'):
        df = pd.read_csv('zillow.csv', index_col=0)
        
    else:
        
        # Query and read data from zillow database
        df = query_zillow_data()
        
        # Cache data
        df.to_csv('zillow.csv')
        
    return df


########## Clean & Split ##########

def get_cols_with_large_null_percentage(df, percentage):
    '''
    This function takes in a dataframe and a percentage and returns a list of columns that have 
    a greater percentage of nulls than provided as an argument
    '''
    
    # Set null threshold. Any columns that have this ratio or higher of nulls will be removed
    null_perc_thresh = percentage

    # Create empty list to keep track of which columns to drop
    cols_with_many_nulls = []

    # Loop through df and append columns with null percentage higher than specified to cols_to_drop list
    for col in df.columns:
        num_nulls = df[col].isnull().sum()
        if num_nulls == 0:
            continue
        null_perc = num_nulls / len(df)
        if null_perc > null_perc_thresh:
            cols_with_many_nulls.append(col)
        
    return cols_with_many_nulls


def remove_outliers(df, k, col_list):
    ''' 
    This function takes in a dataframe, value of k, and a list of columns, removes outliers greater than k times IQR above the 75th percentile and lower than k times IQR below the 25th percentile from the list of columns specified and returns a dataframe
    '''
    
    # loop through each column
    for col in col_list:

        q1, q3 = df[col].quantile([.25, .75])  # get quartiles
        
        iqr = q3 - q1   # calculate interquartile range
        
        upper_bound = q3 + k * iqr   # get upper bound
        lower_bound = q1 - k * iqr   # get lower bound

        # return dataframe without outliers
        df = df[(df[col] > lower_bound) & (df[col] < upper_bound)]
        
    return df


def clean_zillow_data(df):
    '''
    This function takes in the zillow data, cleans it, and returns a dataframe
    '''

    # create list of columns to drop based on percentage of null values
    cols_to_drop = get_cols_with_large_null_percentage(df, 0.35)

    # specify more columns to drop that are duplicated, unnecessary, or not useful
    cols_to_drop.extend(['propertylandusetypeid','id','calculatedbathnbr','finishedsquarefeet12','fullbathcnt','latitude','longitude',
                        'propertycountylandusecode','rawcensustractandblock','regionidzip','structuretaxvaluedollarcnt','assessmentyear',
                        'landtaxvaluedollarcnt','taxamount','censustractandblock','id.1','logerror','transactiondate','propertylandusedesc',
                        'regionidcity','regionidcounty','parcelid','roomcnt'])

    # drop columns that are unncessary or have too many null counts
    df = df.drop(columns=cols_to_drop)

    # drop rows with null values
    df = df.dropna()

     # Rename some columns for simplicity
    df = df.rename(columns={'bedroomcnt':'bedrooms','bathroomcnt':'bathrooms','calculatedfinishedsquarefeet':'area',
                            'lotsizesquarefeet':'lot_area','taxvaluedollarcnt':'taxvalue'})
    
    # create age column based on yearbuilt
    df['age'] = 2021 - df.yearbuilt

    # use a function to remove outliers
    df = remove_outliers(df,1.5,['bedrooms','bathrooms','area','lot_area','taxvalue','age'])

    # drop more outliers where area > 3500 or < 500 sq ft and where tax value > $1,500,000 or < $50,000
    df = df[((df.area < 3500) & (df.area > 500)) & ((df.taxvalue < 1_500_000) & (df.taxvalue > 50_000))]
    
    # Create list of datatypes I want to change
    int_col_list = ['bedrooms','area','taxvalue','age']
    obj_col_list = ['yearbuilt']
    
    # Change data types where it makes sense
    for col in df:
        if col in int_col_list:
            df[col] = df[col].astype(int)
        if col in obj_col_list:
            df[col] = df[col].astype(int).astype(object)

    # replace fips with city & state for readability
    df.fips = df.fips.replace({6037:'Los Angeles, CA',6059:'Orange, CA',6111:'Ventura, CA'})

    # Encode FIPS column, concatenate onto original dataframe, and drop fips column
    dummy_df = pd.get_dummies(df['fips'])
    df = pd.concat([df, dummy_df], axis=1).drop(columns='fips')
    
    return df


########## Split ##########

# Split the data into train, validate, and test
def split_data(df, random_state=369, stratify=None):
    '''
    This function takes in a dataframe and splits the data into train, validate and test samples. 
    Test, validate, and train are 20%, 24%, & 56% of the original dataset, respectively. 
    The function returns train, validate and test dataframes.
    '''
   
    if stratify == None:
        # split dataframe 80/20
        train_validate, test = train_test_split(df, test_size=.2, random_state=random_state)

        # split larger dataframe from previous split 70/30
        train, validate = train_test_split(train_validate, test_size=.3, random_state=random_state)
    else:

        # split dataframe 80/20
        train_validate, test = train_test_split(df, test_size=.2, random_state=random_state, stratify=df[stratify])

        # split larger dataframe from previous split 70/30
        train, validate = train_test_split(train_validate, test_size=.3, 
                            random_state=random_state,stratify=train_validate[stratify])

    # results in 3 dataframes
    return train, validate, test


# create function that scales train, validate, and test datasets using standardscaler
def scale_data_standardscaler(train, validate, test):
    '''
    This function takes in train, validate, and test data sets, scales them using sklearn's StandardScaler
    and returns three scaled data sets
    '''
    # Create the scaler
    scaler = sklearn.preprocessing.StandardScaler()

    # Fit scaler on train dataset
    scaler.fit(train)

    # Transform and rename columns for all three datasets
    train_scaled = pd.DataFrame(scaler.transform(train), columns = train.columns.tolist())
    validate_scaled = pd.DataFrame(scaler.transform(validate), columns = train.columns.tolist())
    test_scaled = pd.DataFrame(scaler.transform(test), columns = train.columns.tolist())

    return train_scaled, validate_scaled, test_scaled

########## Wrangle ##########

def wrangle_zillow():
    '''This function acquires, cleans, and splits data from the zillow database for exploration'''
    # acquire, clean, and split
    train, validate, test = split_data(clean_zillow_data(get_zillow_data()))
    # scale data
    train_scaled, validate_scaled, test_scaled = scale_data_standardscaler(train, validate, test)
    
    return train, validate, test, train_scaled, validate_scaled, test_scaled