# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 20:47:48 2021

@author: harsh
"""

from MigrationData import MigrationData
import pandas as pd 

def get_race_stats(year):
    assert(isinstance(year,int))
    data = MigrationData(year)
    data.load_dframe()
    return data.get_race_country_data(True)


stat_list = []

for year in range(2010,2020):
    stat_list.append(get_race_stats(year))

rename_dict = {}
for i in range(0,10):
    rename_dict[i] = i + 2010
    
race_final = pd.concat(stat_list, axis = 1)
race_final = race_final.rename(columns = rename_dict)

race_final = get_race_stats(2019)
