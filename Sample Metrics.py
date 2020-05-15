import pandas as pd
from pandas import isnull
import numpy as np

df = pd.read_excel('comparison_Sheet.xlsx')

# create 2 new data frames
dfOnline = df[['Longitude', 'Latitude']]
dfMeta = df[['longitude', 'latitude']]

# just prints entire df so I can see what # row to truncate
pd.set_option('display.max_rows', None)

# adding a new column Names from sample names of online or metadata
dfOnline.insert(0, "Names", df[['name']])
dfMeta.insert(0, "Names", df[['sample_name']])

# truncates all the null values that are there from other xlsx sheet.
# Because there were more samples in my sheet vs online
# NOTE: this function will work for any df as long as all samples have names.

dfOnline = dfOnline[~dfOnline.Names.isna()]

#Check that All Sparrow Samples have counterparts in Metadata

MetaData = []
SparrowData = []

for i, series in dfMeta.iterrows():
    MetaData.append(series.Names)

for i, series in dfOnline.iterrows():
    SparrowData.append(series.Names)

SparrowData = np.asarray(SparrowData)
SparrowData = np.unique(SparrowData)
MetaData = np.asarray(MetaData)
MetaData = np.unique(MetaData)

Totaldata = np.concatenate([MetaData, SparrowData])

Totaldata = np.unique(Totaldata, return_counts=True)
dfTotal = pd.DataFrame(Totaldata)

dfTotal = dfTotal.transpose()
dfTotal.columns = ['Names', 'Counts']
Repeats = []

for i, series in dfTotal.iterrows():
    if series.Counts > 1:
        Repeats.append(series.Names)

print(len(SparrowData) - len(Repeats))

# 5 samples on sparrow that aren't on metadata?

Repeats = np.asarray(Repeats)

Arry_SNM = np.concatenate([Repeats, SparrowData])
Arry_SNM = np.unique(Arry_SNM, return_counts=True)

df1 = pd.DataFrame(Arry_SNM)
df1 = df1.transpose()

df1.columns = ['Names', 'Counts']

SNM = []
for i, series in df1.iterrows():
    if series.Counts == 1:
        SNM.append(series.Names)





