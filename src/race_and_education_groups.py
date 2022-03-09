# -*- coding: utf-8 -*-
"""Race_and_education_groups.ipynb
"""

# Commented out IPython magic to ensure Python compatibility.
# %run MigrationData.py

import pandas as pd
import matplotlib.pyplot as plt

# 2010 data #

data_2010 = MigrationData(2010)
data_2010.load_dframe()

race_data_2010 = data_2010.get_race_group_data(False)
ea_data_2010 = data_2010.get_key_data('EDUCATIONAL ATTAINMENT','state', False)



# 2011 data #

data_2011 = MigrationData(2011)
data_2011.load_dframe()

race_data_2011 = data_2011.get_race_group_data(False)
ea_data_2011 = data_2011.get_key_data('EDUCATIONAL ATTAINMENT','state', False)



# 2012 data #

data_2012 = MigrationData(2012)
data_2012.load_dframe()


race_data_2012 = data_2012.get_race_group_data(False)
ea_data_2012 = data_2012.get_key_data('EDUCATIONAL ATTAINMENT','state', False)



# 2013 data #

data_2013 = MigrationData(2013)
data_2013.load_dframe()


race_data_2013 = data_2013.get_race_group_data(False)
ea_data_2013 = data_2013.get_key_data('EDUCATIONAL ATTAINMENT','state', False)


# 2014 data #

data_2014 = MigrationData(2014)
data_2014.load_dframe()

race_data_2014 = data_2014.get_race_group_data(False)
ea_data_2014 = data_2014.get_key_data('EDUCATIONAL ATTAINMENT','state', False)

# 2015 data #

data_2015 = MigrationData(2015)
data_2015.load_dframe()


race_data_2015 = data_2015.get_race_group_data(False)
ea_data_2015 = data_2015.get_key_data('EDUCATIONAL ATTAINMENT','state', False)

# 2016 data #

data_2016 = MigrationData(2016)
data_2016.load_dframe()


race_data_2016 = data_2016.get_race_group_data(False)
ea_data_2016 = data_2016.get_key_data('EDUCATIONAL ATTAINMENT','state', False)

# 2017 data #

data_2017 = MigrationData(2017)
data_2017.load_dframe()

race_data_2017 = data_2017.get_race_group_data(False)
ea_data_2017 = data_2017.get_key_data('EDUCATIONAL ATTAINMENT','state', False)

# 2018 data #

data_2018 = MigrationData(2018)
data_2018.load_dframe()

race_data_2018 = data_2018.get_race_group_data(False)
ea_data_2018 = data_2018.get_key_data('EDUCATIONAL ATTAINMENT','state', False)

# 2019 data #

data_2019 = MigrationData(2019)
data_2019.load_dframe()


race_data_2019 = data_2019.get_race_group_data(False)
ea_data_2019 = data_2019.get_key_data('EDUCATIONAL ATTAINMENT','state', False)

ea_data_2019

temp_df = ea_data_2019

(temp_df.iloc[:,1:len(temp_df)].sum()/sum(temp_df.iloc[:,1:len(temp_df)].sum()) ) * 100

def get_dataframe_of_sums_of_columns(start_year,end_year):
    sum_dict = {}
    temp_df = {2010:ea_data_2010,2011:ea_data_2011,2012:ea_data_2012,2013:ea_data_2013
             ,2014:ea_data_2014,2015:ea_data_2015,2016:ea_data_2016,2017:ea_data_2017
            , 2018:ea_data_2018, 2019:ea_data_2019}
    for i in range(start_year,end_year+1):
        sum_dict[str(i)+'_sum'] = (temp_df[i].iloc[:,1:len(temp_df[i])].sum()/sum(temp_df[i].iloc[:,1:len(temp_df[i])].sum()) ) * 100
        sum_dict[str(i)+'_sum'].reset_index(drop=True, inplace=True)

#     print(series_list)
    
    df = pd.concat(sum_dict,
               axis = 1,ignore_index=True)
#     df.set_index(['All with some error','Less than high school grad',
#                  'High school graduate including equivalency','Some college or associate\'s degree',
#                  'Bachelor\'s degree','Grad or professional degree'])
#     print(df)
    return df, sum_dict.keys()
        
index = ['Less than high school grad',
                 'High school graduate including equivalency','Some college or associate\'s degree',
                 'Bachelor\'s degree','Grad or professional degree']
df,column_names = get_dataframe_of_sums_of_columns(2010,2019)
column_names = list(column_names) + ['Education Level']
# print(column_names)

df['Education Level'] = index

df = df.set_axis(column_names, axis=1, inplace=False)
df = df.set_index('Education Level')
df
# (ea_data_2013.sum())
# f = plt.plot(range(len(ea_data_2019.sum())),ea_data_2019.sum())
# 17910.0-(310.0+3339.0+6538.0+3852.0+3733.0)

df

pip install plotly

import plotly.graph_objects as go

plt.pie(df['2010_sum'],explode= [0.04]*5,colors=('xkcd:baby blue','xkcd:aquamarine','xkcd:bright blue','xkcd:hot pink','xkcd:lavender'),shadow = True,labels = ['<hi-skl','hi-skl grd','clg deg','bach deg','grad deg'],autopct='%1.1f%%',  startangle=0)
plt.title('Fraction of education groups 2019')

centre_circle = plt.Circle((0, 0), 0.45, fc='white')
# plt.get_cmap('bwr')
fig = plt.gcf()

fig.gca().add_artist(centre_circle)

plt.pie(df['2019_sum'],explode= [0.04]*5,colors=('xkcd:purple','xkcd:blue', 'xkcd:green','xkcd:orange','red'),shadow = True,labels = ['<hi-skl','hi-skl grd','clg deg','bach deg','grad deg'],autopct='%1.1f%%',  startangle=0)#, labels = x_tags,shadow = True)
plt.title('Fraction of education groups 2019')

centre_circle = plt.Circle((0, 0), 0.45, fc='white')
fig = plt.gcf()

fig.gca().add_artist(centre_circle)
# pylab.axes().set_ylabel('')

df['2019_sum']

# df.T.columns
# plt.plot(df.columns,df.T[['Less than high school grad']])
# plt.plot(df.columns,df.T[['High school graduate including equivalency']])
# plt.plot(df.columns,df.T[['Some college or associate\'s degree']])
# plt.plot(df.columns,df.T[['Bachelor\'s degree']])
# plt.plot(df.columns,df.T[['Grad or professional degree']])
x_tags = []
for i in range(2010,2020):
    x_tags.append('\''+str(i)[2:4])

from matplotlib.pylab import subplots
fig,axs=subplots(3,2) # 2-rows, 3-column
axs[0][0].plot(x_tags,df.T[['Less than high school grad']],'r-o')
axs[0][0].title.set_text('Less than high school grad')
axs[0][0].set_facecolor('xkcd:light grey')
# axs[0][0].set_xlabel('Year')

axs[0][1].plot(x_tags,df.T[['High school graduate including equivalency']],'g--s')
axs[0][1].title.set_text('High school grad including equivalency')
axs[0][1].set_facecolor('xkcd:light grey')
# axs[0][1].set_xlabel('Year')

axs[1][0].plot(x_tags,df.T[['Some college or associate\'s degree']],'b-.')
axs[1][0].title.set_text('Some college or associate\'s degree')
axs[1][0].set_facecolor('xkcd:light grey')
# axs[1][0].set_xlabel('Year')

axs[1][1].plot(x_tags,df.T[['Bachelor\'s degree']],'y-o')
axs[1][1].title.set_text('Bachelor\'s degree')
axs[1][1].set_facecolor('xkcd:light grey')
# axs[1][1].set_xlabel('Year')

axs[2][0].plot(x_tags,df.T[['Grad or professional degree']],'k-*')
axs[2][0].title.set_text('Grad or professional degree')
axs[2][0].set_facecolor('xkcd:light grey')
# axs[2][0].set_xlabel('Year')

axs[2][1].axis('off')
# axs[4].set_xlabel('Time')

# plt.subplots_adjust(bottom=-0.9,top=0.9)
# fig.show()

fig.suptitle('Trends of percentage Migration on the basis of Education groups vs Year') 
fig.tight_layout()

# axs[0][0].plot(x_tags,df.T[['Less than high school grad']],'r-o')

# fig = plt.plot(x_tags,df.T[['Less than high school grad']],'r-o')
fig = plt.plot(x_tags,df.T[['Grad or professional degree']],'k-*')
plt.title('Grad or professional degree',fontweight='bold')
# plt.set_facecolor('xkcd:light grey')
plt.xlabel('Year',fontweight='bold')
plt.ylabel('Percentage Population',fontweight='bold')
ax = plt.axes()
ax.set_facecolor('xkcd:light grey')

f = (df.T).plot()
f.legend(['<hi-skl','hi-skl grd','clg deg','bach deg','grad deg'])
# ylim(range(0,30,5))

# df.plot.scatter(y='2010_sum',use_index=True)
# df.columns
df.reset_index().plot(x='Education Level', y='2019_sum')

race_data_2010
#

def get_dataframe_of_sums_of_columns(start_year,end_year):
    sum_dict = {}
    temp_df = {2010:race_data_2010,2011:race_data_2011,2012:race_data_2012,2013:race_data_2013
             ,2014:race_data_2014,2015:race_data_2015,2016:race_data_2016,2017:race_data_2017
            , 2018:race_data_2018, 2019:race_data_2019}
    for i in range(start_year,end_year+1):
        sum_dict[str(i)] = (temp_df[i].iloc[:,0:len(temp_df[i])].sum()/sum(temp_df[i].iloc[:,0:len(temp_df[i])].sum()) ) * 100
        sum_dict[str(i)].reset_index(drop=True, inplace=True)

#     print(series_list)
    
    df = pd.concat(sum_dict,
               axis = 1,ignore_index=True)
    return df, sum_dict.keys()
        
index = ['White','Black or African American','Hipanic or Latino','Asian','Other']
df,column_names = get_dataframe_of_sums_of_columns(2010,2019)
column_names = list(column_names) + ['Race']

df['Race'] = index

df = df.set_axis(column_names, axis=1, inplace=False)
df = df.set_index('Race')

df

import squarify
# plot the data using squarify
# print(df.T.iloc[0,0])
lbl = [df.T.columns[i] + '\n'+ str('{:5.2f}'.format(df.T.iloc[-1,i]))+'%' for i in range(len(df.T.columns))]
squarify.plot(sizes=df['2010'], label=lbl, alpha=0.6, color=('xkcd:baby blue','xkcd:green','xkcd:royal purple','xkcd:hot pink','xkcd:light pink'))
# squarify.title('Race migration data 2019')
# squarify.axes('off')

import squarify
# plot the data using squarify
# print(df.T.iloc[0,0])
lbl = [df.T.columns[i] + '\n'+ str('{:5.2f}'.format(df.T.iloc[-1,i]))+'%' for i in range(len(df.T.columns))]
squarify.plot(sizes=df['2019'], label=lbl, alpha=0.6, color=('xkcd:baby blue','xkcd:green','xkcd:royal purple','xkcd:hot pink','xkcd:light pink'))
# squarify.title('Race migration data 2019')
# squarify.axes('off')

plt.plot(df.T['White'])