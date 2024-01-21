# Functions for extracting data

# General
import os.path
# For performing your HTTP requests
import requests  
# For xml & html scrapping 
from bs4 import BeautifulSoup 
# For table analysis
import pandas as pd
import numpy as np
# Write to csv
import csv
# Time
import time
# Visuals
import matplotlib.pyplot as plt
# For data cleaning
import re

def scrapeWinterOlympics(output_file, url="https://en.wikipedia.org/wiki/Winter_Olympic_Games#List_of_Winter_Olympic_Games"):
    '''
    Scrapes Wikipedia for the Winter Olympics dates and outputs into a pickle file.

        Parameters:
            output_file (str): Filepath to save output pickle file
            url (str): URL of Wikipedia page 

        Returns:
            None

    '''
    print("Scraping Wikipedia for Winter Olympics data...")

    # URL of wikipedia page from which you want to scrape tabular data.
    print("URL:", url)

    # Session object allows you to persist certain parameters across requests
    # By default, Request will keep waiting for a response indefinitely. 
    # Therefore, it is advised to set the timeout parameter.
    # If the request was successful, you should see the reponse output as '200'.
    s = requests.Session()
    response = s.get(url, timeout=10)
    print("Response:", response)
    print("A response of 200 means request was successful.")

    # parse response content to html
    soup = BeautifulSoup(response.content, 'html.parser')

    # to view the content in html format
    pretty_soup = soup.prettify()

    # title of Wikipedia page
    print("Title of Wikipedia page:", soup.title.string)

    # find all the tables in the html
    all_tables=soup.find_all('table')

    # get right table to scrape
    right_table=soup.find('table', {"class":'sortable wikitable'})

    # Get columns in the table
    cells = right_table.findAll("td")

    lst_data = []
    for row in cells:
                lst_data.append(str(row))

    print("Data:")
    print(lst_data)

    # Get list of dates
    # If "February" is in the column then that means the column is the dates column
    lst_dates = [x for x in lst_data if "February" in x]
    lst_dates_clean = [x.split('<td>')[1].split('<br/>')[0].replace(" ", "") for x in lst_dates]

    # Clean dates data
    lst_dates_clean = [x.replace('\xa0', '') for x in lst_dates_clean]
    lst_dates_clean = [x.replace('<i>', '') for x in lst_dates_clean]
    lst_dates_clean = [x.replace('</i>\n</td>', '') for x in lst_dates_clean]
    print("Cleaning dates data:")
    print(lst_dates_clean)

    # Get date pairs
    lst_date_pairs = [re.findall(r"(\d+)[^0-9.]", x) for x in lst_dates_clean]
    lst_date_pairs = [[int(int(j)) for j in i] for i in lst_date_pairs]
    print("Winter Olympics date pairs:")
    print(lst_date_pairs)

    # Get list of years
    # If "February" is in the column, then that column has the dates data
    lst_year = [x.split("February")[1] for x in lst_dates_clean]
    lst_year = [int(x) for x in lst_year]
    print("List of years for Winter Olympics:")
    print(lst_year)

    # Pull data together into a dataframe
    print("Creating dataframe...")
    winter_olympics_df = pd.DataFrame()
    winter_olympics_df['date_pairs'] = lst_date_pairs
    winter_olympics_df[['start_day','end_day']] = pd.DataFrame(winter_olympics_df.date_pairs.tolist(), index= winter_olympics_df.index)
    winter_olympics_df['start_month'] = np.where(winter_olympics_df['start_day'] >= winter_olympics_df['end_day'], 1, 2)
    winter_olympics_df['end_month'] = 2
    winter_olympics_df['year'] = lst_year

    # Save dataframe into a pickle file
    print("Saving dataframe into pickle file:", output_file)
    winter_olympics_df.to_pickle(output_file) 

    print("Success!")

def getWinterOlympics(path, refresh_data=False, url="https://en.wikipedia.org/wiki/Winter_Olympic_Games#List_of_Winter_Olympic_Games"):
    '''
    Returns the dates for the Winter Olympics.

    Parameters:
        path (string): the filepath of the expected pickle file the data should be saved in.
                       If the file does not exist, then we scrape Wikipedia to pull in the data
                       and save it into the path specified.
        refresh_data (bool): Set to True to pull in new data from Wikipedia regardless 
                             of whether data already exists.
        url (str): URL of Wikipedia page
    
    Returns:
        winter_olympics_df (dataframe): A dataframe of the Winter Olympics dates
            -------------------------------------------------------------------
            | date_pairs | start_day | end_day | start_month | end_mont | year |
            --------------------------------------------------------------------
    '''
    # If file exists do nothing, else scrape Wikipedia for the data
    if os.path.isfile(path) and not refresh_data:
        print("Taking existing file ", path)
    else:
        print("Web scraping Wikipedia for Winter Olympics dates...")
        scrapeWinterOlympics(outputfile=path, url=url)
    
    # Read pickle file and return dataframe
    winter_olympics_df = pd.DataFrame()
    winter_olympics_df = pd.read_pickle(path)

    return winter_olympics_df