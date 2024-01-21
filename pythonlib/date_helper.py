# Analytics
import pandas as pd   
import numpy as np 
# Date libraries
import calendar
from datetime import datetime

def getYears(trend_df):
    '''
    Returns a list of all the years in the dataframe

        Parameters:
                trend_df (dataframe): A dataframe with the structure:
                                      --------------------------------------
                                      | date | interest_level | is_partial |
                                      -------|----------------|------------|

        Returns:
                years_lst (str): A list of all the years in the dataframe e.g., ['2020', '2021', '2022']
    '''
    years_lst = np.unique(trend_df.date.unique().year).tolist()
    return years_lst

def getLastDay(year, month):
    '''
    Returns the last day of a given month in a year

        Parameters:
                year (int): The year e.g., 2004
                month (int): The month e.g., 1 = January, 12 = December
        Returns:
                last_day (int): The last day of the month
    '''
    month_range = calendar.monthrange(year, month)
    last_day = month_range[1]
    return last_day

def getDates(years_lst):
    '''
    Returns a date dataframe for use in calling the Google Trends API

        Parameters:
                years_lst (int): A list of integers denoting years e.g., [2004, 2005, 2006]
        Returns:
                ym_df (dataframe): A dataframe with the structure:
                ------------------------------------------------------------------------------------
                | year | month | first_day | last_day| start_date | end_date |     date_range      |
                -------|-------|-----------|----------------------|----------|----------------------
                | 2004 |   1   |    1      |   31    | 2004-01-01 |2004-01-31|2004-01-01 2004-01-31|
                ------------------------------------------------------------------------------------
                |  ..  |  ..   |  .....    |    ...  |   ....     |   ....   |     ....            |
    '''

    # Create a month dataframe from 1 = January to 12 = December
    month_df = pd.DataFrame()
    month_df['month'] = pd.DataFrame(np.arange(1,13,1))
    month_df

    # Create a years dataframe of all the years that have available data
    years_df = pd.DataFrame()
    years_df['year'] = pd.DataFrame(years_lst)

    # Perform a cross join of years and month to get dataframe of every month for every year
    month_df['key'] = 0 # Arbitrary key to join on
    years_df['key'] = 0 # Arbitrary key to join on
    ym_df = years_df.merge(month_df, on='key', how='outer').drop(columns='key') # year-month dataframe

    # Get the first and last days of each month for each year
    ym_df['first_day'] = 1
    ym_df['last_day'] = ym_df.apply(lambda row : 
                                    getLastDay(row['year'], row['month']), 
                                    axis=1)
    
    # Get the date ranges for each month
    ym_df['start_date'] = ym_df.apply(lambda row :
                                            str(row['year']) + "-" + "{:02d}".format(row['month']) + "-" + "{:02d}".format(row['first_day']),
                                            axis=1)
    ym_df['end_date'] = ym_df.apply(lambda row :
                                            str(row['year']) + "-" + "{:02d}".format(row['month']) + "-" + "{:02d}".format(row['last_day']),
                                            axis=1)
    ym_df['date_range'] = ym_df.apply(lambda row :
                                            row['start_date'] + " " + row['end_date'],
                                            axis=1)

    return ym_df

def getDateFeatures(trend_df):
    '''
    Returns the year and month features for an interest level dataframe.

        Parameters:
                trend_df (dataframe): A dataframe with the structure:
                                      --------------------------------------
                                      | date | interest_level | is_partial |
                                      -------|----------------|-------------

        Returns:
                trend_df (dataframe): The original dataframe plus month and year features:
                                      -----------------------------------------------------
                                      | date | interest_level | is_partial | year | month |
                                      -------|----------------|------------|------|--------
    '''
    # If the date feature columns do not already exist, then create the date feature columns
    if 'year' not in trend_df.columns.tolist() and 'month' not in trend_df.columns.tolist():
        trend_df['year'] = pd.DatetimeIndex(trend_df['date']).year
        trend_df['month'] = pd.DatetimeIndex(trend_df['date']).month
    return trend_df

def getPastInterest(df, interest_col, hist_interest_col):
    '''
    Returns the interest_level for the same month in the previous year
        Parameters:
            df (dataframe): A dataframe with at least the columns "year", "month", "interest_level"
            interest_col (str): The name of the column referring to the the interest level
            hist_interest_col (str): The name of the column to be created

        Returns:
            join_df (dataframe): The original dataframe plus column hist_interest_col
    '''
    # Join the current year with data for the same month in the previous year
    hist_df = pd.DataFrame()
    hist_df['year_hist'] = df['year']
    hist_df['month_match'] = df['month']
    hist_df['year_match'] = df['year'] + 1
    hist_df[hist_interest_col] = df[interest_col]
    # Perform the join
    join_df = pd.DataFrame()
    join_df = pd.merge(df, hist_df, how='left',  left_on=['year', 'month'], right_on=['year_match', 'month_match'], indicator=True)

    # Where you cannot find historical, just replace with current
    join_df[hist_interest_col] = join_df[hist_interest_col].where(join_df['_merge']=="both", join_df[interest_col])
    
    return join_df