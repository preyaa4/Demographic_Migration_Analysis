# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 20:14:57 2021

@author: harsh
"""

from MigrationData import MigrationData
import pandas as pd 

def get_sex_stats(year):
    assert(isinstance(year,int))
    data = MigrationData(year)
    data.load_dframe()
    return data.get_sex_country_data(True)


stat_list = []

for year in range(2010,2020):
    stat_list.append(get_sex_stats(year))

rename_dict = {}
for i in range(0,10):
    rename_dict[i] = i + 2010
    
sex_final = pd.concat(stat_list, axis = 1)
sex_final = sex_final.rename(columns = rename_dict)


