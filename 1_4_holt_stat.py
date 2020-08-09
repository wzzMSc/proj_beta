# %%
import matplotlib.pyplot as plt
import pandas as pd
import os
import seaborn as sns
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error

dir = "vis/stat/05holt/"

df = pd.read_csv('data/final.csv',header=0,parse_dates=['ISODate'],index_col='ISODate')

resample_method = '3H'
df_resampled = df.resample(resample_method).mean()
df_resampled = df_resampled.dropna(axis=0)
df_resampled['i'] = [x for x in range(1,len(df_resampled)+1)]

prediction_targets = ['BEAMS','BEAMT','BEAMT2']

for x in prediction_targets:
    if not os.path.exists(dir+x+'/'):
        os.makedirs(dir+x+'/')

s = int(len(df_resampled)*0.8)
train,test = df_resampled[:s],df_resampled[s:]

for y in prediction_targets:
    sm.tsa.seasonal_decompose(train[y].values,period=8*30).plot(resid=False)
    plt.savefig(dir+y+'/'+y+'_seasonal_decompose.png',dpi=130)
    plt.cla()
    plt.close()

# %%
for y in prediction_targets:
    holt = Holt(train[y].values).fit()
    test['holt'] = holt.forecast(len(test))
    plt.figure(figsize=(150,10))
    plt.plot(train.i,train[y],label='Train',color='r')
    plt.plot(test.i,test[y],label='Test',color='g')
    plt.plot(test.i,test['holt'],label='Predict',color='b')
    plt.xlabel('Sequencial entries')
    plt.ylabel(y)
    plt.legend()
    plt.savefig(dir+y+'/'+y+'.png',dpi=130)
    plt.cla()
    plt.close()

    print(y,'MSE:',mean_squared_error(test[y],test['holt']))

# %%
