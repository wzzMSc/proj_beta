# %%
import matplotlib.pyplot as plt
import pandas as pd
import os

df = pd.read_csv('data/final.csv',header=0,parse_dates=['ISODate'],index_col='ISODate')

resample_method = '3H'
df_resampled = df.resample(resample_method).mean()


# %%
for x in df_resampled.columns:
    if not os.path.exists("vis/scatter/"+x+'/'):
        os.makedirs("vis/scatter/"+x+'/')

for x in df_resampled.columns:
    for y in df_resampled.columns:
        plt.scatter(df_resampled[x],df_resampled[y],s=0.5)
        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(x+"-"+y)
        plt.savefig("vis/scatter/"+x+'/'+x+"-"+y+".png")
        plt.cla()
        plt.close()

# %%
df_resampled.corr().to_csv('vis/scatter/pearson_r.csv')

df_corr = df_resampled.corr()[df_resampled.corr() >0.6]
corr_index = df_corr.index.tolist()
for x in range(len(df_corr)):
    for y in range(x,len(df_corr)):
        if df_corr.iloc[x,y]>0.6 and df_corr.iloc[x,y]<1:
            print(corr_index[x],'-',corr_index[y],':',df_corr.iloc[x,y])

# %%
