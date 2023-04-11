#!/usr/bin/env python
# coding: utf-8

# In[53]:


print("_"*22,"\n|   Keep Track Your   |\n|     Competitors     |\n|   To Secure Your    |\n|      Business       |\n|"+"_"*21+"|")
a = int(input("\nKlik 1 untuk melanjutkan> "))


# In[4]:


if a == 1:
    print("\nSilahkan pilih menu di bawah ini\n")
    print("-"*10,"MENU","-"*10)
    print(" [1]  Show Data")
    print(" [2]  Sales Performance")
    print(" [3]  Agent Performance")
    print(" [4]  Supplier Analysis")
    print(" [5]  Segment Analysis")
    print(" [99] Exit\n")
else:
    print("Anda keluar dari system")
b=int(input("Enter number of your choice: "))


# In[5]:


#Import Library
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import datetime
import scipy.stats as stats
import warnings


# # Data

# In[15]:


# Import Data
data = pd.read_csv("D:/TRAINING/CISCO/Sales_wireless.csv", sep=";", encoding="unicode_escape")
data.info()
#Data
data['Month']=data['Date'].apply(lambda x: datetime.datetime.strptime(x, '%d/%m/%Y').strftime('%m/%Y'))
data['Day']=data['Date'].apply(lambda x: datetime.datetime.strptime(x, '%d/%m/%Y').strftime('%d/%m/%Y'))
data['Year']=data['Date'].apply(lambda x: datetime.datetime.strptime(x, '%d/%m/%Y').strftime('%Y'))
data


# # Sales Performance

# In[24]:


#Data
data2=data
data2['Day']=data2['Date'].str[0:2]
data2['Month']=data2['Date'].str[3:5]

#Plot
data2.groupby(['Month','Day'])['Sales_Amount'].sum().plot(marker='o',color='indianred')
plt.title('Time Series Sales Amount',loc='center',pad=30, fontsize=15, color='black')
plt.xlabel('Date', fontsize = 12)
plt.ylabel('Sales Amount',fontsize = 12)
plt.grid(color='darkgray', linestyle=':', linewidth=0.5)
plt.ylim(ymin=0)
plt.legend(loc='upper center', bbox_to_anchor=(0.95, 1), shadow=True, ncol=1)
plt.gcf().set_size_inches(20, 10)
plt.tight_layout()

#Plot
data.groupby(['Day', 'Month'])['Sales_Amount'].sum().unstack().plot(marker='x',cmap='cool')
plt.title('Sales Amount',loc='center',pad=30, fontsize=15, color='black')
plt.xlabel('Date', fontsize = 12)
plt.ylabel('Sales Amount',fontsize = 12)
plt.grid(color='darkgray', linestyle=':', linewidth=0.5)
plt.ylim(ymin=0)
plt.legend(loc='upper center', bbox_to_anchor=(0.96, 1), shadow=True, ncol=1)
plt.gcf().set_size_inches(20, 10)
plt.tight_layout()


# # Agent Performance

# In[27]:


#Data
data3=data
data3['Day']=data3['Date'].str[0:2]
data3['Month']=data3['Date'].str[3:5]

#Plot
data3.groupby(['Month','Day','Agent'])['Sales_Amount'].sum().unstack().plot.area(cmap='RdPu')
plt.title('Sales Amount by Agent',loc='center',pad=30, fontsize=18, color='black')
plt.xlabel('Date', fontsize = 14)
plt.ylabel('Sales Amount',fontsize = 14)
plt.grid(color='darkgray', linestyle=':', linewidth=0.5)
plt.ylim(ymin=0)
plt.legend(loc='upper center', bbox_to_anchor=(0.95, 1), shadow=True, ncol=1)
plt.gcf().set_size_inches(20, 10)
plt.tight_layout()

#Data
datagroup=data.groupby(['Month','Agent'])[['Sales_Amount']].sum()
datagroup

#Plot
data.groupby(['Month','Agent'])['Sales_Amount'].sum().unstack().plot(marker='d', cmap='magma')
plt.title('Sales Amount by Agent',loc='center',pad=30, fontsize=15, color='black')
plt.xlabel('Date', fontsize = 12)
plt.ylabel('Sales Amount',fontsize = 12)
plt.grid(color='darkgray', linestyle=':', linewidth=0.5)
plt.ylim(ymin=0)
plt.legend(loc='upper center', bbox_to_anchor=(0.95, 1), shadow=True, ncol=1)
plt.gcf().set_size_inches(20, 10)
plt.tight_layout()


# # Agent Analysis

# In[34]:


#Data
datajoin=data[['Sales_Amount','Cost','Net_Earnings','Profit_Contribution_Ratio','Agent']]

#Plot
with sns.axes_style('ticks'):
    plot=sns.pairplot(datajoin, hue='Agent', 
                      hue_order=['STKEVON','STKWAN','STKYOSEF','STKANSON', 'Wireless Service'], 
                      markers=['+','o','s','D','x'], 
                      diag_kind='kde', height=3, diag_kws=dict(shade=True))
    
    for i,j in zip(*np.triu_indices_from(plot.axes, 1)):
        plot.axes[i,j].set_visible(False)
plt.show()

#Plot
sns.scatterplot(data=data, x='Cost', y='Sales_Amount', hue = 'Agent', style = 'Agent')
plt.gcf().set_size_inches(20, 10)

#Plot
g = sns.FacetGrid(data, col="Agent", col_wrap=3, hue="Agent")
b = g.map_dataframe(sns.scatterplot, x="Cost", y="Sales_Amount")
g.add_legend()

#Data
x=data['Profit_Contribution_Ratio']*100
y=data['Sales_Amount']

#Plot
warnings.filterwarnings('ignore')
sns.set(style='ticks')
sns.jointplot(x, y, kind='reg', xlim=(0, 0.8), ylim=(0, 2000), height=7, stat_func=stats.pearsonr)


# # Supplier Analysis

# In[37]:


databar = data.groupby(['Company'])[['Sales_Amount']].sum()
dataline = data.groupby(['Company'])[['Net_Earnings']].sum()
databar
dataline
databar['Net_Earnings']=dataline
databar2=databar.sort_values(['Sales_Amount'],ascending=False)
databar2.style.highlight_max(color = 'red', axis=0)


# In[35]:


#Data
datasup=data.groupby(['Company'])[['Profit_Contribution_Ratio']].sum()
datasup.sort_values(['Profit_Contribution_Ratio'], ascending=False).head(10)


# In[51]:


fig2, ax = plt.subplots(figsize=(12,8))
ax2 = ax.twinx()
df2 = databar2.plot(kind='bar', y='Sales_Amount', ax=ax2,stacked=False,alpha = .15)
df2 = databar2.plot(kind='line',y='Net_Earnings', ax=ax2,marker='d', markersize=12)
ax.set_xlabel('Company')
ax.set_title('Sales Amount & Net Earnings by Company')
plt.gcf().set_size_inches(27, 8)

# Data
dfstack = data.groupby(['Company'])[['Profit_Contribution_Ratio']].mean()
dfstack.style.highlight_max(color = 'red', axis=0)
dfnew= {'Company': ['AT&T','Amazon','Apple','Castify','EY Cell','Fun TV','H20','HomeX','Huawei','InCell ','LycaMobile','Motorola','Samsung',
   'SanDisk','Shein','SimpleMobile','TCL ','TMobile','Temu','UltraMobile','Unblock','XiaoMi']}
dfnew=pd.DataFrame(dfnew)
dfstack['Company']=dfnew
#Plot
fig, ax = plt.subplots(figsize=(16,10), dpi= 80)
ax.vlines(x=dfnew.Company, ymin=0, ymax=dfstack.Profit_Contribution_Ratio*100, color='firebrick', alpha=0.7, linewidth=2)
ax.scatter(x=dfnew.Company, y=dfstack.Profit_Contribution_Ratio*100, s=75, color='firebrick', alpha=0.7)
ax.set_title('Lollipop Chart for Average Profit Contribution Ratio (%)', fontdict={'size':22})
ax.set_ylabel('Average Profit Contribution Ratio (%)')
ax.set_xticks(dfnew.Company)
plt.gcf().set_size_inches(23, 10)


# Prepare Data
dataApple=data[data['Company']=='Apple'][['Agent','Sales_Amount','Category']]
dataApple1=dataApple.groupby(['Agent'])[['Sales_Amount']].sum()

#Plot
dataApple1.plot(kind='pie', subplots=True, figsize=(8, 8))
plt.title("Pie Chart of Vehicle Class - Bad")
plt.ylabel("")
plt.show()

# Prepare Data
dataApple2=dataApple.groupby(['Category'])[['Sales_Amount']].sum()
Category = ['Brand New Phone','Device Repair','Refurbished Phone or Device','Software Service','Tech Accessories','Wireless Service']
Sales = [45020,5240,40518,385,3369,3550]


# Fig Size
fig4, ax = plt.subplots(figsize =(16, 9))
 
# Horizontal Bar Plot
ax.barh(Category,Sales)
 
# Remove axes splines
for s in ['top', 'bottom', 'left', 'right']:
    ax.spines[s].set_visible(False)
 
# Remove x,y Ticks
ax.xaxis.set_ticks_position('none')
ax.yaxis.set_ticks_position('none')
 
# Add padding between axes and labels
ax.xaxis.set_tick_params(pad = 5)
ax.yaxis.set_tick_params(pad = 10)
 
# Add x, y gridlines
ax.grid(b = True, color ='grey',
        linestyle ='-.', linewidth = 0.5,
        alpha = 0.2)
 
# Show top values
ax.invert_yaxis()
 
# Add annotation to bars
for i in ax.patches:
    plt.text(i.get_width()+0.2, i.get_y()+0.5,
             str(round((i.get_width()), 2)),
             fontsize = 10, fontweight ='bold',
             color ='grey')
 
# Add Plot Title
ax.set_title('Sales Amount "Apple Company" by Category',
             loc ='center',fontsize = 14)
 
# Add Text watermark
fig.text(0.9, 0.15, 'Jeeteshgavande30', fontsize = 12,
         color ='grey', ha ='right', va ='bottom',
         alpha = 0.7)
 
# Show Plot
plt.show()



# # Segment Analysis

# In[45]:


dataseg=data.groupby(['Category'])[['Cost']].median()
dataseg.style.highlight_max(color = 'red', axis=0)


# In[46]:


dataseg['Profit_Contribution_Ratio']=data.groupby(['Category'])[['Profit_Contribution_Ratio']].sum()
dataC= {'Category': ['Brand New Phone', 'Device Repair', 'Refurbished Phone or Device', 'Software Service', 'TV Box','Tech Accessories','Wireless Service'],
        'Cost' : [829.0,20.0,135.0,0.0,140.0,4.0,47.0],
        'Profit_Contribution_Ratio': [0.1789,0.3313,0.3238,0.0651,0.0557,0.1898,0.5245]}

df = pd.DataFrame(dataC)
df.style.highlight_max(color = 'red', axis=0)


# In[52]:


#Prepare Data
x=df['Cost']
y=df['Profit_Contribution_Ratio']
l=df['Category']

#Plot
fig3, ax = plt.subplots(figsize=(12,8))
ax.scatter(x[0], y[0], marker='s', s=178, color='r', label=l[0])
ax.scatter(x[1], y[1], marker='s', s=331, color='grey', label=l[1])
ax.scatter(x[2], y[2], marker='s', s=323, color='blue', label=l[2])
ax.scatter(x[3], y[3], marker='s', s=65, color='y', label=l[3])
ax.scatter(x[4], y[4], marker='s', s=55, color='green', label=l[4])
ax.set_ylabel('Profit Contribution Ratio')
ax.set_title('Cost vs Profit Contribution Ratio')
ax.set_xlabel('Cost')
ax.legend(loc='upper right',bbox_to_anchor=(1,1))
plt.gcf().set_size_inches(10, 10)

#Plot
sns.swarmplot(x="Category", y="Profit_Contribution_Ratio", data=data)
plt.ylim(ymin=0, ymax=0.010)
plt.gcf().set_size_inches(15, 8)

#Prepare Data
datanew=data.groupby(['Category'])[['Sales_Amount','Cost']].median()

#Plot
fig2, ax = plt.subplots(figsize=(12,8))
ax2 = ax.twinx()
df3 = datanew.plot(kind='bar', y='Sales_Amount', ax=ax2,color= 'red',stacked=False,alpha = .15)
df3 = datanew.plot(kind='bar',y='Cost', ax=ax2, color = 'lightblue')
ax.set_xlabel('Category')
ax.set_title('Median Sales Amount & Median Cost by Category')
plt.gcf().set_size_inches(17, 8)

