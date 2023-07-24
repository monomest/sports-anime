# General
import os.path
# GoogleTrends API
from pytrends.request import TrendReq
# Analytics
import pandas as pd  

def getInterestOverTime(search_term_lst, topic_name, timeframe='2004-01-01 2023-07-01', geo='', gprop=''):
    '''
    Returns the global interest over time for a search term in Google

        Parameters:
                search_term_lst (list): A list containing the string denoting the search term e.g., ["Yuri on Ice"]
                topic_name (str): The specific topic related to the search term e.g., "Japanese animated series"
                timeframe (str): Date to start from. Defaults to specific timeframe. 
                    Set to 'all' for everything
                    Specific dates, 'YYYY-MM-DD YYYY-MM-DD' example '2016-12-14 2017-01-25'
                    Specific datetimes, 'YYYY-MM-DDTHH YYYY-MM-DDTHH' example '2017-02-06T10 2017-02-12T07'
                geo (str): Two letter country abbreviation, defaults to '' for world e.g., "US" for United States
                gprop (str): What Google property to filter to, defaults to '' for web search 
                                Can be 'images', 'news', 'youtube' or 'froogle' (for Google Shopping results)

        Returns:
                topic_id (str): The id of the topic_name e.g., '/g/11cmg5bxns' is the id for the search term
                                "Yuri on Ice" where the topic_name is "Japanese animated series"
                trend_df (dataframe): The dataframe containing the interest over time for the search_term and topic_id
    '''
    # Connect to Google
    pytrend = TrendReq()
    
    # Build payload
    pytrend.build_payload(search_term_lst, cat=0, timeframe=timeframe, geo=geo, gprop=gprop)
    # Retrieve topic_id 
    # As per: https://stackoverflow.com/questions/47389000/pytrends-how-to-specify-a-word-as-a-topic-instead-of-a-search-term
    keywords = pytrend.suggestions(search_term_lst[0])
    keywords_df = pd.DataFrame(keywords)
    topic_id = keywords_df[keywords_df["type"]==topic_name].mid[0]

    # Build payload again with the topic_id as the search term
    search_term_lst = [topic_id]
    # Get interest over time for the topic_id
    pytrend.build_payload(search_term_lst, cat=0, timeframe=timeframe, geo=geo, gprop=gprop)
    trend_df = pytrend.interest_over_time()
    
    # Clean up the dataframe
    trend_df.reset_index(inplace=True)
    trend_df.rename(columns={topic_id: "interest_level", "is_partial": "isPartial"}, inplace=True)

    return topic_id, trend_df

def getMonthlyInterest(path, search_term_lst, topic_name):
    '''
    Returns the monthly global interest over time for a search term in Google

    Parameters:
        path (string): the filepath of the expected pickle file the data should be saved in.
                       If the file does not exist, then we use GoogleTrends API to pull in the data
                       and save it into the path specified.
        search_term_lst (list): A list containing the string denoting the search term e.g., ["Yuri on Ice"]
        topic_name (str): The specific topic related to the search term e.g., "Japanese animated series"
    
    '''
    if os.path.isfile(path):
        print("Taking existing file ", path)
        yuri_world_df = pd.DataFrame()
        yuri_world_df = pd.read_pickle(path)
    else:
        print("Getting interest over time for Yuri on Ice...")
        yuri_topic_id, yuri_world_df = getInterestOverTime(search_term_lst, topic_name)
        # Save to pickle file
        print("Saving data into ", path)
        yuri_world_df.to_pickle(path)
    return yuri_world_df