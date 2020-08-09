# %%
import matplotlib.pyplot as plt
import pandas as pd
import os
import seaborn as sns


from sklearn.ensemble import AdaBoostClassifier,ExtraTreesClassifier,GradientBoostingClassifier,RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier

from sklearn.metrics import mean_squared_error




df = pd.read_csv('data/final.csv',header=0,parse_dates=['ISODate'],index_col='ISODate')
prediction_targets = ['BEAMS','BEAMT','BEAMT2']

resample_method = '3H'
df_resampled = df.resample(resample_method).mean()
# now->future 3H
for target in prediction_targets:
    df_resampled[target] = df_resampled[target].shift(-1)

df_resampled = df_resampled.dropna(axis=0)
df_resampled['i'] = [x for x in range(1,len(df_resampled)+1)]

s = int(len(df_resampled)*0.8)
train,test = df_resampled[:s],df_resampled[s:]

dir = "vis/machine/02mul_cla/"

# %%
for x in prediction_targets:
    if not os.path.exists(dir+x+'/'):
        os.makedirs(dir+x+'/')


for x in prediction_targets:
    thres = df_resampled[x].max()*0.5
    df_resampled[x][df_resampled[x]<thres] = 0
    df_resampled[x][df_resampled[x]>=thres] = 1

raw_features = "MTEMP,MUONKICKER,HTEMP,TS1_TOTAL_YEST,TS1_TOTAL,REPR,REPR2,TS2_TOTAL,TS2_TOTAL_YEST".split(',')


# %%
models = [AdaBoostClassifier(),ExtraTreesClassifier(),GradientBoostingClassifier(),RandomForestClassifier(),\
    KNeighborsClassifier(),MLPClassifier()]

for model in models:
    for y in prediction_targets:
        model.fit(train[raw_features],train[y])
        pred = model.predict(test[raw_features])
        plt.figure(figsize=(150,10))
        # plt.plot(train.i,train[y],label='Train',color='r')
        plt.plot(test.index,test[y],label='Test',color='r')
        plt.plot(test.index,pred,label='Predict',color='b')
        plt.xlabel('Date')
        plt.ylabel(y)
        plt.legend()
        plt.savefig(dir+y+'/'+type(model).__name__+'.png',dpi=130)
        plt.cla()
        plt.close()

        print(y,type(model).__name__,'MSE:',mean_squared_error(test[y],pred))