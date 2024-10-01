import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("result.csv",header=0, index_col=0)
df.index.name = None
colores = ['#2c3e50', '#34495e', '#7f8c8d', '#95a5a6']
# count = df["Lista 30"].value_counts()
print(df.head())
for index,row in enumerate(df.index):
    fig, ax = plt.subplots()    
    df.iloc[index].plot.pie(autopct='%1.1f%%',wedgeprops={'edgecolor': 'white'},labels=["","","","","","","","","","",""],ax=ax)
    ax.legend(labels=df.columns, bbox_to_anchor=(1, 0, 0.5, 1))
    plt.savefig(f'results/result_{row}.pdf', bbox_inches='tight')
    # plt.show()
    
