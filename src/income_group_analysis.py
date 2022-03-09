# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 20:57:21 2021

@author: harsh
"""


from MigrationData import MigrationData
import pandas as pd 

def get_income_stats(year):
    assert(isinstance(year,int))
    data = MigrationData(year)
    data.load_dframe()
    return data.get_income_country_data(True)


stat_list = []

for year in range(2010,2020):
    stat_list.append(get_income_stats(year))

rename_dict = {}
for i in range(0,10):
    rename_dict[i] = i + 2010
    
income_final = pd.concat(stat_list, axis = 1)
income_final = income_final.rename(columns = rename_dict)

