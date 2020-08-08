# %%
import matplotlib.pyplot as plt
import pandas as pd
import os

df = pd.read_csv('data/final.csv',header=0,parse_dates=['ISODate'],index_col='ISODate')

resample_method = '3H'
df_resampled = df.resample(resample_method).mean()

# %%
for x in df_resampled.columns:
    if not os.path.exists("vis/raw_reg/"+x+'/'):
        os.makedirs("vis/raw_reg/"+x+'/')

for y in df_resampled.columns:
    plt.figure(figsize=(150,10))
    plt.plot(df_resampled.index,df_resampled[y])
    plt.xlabel('Date')
    plt.ylabel(y)
    plt.savefig("vis/raw_reg/"+y+'/'+y+'.png',dpi=130)
    plt.cla()
    plt.close()