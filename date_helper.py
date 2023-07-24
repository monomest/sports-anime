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