#!/usr/bin/env python
# coding: utf-8

# # Data Visualization: Trump's Winning Rate
# This report provides detailed facts about Trump's Winning Rate and its correlation between economics indicators, both at national level and at state level

# In[5]:


import pandas as pd
import datetime
import time
import matplotlib.pyplot as plt
import matplotlib.dates as dt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from matplotlib import cm
import numpy as np
import math


# ## 1. Trump vs. Biden Winning Rate by Time

# In[6]:


pnt = pd.read_csv('presidential_national_toplines_2020.csv')
pnt['date'] = pnt['modeldate'].apply(lambda x: datetime.datetime(int(x.split('/')[2]),int(x.split('/')[0]),int(x.split('/')[1])))
date = pnt['date']
y1 = pnt['ecwin_inc']
y2 = pnt['ecwin_chal']
pnt_win=pd.DataFrame({'date': date, 'Trump': y1, 'Biden': y2})


# In[7]:


import seaborn as sns
fig, ax = plt.subplots(figsize=(14, 4))
df = pnt_win
y = [df['Trump'].tolist(),df['Biden']-df['Trump']]
pal = sns.color_palette("Set1")
ax.stackplot(df['date'], y ,labels=['Trump','Biden'], colors=pal, alpha=0.4 )
ax.legend(loc='upper left')

date_form = DateFormatter("%m-%d")
ax.xaxis.set_major_formatter(date_form)
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
plt.show()


# In[8]:


fig, ax = plt.subplots(figsize=(14, 4))
df = pnt_win
# Add x-axis and y-axis
ax.plot(df['date'],df['Trump'], color='red', label = 'Trump Winning Rate')
ax.plot(df['date'],df['Biden'],color='darkblue', label = 'Biden Winning Rate', linestyle='dashed')
# Set title and labels for axes
ax.set(xlabel="date",
       ylabel="Winning rate of the election 2020",
       title="Trump vs. Biden")
# Define the date format
date_form = DateFormatter("%m-%d")
ax.xaxis.set_major_formatter(date_form)
# Ensure a major tick for each week using (interval=1) 
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
plt.legend()
plt.show()


# * Trump's winning rate has a declining trend and the winning rate gap between Biden and Trump is enlarging since the beginning of September

# ## 2. Trump's Winning Rate Changes over Time

# In[9]:


pnt_diff = pnt_win.set_index('date').sort_values(by='date').diff().dropna().reset_index()


# In[10]:


fig, ax = plt.subplots(figsize=(14, 4))
df = pnt_diff

# Add x-axis and y-axis
ax.scatter(df['date'],df['Trump'],c= df['Trump'].apply(lambda x: math.floor(-10000*x)))
ax.plot(df['date'], df['Trump'],color='grey')
ax.plot(df['date'],[0]*132,color='lightblue')

# Set title and labels for axes
ax.set(xlabel="date", ylabel="Daily changes in winning rate",title="Variation in winning rate: Trump")

# Define the date format
date_form = DateFormatter("%m-%d")
ax.xaxis.set_major_formatter(date_form)

# Ensure a major tick for each week using (interval=1) 
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))

plt.show()


# * Trump's winning rate fluctuate a lot from June to August: There are large jumps and drops.
# * However, since the beginning of September, the fluctuation is smaller and the winning rate drops for most of the times.

# ## 3. Trump's Winning Rate at State Level 

# In[11]:


us_state_abbrev = {'Alabama': 'AL', 'Alaska': 'AK','American Samoa': 'AS','Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA','Colorado': 'CO','Connecticut': 'CT', 'Delaware': 'DE','District of Columbia': 'DC','Florida': 'FL',
    'Georgia': 'GA','Guam': 'GU','Hawaii': 'HI','Idaho': 'ID','Illinois': 'IL','Indiana': 'IN','Iowa': 'IA','Kansas': 'KS','Kentucky': 'KY','Louisiana': 'LA',
    'Maine': 'ME','Maryland': 'MD','Massachusetts': 'MA','Michigan': 'MI','Minnesota': 'MN','Mississippi': 'MS','Missouri': 'MO',
    'Montana': 'MT','Nebraska': 'NE','Nevada': 'NV','New Hampshire': 'NH','New Jersey': 'NJ','New Mexico': 'NM','New York': 'NY',
    'North Carolina': 'NC','North Dakota': 'ND','Northern Mariana Islands':'MP','Ohio': 'OH','Oklahoma': 'OK','Oregon': 'OR','Pennsylvania': 'PA',
    'Puerto Rico': 'PR','Rhode Island': 'RI','South Carolina': 'SC','South Dakota': 'SD', 'Tennessee': 'TN','Texas': 'TX','Utah': 'UT','Vermont': 'VT','Virgin Islands': 'VI','Virginia': 'VA',
    'Washington': 'WA','West Virginia': 'WV','Wisconsin': 'WI', 'Wyoming': 'WY'
}


# In[12]:


pst = pd.read_csv('presidential_state_toplines_2020.csv')
pst['date'] = pst['modeldate'].apply(lambda x:datetime.datetime(int(x.split('/')[2]),int(x.split('/')[0]),int(x.split('/')[1])))
pst['code'] = pst['state'].apply(lambda x: 'no' if '-' in x else us_state_abbrev[x])
pst = pst[pst['code']!='no']


# ### 3.1 Winning Rate by State-Month

# In[14]:


import plotly.graph_objects as go

pst_cat = pst[['date','winstate_inc','code']]
datevar = pst_cat['date'].drop_duplicates()[0:-1:30]
for date in datevar:
    pst_sub = pst_cat[pst_cat['date'] == date]
    fig = go.Figure(data=go.Choropleth(
    locations=pst_sub['code'], # Spatial coordinates
    z = pst_sub['winstate_inc'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Reds',
    colorbar_title = "Winning Rate",))

    fig.update_layout(
        title_text = 'Trump winning rate by state:'+ str(date.date()),
        geo_scope='usa', # limite map scope to USA
    )
    fig.show()


# * From the above graphs, we can see the Trump's winning rates by state and month
# * The winning rates are particularly low in Northeast and West coast while higher in the middle states

# ### 3.2 States with the Largest Uncertainties

# In[15]:


pst_cat = pst[['date','winstate_inc','code']]
datevar = pst_cat['date'].drop_duplicates()[0:-1:30]
for date in datevar:
    pst_sub = pst_cat[pst_cat['date'] == date]
    fig = go.Figure(data=go.Choropleth(
    locations=pst_sub['code'], # Spatial coordinates
    z = -abs(pst_sub['winstate_inc']-0.5), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Reds',
    colorbar_title = "Uncertainty Level",))

    fig.update_layout(
        title_text = 'Uncertainties by state:'+ str(date.date()),
        geo_scope='usa', # limite map scope to USA
    )
    fig.show()


# * This graphs show the uncertainty levels of Trump winning of each states by month
# * OH, GA, and IA are the three states that Trump's winning rate is close to 50%

# ### 3.3 Correlation between Trump's State level Winning Rate with National level Winning Rate

# In[16]:


pst_cat = pst_cat.set_index(['code','date'])
pst_cat = pst_cat.sort_values(by = ['code','date'])
pst_diff = pst_cat.diff().dropna()
pst_diff = pst_diff.reset_index()


# In[17]:


pst_pnt_diff_merge = pst_diff.merge(pnt_diff, on='date')
pst_pnt_merge = pst_cat.reset_index().merge(pnt_win, on='date')


# In[18]:


pst_pnt_corr = pst_pnt_merge.groupby('code')['winstate_inc','Trump'].corr().reset_index()


# In[19]:


pst_pnt_corr = pst_pnt_corr[pst_pnt_corr['level_1']=='Trump'][['code','winstate_inc']]


# In[20]:


fig = go.Figure(data=go.Choropleth(
locations=pst_pnt_corr['code'], # Spatial coordinates
z = pst_pnt_corr['winstate_inc'].astype(float), # Data to be color-coded
locationmode = 'USA-states', # set of locations match entries in `locations`
colorscale = 'blues',
colorbar_title = "Correlation with State Winning Rate",))

fig.update_layout(
    title_text = "Correlation between Trump's State level Winning Rate with National level Winning Rate",
    geo_scope='usa', # limite map scope to USA
    )
fig.show()


# * The correlation is the highest in PA, UT, CO: If Trump wins these three states, he is likely to win the national election.
# * The correlation is the lowest in KY: Trump is more likely to win the national election if he lost in KY.

# ## 4. Comovement between Trump's Winning Rate and Economic Indicators

# In[21]:


ei = pd.read_csv('economic_index.csv')
ei['date'] = ei['modeldate'].apply(lambda x: datetime.datetime(int(x.split('/')[2]),int(x.split('/')[0]),int(x.split('/')[1]))  )


# In[22]:


idx1 = ei[ei['indicator']=='S&P 500'].set_index('date').rename(columns = {'current_zscore':'S&P 500'})['S&P 500']
idx2 = ei[ei['indicator']=='Personal consumption expenditures'].set_index('date').rename(columns = {'current_zscore':'Personal consumption expenditures'})['Personal consumption expenditures']
idx3 = ei[ei['indicator']=='Industrial production'].set_index('date').rename(columns = {'current_zscore':'Industrial production'})['Industrial production']
idx4 = ei[ei['indicator']=='Nonfarm payrolls'].set_index('date').rename(columns = {'current_zscore':'Nonfarm payrolls'})['Nonfarm payrolls']
idx5 = ei[ei['indicator']=='Consumer price index'].set_index('date').rename(columns = {'current_zscore':'Consumer price index'})['Consumer price index']
idx6 = ei[ei['indicator']=='Real disposable personal income'].set_index('date').rename(columns = {'current_zscore':'Real disposable personal income'})['Real disposable personal income']
idx = ei[ei['indicator']=='Average of all six indicators'].set_index('date').rename(columns = {'current_zscore':'Average of all six indicators'})['Average of all six indicators']
idx_merge = pd.merge(idx1,idx2,on='date').merge(idx3, on='date').merge(idx4, on='date').merge(idx5, on='date').merge(idx6, on='date').merge(idx, on='date')
idx_merge = idx_merge.reset_index()


# ### 4.1 National Level Comovement

# In[23]:


fig, ax = plt.subplots(figsize=(14, 4))

df = pnt_win
ax.scatter(df['date'],
       df['Trump'],
       c= -df['Trump'])
ax.plot(df['date'],
       df['Trump'],
       color='blue')

ax2=ax.twinx()
df = idx_merge
ax2.plot(df['date'],
       df['S&P 500'],
       color='green')
ax2.scatter(df['date'],
       df['S&P 500'],
       c= -df['S&P 500'])

# Set title and labels for axes
ax.set_ylabel("S&P 500", color="green")
ax2.set_ylabel("Trump winning rate", color="blue")
ax.set(title = "Trump winning rate vs. S&P 500")

# Define the date format
date_form = DateFormatter("%m-%d")
ax.xaxis.set_major_formatter(date_form)

# Ensure a major tick for each week using (interval=1) 
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))

plt.show()


# * There are some comovements between Trump's winning rate and S&P 500 before the end of September
# * The correlation between Trump's winning rate and S&P 500 becomes negative since around 9/29/2020

# In[24]:


fig, ax = plt.subplots(figsize=(14, 4))

df = pnt_win
ax.scatter(df['date'],
       df['Trump'],
       c= -df['Trump'])
ax.plot(df['date'],
       df['Trump'],
       color='blue')

ax2=ax.twinx()
df = idx_merge
ax2.plot(df['date'],
       df['Average of all six indicators'],
       color='green')
ax2.scatter(df['date'],
       df['Average of all six indicators'],
       c= -df['Average of all six indicators'])

# Set title and labels for axes
ax.set_ylabel("Average of all six indicators", color="green")
ax2.set_ylabel("Trump winning rate", color="blue")
ax.set(title = "Trump winning rate vs. Average of all six indicators")

# Define the date format
date_form = DateFormatter("%m-%d")
ax.xaxis.set_major_formatter(date_form)

# Ensure a major tick for each week using (interval=1) 
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))

plt.show()


# * There are some comovements between Trump's winning rate and average of indicators before the mid August
# 

# ### 4.2 Comovement between Trump's State Level Winning Rate and Economic Indicators

# In[25]:


pst_merge = pst_cat.reset_index().merge(pnt_win, on = 'date').merge(idx1, on ='date')

pst_corr = pst_merge.groupby('code')['winstate_inc','S&P 500'].corr().reset_index()
pst_corr = pst_corr[pst_corr['level_1']=='S&P 500'][['code','winstate_inc']]


# In[26]:


fig = go.Figure(data=go.Choropleth(
locations=pst_sub['code'], # Spatial coordinates
z = pst_corr['winstate_inc'].astype(float), # Data to be color-coded
locationmode = 'USA-states', # set of locations match entries in `locations`
colorscale = 'blues',
colorbar_title = "Correlation with S&P 500",))

fig.update_layout(
    title_text = 'Trump winning rate correlation with stock market',
    geo_scope='usa', # limite map scope to USA
    )
fig.show()


# * The states whose winning rates are highly positively correlated with S&P 500 are: OH, WI, OR...
# * The states whose winning rates are highly negatively correlated with S&P 500 are: NM, OK, KS...
# * States such as MD are not likely to be affected by stock market

# In[27]:


pst_merge = pst_cat.reset_index().merge(pnt_win, on = 'date').merge(idx, on ='date')
pst_corr = pst_merge.groupby('code')['winstate_inc','Average of all six indicators'].corr().reset_index()
pst_corr = pst_corr[pst_corr['level_1']=='Average of all six indicators'][['code','winstate_inc']]
fig = go.Figure(data=go.Choropleth(
locations=pst_sub['code'], # Spatial coordinates
z = pst_corr['winstate_inc'].astype(float), # Data to be color-coded
locationmode = 'USA-states', # set of locations match entries in `locations`
colorscale = 'blues',
colorbar_title = "Correlation with Average of all six indicators",))

fig.update_layout(
    title_text = 'Trump winning rate correlation with economics indicators',
    geo_scope='usa', # limite map scope to USA
    )
fig.show()


# * The states whose winning rates are highly positively correlated with economics indicators are: OR, OH, CT...
# * The states whose winning rates are highly negatively correlated with economics indicators: NM, OK, KS...
# * States such as NE, VT, WY are not likely to be affected by economics indicators
