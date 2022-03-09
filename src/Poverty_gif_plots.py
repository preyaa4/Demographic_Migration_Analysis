# -*- coding: utf-8 -*-
"""
Created on Thursday Nov 25

@author: Conghao
"""
from os import read
import pandas as pd
import plotly.graph_objects as go
import imageio
import os 

def get_poverty_data_to_csv(years):
    """
    This funtion is to get porverty data of the years and output them as csv files.
    """
    assert isinstance(years, list), 'Input year should be a list'
    assert 2009 < max(years) < 2020, 'The range of the input year should be between 2010 to 2019'

    from MigrationData import MigrationData
    ##years = [2010,2011,2012,2013,2014,2015,2016,2017,2018, 2019]
    l_year_info = [MigrationData(2010)]*len(years)

    porverty_group_data = {}
    file_name = ''
    poverty_under_100 = pd.DataFrame()
    poverty_between_100_to_149 = pd.DataFrame()
    poverty_above_150 = pd.DataFrame()


    for year in years:
        l_year_info[year-2010] = MigrationData(year)
        l_year_info[year-2010].load_dframe()
        porverty_group_data[year] = l_year_info[year-2010].get_poverty_group_data(True)
        file_name = '/Users/conghaoliu/Library/Mobile Documents/com~apple~CloudDocs/ucsd/ece143/project/Demographic_Migration_Analysis-main/src/porverty_' + str(year) + '.csv'

        porverty_group_data[year].to_csv(file_name)

    for year in years:
        read_in_file = pd.read_csv('/Users/conghaoliu/Library/Mobile Documents/com~apple~CloudDocs/ucsd/ece143/project/Demographic_Migration_Analysis-main/src/porverty_' + str(year) + '.csv')
        poverty_under_100['Geographic Area Name'] = read_in_file['Geographic Area Name']
        poverty_under_100[str(year)] = read_in_file['Below 100 percent']

        poverty_between_100_to_149['Geographic Area Name'] = read_in_file['Geographic Area Name']
        poverty_between_100_to_149[str(year)] = read_in_file['100 to 149 percent']

        poverty_above_150['Geographic Area Name'] = read_in_file['Geographic Area Name']
        poverty_above_150[str(year)] = read_in_file['above 150 percent']

    read_in_state_code = pd.read_csv('/Users/conghaoliu/Library/Mobile Documents/com~apple~CloudDocs/ucsd/ece143/project/Demographic_Migration_Analysis-main/src/states.csv')
    state_code = read_in_state_code['Abbreviation']

    poverty_under_100['Geographic Area Name'] = state_code
    poverty_between_100_to_149['Geographic Area Name'] = state_code
    poverty_above_150['Geographic Area Name'] = state_code

    poverty_under_100.to_csv('/Users/conghaoliu/Library/Mobile Documents/com~apple~CloudDocs/ucsd/ece143/project/Demographic_Migration_Analysis-main/src/porverty_poverty_under_100.csv')
    poverty_between_100_to_149.to_csv('/Users/conghaoliu/Library/Mobile Documents/com~apple~CloudDocs/ucsd/ece143/project/Demographic_Migration_Analysis-main/src/poverty_between_100_to_149.csv')
    poverty_above_150.to_csv('/Users/conghaoliu/Library/Mobile Documents/com~apple~CloudDocs/ucsd/ece143/project/Demographic_Migration_Analysis-main/src/poverty_above_150.csv')

    ##print(poverty_under_100)
    ##print(poverty_between_100_to_149)
    ##print(poverty_above_150)

def print_poverty_data_to_gif(years, gif_name, filepath):
    """
    This function is to output each year's data as a png image and combine them as a gif image.
    """
    assert isinstance(years, list), 'Input years should be a list'
    assert 2009 < max(years) < 2020, 'The range of the input year should be between 2010 to 2019'

    df = pd.read_csv(filepath)
    for year in years:
        fig = go.Figure(data=go.Choropleth(
            locations=df['Geographic Area Name'], # Spatial coordinates
            z = df[str(year)].astype(float), # Data to be color-coded
            locationmode = 'USA-states', # set of locations match entries in `locations`
            colorscale = 'Reds',
            colorbar_title = "Percent",
        ))

        fig.update_layout(
            title_text = str(year) + ' Porverty probability of USA above 150',
            geo_scope='usa', # limite map scope to USA
        )
        image_name = '/Users/conghaoliu/Library/Mobile Documents/com~apple~CloudDocs/ucsd/ece143/project/Demographic_Migration_Analysis-main/src/poverty_above_150_' + str(year) + '.png'
        fig.write_image(image_name)

    with imageio.get_writer(uri=gif_name, mode='I', fps=1) as writer:
        for year in years:
            read_in_image = '/Users/conghaoliu/Library/Mobile Documents/com~apple~CloudDocs/ucsd/ece143/project/Demographic_Migration_Analysis-main/src/poverty_above_150_' + str(year) + '.png'
            writer.append_data(imageio.imread(read_in_image))








    




