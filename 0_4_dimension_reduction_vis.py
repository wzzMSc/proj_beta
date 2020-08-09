# %%
import matplotlib.pyplot as plt
import pandas as pd
import os
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns

df = pd.read_csv('data/final.csv',header=0,parse_dates=['ISODate'],index_col='ISODate')

resample_method = '3H'
df_resampled = df.resample(resample_method).mean()
df_resampled = df_resampled.dropna(axis=0)

prediction_targets = ['BEAMS','BEAMT','BEAMT2']


# %%
for x in prediction_targets:
    if not os.path.exists("vis/dr_pca/"+x+'/'):
        os.makedirs("vis/dr_pca/"+x+'/')


for x in prediction_targets:
    thres = df_resampled[x].max()*0.5
    df_resampled[x][df_resampled[x]<thres] = 0
    df_resampled[x][df_resampled[x]>=thres] = 1

# %%
raw_features = "MTEMP,MUONKICKER,HTEMP,TS1_TOTAL_YEST,TS1_TOTAL,REPR,BEAMT2,REPR2,TS2_TOTAL,TS2_TOTAL_YEST".split(',')

# %%
pca = PCA(n_components=3)
pca_result = pca.fit_transform(df_resampled[raw_features].values)
print('Explained variation per principal component: {}'.format(pca.explained_variance_ratio_))

# %%
for i in range(1,pca_result.shape[1]+1):
    df_resampled['PCA'+str(i)] = pca_result[:,i-1]


# %%
pca_l = ['PCA1','PCA2','PCA3']
for target in prediction_targets:
    for x in pca_l:
        for y in pca_l:
            sns.scatterplot(x,y,data=df_resampled,hue=target)
            plt.savefig("vis/dr_pca/"+target+'/'+x+"-"+y+".png")
            plt.cla()
            plt.close()

# %%
for target in prediction_targets:
    ax = Axes3D(plt.figure(figsize=(15,15)))
    ax.scatter3D(df_resampled['PCA1'],df_resampled['PCA2'],df_resampled['PCA3'],c=df_resampled[target])
    ax.set_xlabel('PCA1')
    ax.set_ylabel('PCA2')
    ax.set_zlabel('PCA3')
    plt.savefig("vis/dr_pca/"+target+'/'+target+"_3d.png",dpi=130)
    plt.cla()
    plt.close()

##################################################################
#######                t-SNE
##################################################################
# %%
for x in prediction_targets:
    if not os.path.exists("vis/dr_tsne/"+x+'/'):
        os.makedirs("vis/dr_tsne/"+x+'/')

tsne = TSNE(n_components=3,verbose=1,n_iter=1000)
tsne_results = tsne.fit_transform(df_resampled[raw_features].values)

for i in range(1,tsne_results.shape[1]+1):
    df_resampled['tSNE'+str(i)] = tsne_results[:,i-1]

tsne_l = ['tSNE1','tSNE2','tSNE3']
for target in prediction_targets:
    for x in tsne_l:
        for y in tsne_l:
            sns.scatterplot(x,y,data=df_resampled,hue=target)
            plt.savefig("vis/dr_tsne/"+target+'/'+x+"-"+y+".png")
            plt.cla()
            plt.close()

for target in prediction_targets:
    ax = Axes3D(plt.figure(figsize=(15,15)))
    ax.scatter3D(df_resampled['tSNE1'],df_resampled['tSNE2'],df_resampled['tSNE3'],c=df_resampled[target])
    ax.set_xlabel('tSNE1')
    ax.set_ylabel('tSNE2')
    ax.set_zlabel('tSNE3')
    plt.savefig("vis/dr_tsne/"+target+'/'+target+"_3d.png",dpi=130)
    plt.cla()
    plt.close()

# %%
