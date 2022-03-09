# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 18:16:57 2021

@author: Mark

Using "wdir='*/Demographic_Migration_Analysis/src'"

Basic data processing and importing. A pyplot call is used, and one image is created.

TODO: remove the shades from the pie charts, breakup the years
"""

from MigrationData import MigrationData
import pandas as pd
import matplotlib.pyplot as plt
#import numpy as np

def correct_year(year):
    '''
    Function to check the correct year s.t. it is between 2010 and 2019
    
    Parameters
    ----------
    year: int
        the int to be checked for the domain [2010,2019]
    
    Returns
    -------
    None
    '''
    assert isinstance(year, int)
    assert year <= 2019
    assert 2010 <= year 

def get_age_group_data_allyrs(years, ispercent):
    '''
    Function to get age information for all years and return it as a dict of pandas.core.frame.DataFrame
    
    Parameters
    ----------
    ispercent: bool
        whether the return type should be in percent or not
    years: tuple
        contains a tuple of ints (years)
        
    Returns
    -------
    age_group_data: dict of pandas.core.frame.DataFrame 
        dataframes for the given years
    
    '''
    assert isinstance(ispercent, bool)
    assert isinstance(years, tuple)
    l_year_info = [MigrationData(2010)]*len(years)
    age_group_data = {}
    if ispercent:
        for year in years:
            correct_year(year)
            l_year_info[year-2010] = MigrationData(year)
            l_year_info[year-2010].load_dframe()
            age_group_data[year] = l_year_info[year-2010].get_age_group_data(ispercent)
        return age_group_data
    else:
        for year in years:
            correct_year(year)
            l_year_info[year-2010] = MigrationData(year)
            l_year_info[year-2010].load_dframe()
            age_group_data[year] = l_year_info[year-2010].get_age_group_data(ispercent).astype('int32')
        return age_group_data

def get_sex_group_data_allyrs(years, ispercent):
    '''
    Function to get age information for all years and return it as a dict of pandas.core.frame.DataFrame
    
    Parameters
    ----------
    ispercent: bool
        whether the return type should be in percent or not
    years: tuple
        contains a tuple of ints (years)
        
    Returns
    -------
    age_group_data: dict of pandas.core.frame.DataFrame 
        dataframes for the given years
    
    '''
    assert isinstance(ispercent, bool)
    assert isinstance(years, tuple)
    l_year_info = [MigrationData(2010)]*len(years)
    age_group_data = {}
    if ispercent:
        for year in years:
            correct_year(year)
            l_year_info[year-2010] = MigrationData(year)
            l_year_info[year-2010].load_dframe()
            age_group_data[year] = l_year_info[year-2010].get_sex_group_data(ispercent)
        return age_group_data
    else:
        for year in years:
            correct_year(year)
            l_year_info[year-2010] = MigrationData(year)
            l_year_info[year-2010].load_dframe()
            age_group_data[year] = l_year_info[year-2010].get_sex_group_data(ispercent).astype('int32')
        return age_group_data

def get_age_info_years_state(data, state, years):
    '''
    Function to get all years info for a certain state. This is assumed to come after the 
    get_age_group_data_allyrs.
    
    Parameters
    ----------
    Data: dict
        dict of years of type pd.core.frame.DataFrame
    state:str
        the string of the state to be used
    years: tuple
        contains the valid years for which to be analyzed
        
    Returns
    -------
    all_years_population_data_state: pandas.core.frame.DataFrame
        the years information by age and state; the columns will be the groupings of the age 
        and the index will be the years
    '''
    #Next 4 lines are for enforcing the data model
    assert isinstance(data,dict)
    for year in years: #check the years are correct!
        correct_year(year)
        assert (state in data[year].axes[0])
    cols = ('1 to 17 years', '18 to 24 years', '25 to 54 years', '55 years and over')
    all_years_population_data_state = []
    for year in years:
        all_years_population_data_state.append(data[year].loc[state])
    all_years_population_data_state = pd.DataFrame(all_years_population_data_state,columns = cols, index = years)
    return all_years_population_data_state
    
if  __name__ == '__main__':
    years = (2010,2011,2012,2013,2014,2015,2016,2017,2018, 2019)
    age_keys = ('1 to 17 years', '18 to 24 years', '25 to 54 years', '55 years and over')
    
    #Plotting age info for California
    age_data_allyrs = get_age_group_data_allyrs(years,False);
    #Graphing of California_migration_pyplot.png
    #california_info_by_age = get_age_info_years_state(age_data_allyrs, 'California', years)
    #plot_cali = california_info_by_age.plot(title="California's inflow migration by age group")
    for year in years:
        age_data_allyrs[year] = age_data_allyrs[year].sum()
    #Break into under 24 and over 24
    age_data_df = pd.DataFrame(age_data_allyrs.values(), index = years, columns = age_keys)
    age_data_df.loc[:,'Total'] = age_data_df.sum(axis=1)
    '''frame_young = {age_keys[0]: age_data_df[age_keys[0]], age_keys[1]: age_data_df[age_keys[1]]}
    y_pf=pd.DataFrame(frame_young) #youth pandas dataframe
    y_plot = y_pf.plot.bar(stacked=True, title = "Youth migration follows a roughly linear path", rot = 0); 
    #y_plot means youth's plot
    y_plot.legend(loc = 'lower center')
    #y_plot.grid(axis = 'y')
    #y_plot.set_ylim((2800000,3400000))
    #y_plot.spines['top'].set_visible(False)
    y_plot.ticklabel_format(axis = 'y', useMathText = True)
    y_plot.set_ylabel("Youths migrating")
    y_plot.set_xlabel("Year")
    y_plot.plot()'''
    
    '''for age in age_keys:
        age_data_df[age] = age_data_df[age]/age_data_df['Total']
    age_data_df = age_data_df.drop(columns = 'Total')
    ax2 = age_data_df.plot()
    ax2.set_ylabel("Age demographics")
    ax2.set_xlabel("Year")
    ax2.plot()'''
    
    
    '''age_data_seniors = age_data_df[age_keys[3]]/age_data_df[age_keys[3]][2019]
    ax3 = age_data_seniors.plot(title = "Senior-aged migration")
    ax3.set_ylabel("Percent of migrants as a proportion of 2019")
    ax3.set_xlabel("Year")
    ax3.plot()'''
    
    #Below are other plots, that are kept for documentation purposes and DID NOT make it into the presentation
    sizes = [age_data_df[age_keys[0]][2010]/age_data_df['Total'][2010], age_data_df[age_keys[1]][2010]/age_data_df['Total'][2010], age_data_df[age_keys[2]][2010]/age_data_df['Total'][2010], age_data_df[age_keys[3]][2010]/age_data_df['Total'][2010]]
    explode = (0,0,0,0)
    fig4, ax4 = plt.subplots()
    ax4.pie(sizes, explode=explode, labels=age_keys, autopct='%1.1f%%', startangle=90)
    ax4.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax4.title.set_text("Migrant age composition in 2010")
    plt.savefig('../Visualization_and_plots/age_plots/age_2010.png')
    
    sizes = [age_data_df[age_keys[0]][2019]/age_data_df['Total'][2019], age_data_df[age_keys[1]][2019]/age_data_df['Total'][2019], age_data_df[age_keys[2]][2019]/age_data_df['Total'][2019], age_data_df[age_keys[3]][2019]/age_data_df['Total'][2019]]
    explode = (0,0,0,0)
    fig4, ax4 = plt.subplots()
    ax4.pie(sizes, explode=explode, labels=age_keys, autopct='%1.1f%%', startangle=90)
    ax4.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax4.title.set_text("Migrant age composition in 2019")
    plt.savefig('../Visualization_and_plots/age_plots/age_2019.png')
    
    '''#Plotting the increase in working class migration
    #frame_worth = {age_keys[2]: age_data_df[age_keys[2]]}
    #w_df = pd.DataFrame(frame_worth)
    w_plot = age_data_df[age_keys[3]].plot(title = "Large increase in old people migrating", rot = 0)
    w_plot.ticklabel_format(axis = 'y')
    w_plot.set_xlabel("Year")
    w_plot.legend(loc = 'lower right')
    w_plot.plot()'''
    
    #Plotting sex data, specifically the difference in the male and female migrants with bar graphs
    sex_data = get_sex_group_data_allyrs(years,False)
    for year in years:
        sex_data[year] = sex_data[year].sum()
    sex_data_df = pd.DataFrame(sex_data.values(), index = years, columns = ['Male', 'Female'])
    '''#initial_sex_dif = sex_data_df['Male'][2010] - sex_data_df['Female'][2010]
    #fin_sex_dif = sex_data_df['Male'][2019] - sex_data_df['Female'][2019]
    sex_data_df['Total'] = sex_data_df['Male'] + sex_data_df['Female']
    sex_data_df['Male'] = sex_data_df['Male']/ sex_data_df['Total']
    sex_data_df['Female'] = sex_data_df['Female']/ sex_data_df['Total']
    sex_data_df = sex_data_df.drop(columns = 'Total')
    ax = sex_data_df.plot(title = 'Male vs female migration percent trends')
    ax.set_ylabel("Percent of migrants")
    ax.set_xlabel("Year")
    ax.plot()'''
    
    
    #Plotting for 2010 pie chart male vs female
    labels = 'Male', 'Female'
    sizes = [sex_data_df['Male'][2010], sex_data_df['Female'][2010]]
    explode = (0,0)
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1.title.set_text("Male vs female migrants % in 2010")
    plt.savefig('../Visualization_and_plots/sex_stat_plots/male_vs_female_2010.png')
    #Plotting for 2019 pie chart male vs female
    sizes = [sex_data_df['Male'][2019], sex_data_df['Female'][2019]]
    explode = (0,0)
    fig2, ax2 = plt.subplots()
    ax2.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', startangle=90)
    ax2.title.set_text("Male vs female migrants % in 2019")
    ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig('../Visualization_and_plots/sex_stat_plots/male_vs_female_2019.png')
    
