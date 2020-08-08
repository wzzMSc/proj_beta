# %%
import pandas as pd
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from dateutil import parser
from datetime import date
from os import makedirs

prediction_targets = ['BEAMS','BEAMT','BEAMT2']
downtime_attrs = ['StartDate','SecondsSinceUp','EndDate','LastedSeconds']
df = pd.read_csv('data/final.csv',header=0,parse_dates=['ISODate'])

cycles_Dates = [
 ['12 Apr 2016','20 May 2016'],
 ['28 Jun 2016','29 Jul 2016'],
 ['13 Sep 2016','28 Oct 2016'],
 ['15 Nov 2016','16 Dec 2016'],
 ['14 Feb 2017','30 Mar 2017'],
 ['02 May 2017','01 Jun 2017'],
 ['19 Sep 2017','27 Oct 2017'],
 ['14 Nov 2017','20 Dec 2017'],
 ['06 Feb 2018','25 Mar 2018'],
 ['17 Apr 2018','18 May 2018'],
 ['11 Sep 2018','26 Oct 2018'],
 ['13 Nov 2018','18 Dec 2018'],
 ['05 Feb 2019','29 Mar 2019'],
 ['04 Jun 2019','19 Jul 2019'],
 ['10 Sep 2019','25 Oct 2019'],
 ['12 Nov 2019','20 Dec 2019']
]

for x in prediction_targets:
    if not os.path.exists("vis/downtime/"+x+'/'):
        os.makedirs("vis/downtime/"+x+'/')

# # %%
# for target in prediction_targets:
#     for cycle in cycles_Dates:
#         target_threshold = df[(df['ISODate']>=cycle[0]) & (df['ISODate']<cycle[1])][target].max()*0.8
#         first_up=0
#         is_down = 0
#         up_start = 0
#         down_start = 0
#         list_df,l=[],[]
#         df_list = df[(df['ISODate']>=cycle[0]) & (df['ISODate']<cycle[1])].to_dict('records')
#         for doc in df_list:
#             if first_up == 0:
#                 if int(doc[target])>=target_threshold:
#                     first_up=1
#                     up_start=int(doc['SEC_1970'])
#             else:
#                 if is_down==0:
#                     if int(doc[target])<target_threshold:
#                         is_down=1
#                         down_start=int(doc['SEC_1970'])
#                         l.append(doc['ISODate'])
#                         l.append(down_start-up_start)
#                 else:
#                     if int(doc[target])>=target_threshold:
#                         is_down=0
#                         l.append(doc['ISODate'])
#                         l.append(int(doc['SEC_1970']) - down_start)
            
#             if len(l)==len(downtime_attrs):
#                 list_df.append(l)
#                 l=[]
#         df_down = pd.DataFrame(list_df,columns=downtime_attrs)
#         df_down.to_csv('vis/downtime/Downtime_'+target+'.csv',mode='a',header=False)

# %%
for target in prediction_targets:
    df_target = pd.read_csv('vis/downtime/Downtime_'+target+'.csv',names=downtime_attrs)
    df_target['StartDate'] = pd.to_datetime(df_target['StartDate'])
    df_target.set_index('StartDate')
    plt.figure(figsize=(150,10))
    plt.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%Y-%m-%d", tz=None))
    plt.gca().xaxis.set_major_locator(matplotlib.dates.DayLocator(bymonthday=None, interval=20, tz=None))
    plt.plot(df_target['StartDate'],df_target['LastedSeconds'])
    plt.xlabel('StartDate')
    plt.ylabel('LastedSeconds')
    plt.savefig("vis/downtime/"+target+'/'+target+'.png',dpi=130)
    plt.cla()
    plt.close()

# %%
for x in prediction_targets:
    if not os.path.exists("vis/downtime_seq/"+x+'/'):
        os.makedirs("vis/downtime_seq/"+x+'/')

for target in prediction_targets:
    df_target = pd.read_csv('vis/downtime/Downtime_'+target+'.csv',names=downtime_attrs)
    df_target['i'] = [x for x in range(1,len(df_target)+1)]
    plt.figure(figsize=(150,10))
    plt.plot(df_target['i'],df_target['LastedSeconds'])
    plt.xlabel('Sequential order')
    plt.ylabel('LastedSeconds')
    plt.savefig("vis/downtime_seq/"+target+'/'+target+'.png',dpi=130)
    plt.cla()
    plt.close()
    df_target.to_csv('vis/downtime/Downtime_seq_'+target+'.csv')

# %%
for x in prediction_targets:
    if not os.path.exists("vis/downtime_seconds_since_up/"+x+'/'):
        os.makedirs("vis/downtime_seconds_since_up/"+x+'/')

for target in prediction_targets:
    df_target = pd.read_csv('vis/downtime/Downtime_seq_'+target+'.csv',header=0)
    max = df_target['SecondsSinceUp'].max()
    bins = [max*x*0.005 for x in range(0,201)]
    labels = [str(int(bins[i]))+'-'+str(int(bins[i+1])) for i in range(0,len(bins)-1)]
    df_target['Bin'] = pd.cut(df_target['SecondsSinceUp'],bins=bins,labels=labels)
    labels_count = [list(df_target['Bin'].values).count(labels[i]) for i in range(len(labels))]
    plt.figure(figsize=(250,10))
    plt.bar(labels,labels_count)
    plt.xlabel('Seconds since up')
    plt.ylabel('Number of incidents')
    plt.savefig("vis/downtime_seconds_since_up/"+target+'/'+target+'.png',dpi=130)
    plt.cla()
    plt.close()

# %%
