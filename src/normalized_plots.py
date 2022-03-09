#!/usr/bin/env python
# coding: utf-8

# In[15]:


run MigrationData.py


# In[26]:


data_2019 = MigrationData(2019)
data_2019.load_dframe()
data_2019 = pd.read_csv(data_2019.fname)


# In[27]:


data_2019


# In[17]:


run age_group_analysis.py


# In[18]:


print(age_final)


# In[3]:


import matplotlib.pyplot as plt


# In[22]:


labels=["1 to 17 years",'18 to 24 years','25 to 54 years', '55 years and over']
explode=[0.035,0.035,0.035,0.035]
y=age_final[2019]
plt.figure(figsize=(7,7)) 
textprops = {"fontsize":15}
plt.pie(y,labels=labels,autopct='%1.1f%%',textprops=textprops)
plt.title('Normalized age migration trend in 2019',fontsize='18')
#plt.legend(labels=labels,loc='best')
plt.savefig('normalized_age_pie')


# In[23]:


explode = (0,0)
fig4, ax4 = plt.subplots()
ax4.pie(y, labels=labels, autopct='%1.1f%%', startangle=90)
ax4.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax4.title.set_text("Normalized age migration trend in 2019")
plt.savefig('normalized_age_pie.png')


# In[ ]:





# In[8]:


run sex_group_analysis.py


# In[9]:


print(sex_final)


# In[11]:


labels=['Male','Female']
explode=[0.035,0.035]
y=sex_final[2019]
plt.figure(figsize=(7,7)) 
textprops = {"fontsize":15}
plt.pie(y,labels=labels,explode=explode,autopct='%1.1f%%',textprops=textprops)
plt.title('Normalized sex migration trend',fontsize='18',pad=28)
plt.legend(labels=labels,loc='best')
plt.savefig('normalized_sex_pie')


# In[15]:


explode = (0,0)
fig4, ax4 = plt.subplots()
ax4.pie(y, explode=explode, labels=labels, autopct='%1.1f%%', startangle=90)
ax4.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax4.title.set_text("Normalized Male vs Female Migrants % in 2019")
plt.savefig('normalized_sex_pie.png')


# In[16]:


x_pos=[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019]
y=sex_final.loc['Female']
z=sex_final.loc['Male']
plt.figure(figsize=(7,7)) 
plt.plot(y,'--bo',label='')
plt.plot(z,'--ro',label="")
plt.xticks(x_pos)
#plt.yticks([i for i in range(50,77,3)])
plt.title('Trend of people moving earning in the range $0 to 35k')
plt.ylabel('in % of total people moving')
plt.xlabel('Year')
#plt.savefig('income_trend_0to35k')
y


# In[3]:


run housing_group_analysis.py


# In[4]:


print(housing_final)


# In[41]:


labels=['owner-occupied','renter-occupied']
explode=[0.035,0.035]
y=housing_final[2019]
plt.figure(figsize=(7,7)) 
textprops = {"fontsize":15}
plt.pie(y,labels=labels,explode=explode,autopct='%1.1f%%',textprops=textprops)
plt.title('Normalized Housing Migration Trend for 2019',fontsize='18',pad=28)
plt.legend(labels=labels,loc='best')
plt.savefig('normalized_renter_pie')


# In[12]:


run race_group_analysis.py


# In[13]:


print(race_final)


# In[49]:


labels=['White','Black or African American', 'Hispanic or Latino', 'Asian', 'Other']
explode=[0.035,0.035,0.035,0.035,0.035]
y=race_final[0]
plt.figure(figsize=(7,7)) 
textprops = {"fontsize":15}
plt.pie(y,labels=labels,explode=explode,autopct='%1.1f%%',textprops=textprops)
plt.title('Normalized Race Migration Trend',fontsize='18',pad=28)
plt.legend(labels=labels,loc='best')
#plt.savefig('normalized_race_pie')


# In[75]:



import squarify
# plot the data using squarify
# print(df.T.iloc[0,0]) + '\n'+ str('{:5.2f}'.format(y[i])) +'%'

lbl = [i + '\n'+ str('{:5.2f}'.format((y[i]/y.sum()) *100) ) + '%' for i in y.index]
squarify.plot(sizes=y, label=lbl, alpha=0.6, color=('xkcd:baby blue','xkcd:green','xkcd:royal purple','xkcd:hot pink','xkcd:light pink'))
# squarify.title('Race migration data 2019')
# squarify.axes('off')
# lbl
# (y/y.sum() )*100
plt.axis('off')
plt.savefig('normalized_race_pie')


# In[44]:


run income_group_analysis.py


# In[23]:


print(income_final)


# In[42]:


labels=['0 to 35k dollars','35k to 50k dollars', '50k to 75k dollars', '75k+ dollars']
explode=[0.035,0.035,0.035,0.035]
y=income_final[2019]
plt.figure(figsize=(7,7)) 
textprops = {"fontsize":15}
plt.pie(y,labels=labels,explode=explode,autopct='%1.1f%%',textprops=textprops)
plt.title('Normalized Income Based Migration Trend for 2019',fontsize='18',pad=28)
plt.legend(labels=labels,loc='upper left')
plt.savefig('normalized_income_pie')


# In[1]:


run education_group_analysis.py


# In[2]:


print(education_final)


# In[6]:


plt.pie(education_final[2019],explode= [0.04]*5,colors=('xkcd:baby blue','xkcd:aquamarine','xkcd:bright blue','xkcd:hot pink','xkcd:lavender'),shadow = True,labels = ['less than high school','high school grad','college','bachelors','graduate'],autopct='%1.1f%%',  startangle=0)
plt.title('Normalized Fraction of education groups 2019')

centre_circle = plt.Circle((0, 0), 0.45, fc='white')
# plt.get_cmap('bwr')
fig = plt.gcf()

fig.gca().add_artist(centre_circle)
plt.savefig('normalized_education_pie')


# In[ ]:




