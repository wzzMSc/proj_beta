# %%
import matplotlib.pyplot as plt
import pandas as pd
import os

df = pd.read_csv('data/final.csv',header=0,parse_dates=['ISODate'],index_col='ISODate')

resample_method = '3H'
df_resampled = df.resample(resample_method).mean()



# %%
for x in df_resampled.columns:
    if not os.path.exists("vis/raw_cla/"+x+'/'):
        os.makedirs("vis/raw_cla/"+x+'/')


for x in df_resampled.columns:
    thres = df_resampled[x].max()*0.5
    df_resampled[x][df_resampled[x]<thres] = 0
    df_resampled[x][df_resampled[x]>=thres] = 1

for y in df_resampled.columns:
    plt.figure(figsize=(150,10))
    plt.plot(df_resampled.index,df_resampled[y])
    plt.xlabel('Date')
    plt.ylabel(y)
    plt.savefig("vis/raw_cla/"+y+'/'+y+'.png',dpi=130)
    plt.cla()
    plt.close()