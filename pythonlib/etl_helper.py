# Functions to help extract, transform and load data

def cleanTrainingDataset(trend_df):
    '''
    Returns a clean dataset for a given dataframe:
        1. Remove isPartial = True
        2. Takes data up until October 2016 (the month that "Yuri on Ice" aired)

        Parameters:
                trend_df (dataframe): A dataframe with the structure:
                                      --------------------------------------------
                                      | date | interest_level | is_partial |......
                                      -------|----------------|------------|------

        Returns:
                clean_df (dataframe): The cleaned version of original dataframe
    '''
    clean_df = trend_df.loc[(trend_df['isPartial'] == False) & (trend_df['date'] < '2016-10-01')]
    return clean_df

def cleanPredictionDataset(trend_df):
    '''
    Returns a clean dataset to predict for the effect without Yuri on Ice, for a given dataframe:
        1. Remove isPartial = True
        2. Takes data from all available years
    
    Parameters:
        trend_df (dataframe): A dataframe with the structure:
                                --------------------------------------------
                                | date | interest_level | is_partial |......
                                -------|----------------|------------|------
    Returns:
            prediction_df (dataframe): The cleaned version of original dataframe for predictions
    '''
    prediction_df = trend_df.loc[(trend_df['isPartial'] == False)]
    return prediction_df