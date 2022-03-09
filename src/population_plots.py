# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 07:41:28 2021

@author: harsh
"""

from MigrationData import MigrationData
import pandas as pd 
import plotly.graph_objects as go
import plotly.express as px
import imageio
import os 

def get_population_stats(year):
    '''
    Function to get the overall population statistics for a particular year 

    Parameters
    ----------
    year : int
        year.

    Returns
    -------
    population : pd.core.frame.DataFrame
        DESCRIPTION.

    '''
    assert(isinstance(year,int))
    data = MigrationData(year)
    data.load_dframe()
    
    # if year > 2017:
    #     key_str = 'Estimate!!Moved; from different  state!!Population 1 year and over'
    # else:
    #     key_str = 'Moved; from different  state!!Estimate!!Population 1 year and over'
    # pop_key = data.get_key(data.dframe, key_str)
    
    # if year > 2017:
    #     key_str = 'Estimate!!Total!!Population 1 year and over'
    # else:
    #     key_str = 'Total!!Estimate!!Population 1 year and over'
    # pop_total_key = data.get_key(data.dframe, key_str)
    # # print(pop_key)
    # population_keys = ['Geographic Area Name', pop_key]
    
    # population = data.dframe[population_keys].rename(columns = {"Geographic Area Name":"state", pop_key:'population'})
    # # population = population.rename(columns = {"Geographic Area Name":"state", 'Population 1 year and over':'population'})
    population = data.get_population_stats().rename(columns = {"state":"state", 'population_total':'population','population':'percentage'})
    state_codes = pd.read_csv("../data/state_code.csv")
    
    population = pd.merge(population, state_codes, on='state')
    population['year'] = [year]*len(population['state'])
    return population 


def gen_state_map(population,fname, plot_name):
    '''
    Function to generate the state level data map 

    Parameters
    ----------
    population : pd.core.frame.DataFrame
        input population stats data frame
    fname : str
        file name of the figure.
    plot_name : str
        Plot description 

    Returns
    -------
    None.
    Saves a plot with the given name

    '''
    assert(isinstance(population,pd.core.frame.DataFrame))
    assert(isinstance(fname,str))
    assert(isinstance(plot_name,str))
    fig = go.Figure(data=go.Choropleth(
        locations=population['code'], # Spatial coordinates
        z = population['population'].astype(float), # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Blues',
        colorbar_title = "Population",
    ))
    
    fig.update_layout(
        title_text = plot_name,
        geo_scope='usa', # limite map scope to USA
    )
    fig.add_scattergeo(locations=population['code'],
                       locationmode='USA-states',
                       text=population['code'],
                       mode='text')
    
    #fig.show()
    fig.write_image(fname)


images = []
directory = '../Visualization_and_plots/population_stat_plots/'
try:
    os.stat(directory)
except:
    os.mkdir(directory)
for year in range(2010,2020):
    population = get_population_stats(year)
    fname = directory +str(year) +"_population_stats.png"
    plot_name = 'Population Moved from a Different State in ' + str(year)
    gen_state_map(population,fname, plot_name)
    images.append(imageio.imread(fname))
    print("Plot generated for the year ",year)
imageio.mimsave(directory+'population_migrated_numbers.gif', images, format='GIF', duration=1)

# year = 2010 
# population = get_population_stats(year)
# fname = str(year) +"_population_stats.png"
# plot_name = 'Percentage of Population Moved from a Different State in ' + str(year)
# gen_state_map(population,fname, plot_name)

# for year in range(2011,2020):
#     population = population.append(get_population_stats(year), ignore_index = True)


# fig = px.choropleth_mapbox(population,
#                            scope = "usa",
#                            featureidkey='properties.name',
#                            locations='code',
#                            color='Count',
#                            hover_name='code',
#                            hover_data=['population'],
#                            color_continuous_scale='Reds',
#                            animation_frame='year',
#                            mapbox_style='carto-positron',
#                            title='Cumulative Numbers of Crimes in Vancouver Neighborhoods',
#                            center={'lat':49.25, 'lon':-123.13},
#                            zoom=11,
#                            opacity=0.75,
#                            labels={'Count':'Count'},
#                            width=1100,
#                            height=800
#                           )

