import pandas as pd
from pandas import isnull
import numpy as np
from Comparing import *

# create 2 new data frames
dfOnline = df3[['Longitude', 'Latitude']]
dfMeta = df3[['longitude', 'latitude']]

# just prints entire df so I can see what # row to truncate
pd.set_option('display.max_rows', None)

# adding a new column Names from sample names of online or metadata
dfOnline.insert(0, "Names", df3[['name']])
dfMeta.insert(0, "Names", df3[['sample_name']])

# truncates all the null values that are there from other xlsx sheet.
# Because there were more samples in my sheet vs online
# NOTE: this function will work for any df as long as all samples have names.

dfOnline = dfOnline[~dfOnline.Names.isna()]

Metalist = []
SparrowList = []
for i, series in dfMeta.iterrows():
    Metalist.append(series.Names)

for i, series in dfOnline.iterrows():
    SparrowList.append(series.Names)

Metadatasamples = np.asarray(Metalist, order='F')
Metadatasamples = np.unique(Metadatasamples)
SparrowSamples = np.asarray(SparrowList)
SparrowSamples = np.unique(SparrowSamples)

totalsamples = np.concatenate((Metadatasamples, SparrowSamples))
totalsamples = np.unique(totalsamples, return_counts=True)
dfTotal = pd.DataFrame(totalsamples)
dfTotal = dfTotal.transpose()
dfTotal.columns = ['Names', 'Counts']

Uploadable_total = []
for i, series in dfTotal.iterrows():
    if series.Counts == 1:
        Uploadable_total.append(series.Names)

# Uploadable_total is the total of metadata samples that are not on sparrow. Some have metadata and others do not.
# creating empty lists for data from for loop

MetaFound = []
OnlMissing = []
MetaMissing = []

# For each row, if the value for Longitude is NaN then the Name of the sample goes into the list
for i, series in dfOnline.iterrows():
    if (isnull(series.Longitude)) is True:
        OnlMissing.append(series.Names)

for i, series in dfMeta.iterrows():
    if (isnull(series.longitude)) is True:
        MetaMissing.append(series.Names)

for i, series in dfMeta.iterrows():
    if (isnull(series.longitude)) is False:
        MetaFound.append(series.Names)

# combing lists, turning them into a numpy array and then
# returning an arry that has NO duplicates
MissingData1 = MetaMissing + OnlMissing
arry_test = np.asarray(MissingData1, order='F')
MissingData = np.unique(arry_test)

MissingOnline = np.asarray(OnlMissing, order='F')
MetaFound = np.asarray(MetaFound, order='F')
MissingOnline = np.unique(MissingOnline)
MetaFound = np.unique(MetaFound)

arryc = np.concatenate((MetaFound, MissingOnline))

Update = np.unique(arryc, return_counts=True)
dfc = pd.DataFrame(Update)
dfc = dfc.transpose()

# dfc is a dataframe that has a full list of unique samples from the combined lists
# The 2nd column gives the number of times it was duplicated, if 2nd column = 2 when there is a location on metadata
# that isn't uploaded to sparrow
# rename columns to make iteration nice

dfc.columns = ['Name', 'Counts']
Uploadable = []
for i, series in dfc.iterrows():
    if series.Counts > 1:
        Uploadable.append(series.Name)

# return false value if no longitutde or latitude is recorded, otherwise true, then replace false with 0 and true with 1
dfOnSt = ~dfOnline.isna()

dfMSt = ~dfMeta.isna()

dfOnSt = dfOnSt.drop(columns=['Names', 'Longitude'])
dfOnSt = dfOnSt * 1
dfMSt = dfMSt.drop(columns=['Names', 'longitude'])
dfMSt = dfMSt * 1

# turns pandas dataframe into a numpy array
Online = dfOnSt.to_numpy()
Metadata = dfMSt.to_numpy()

# Some Statistic stuffs
var = "%"
len(Online)
Percent_Loc_Found_Online = np.round(np.count_nonzero(Online) / len(Online) * 100)
Percent_Loc_Found_Metada = np.round(np.count_nonzero(Metadata) / len(Metadata) * 100)
