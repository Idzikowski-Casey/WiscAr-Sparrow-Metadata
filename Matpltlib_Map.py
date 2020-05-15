import numpy as np
from pandas import isnull
import geopandas as gpd
import matplotlib.pyplot as plt
from Comparing import *
dfr = dfm
dfm1 = dfr
dfm1["longitude"] = pd.to_numeric(dfm1["longitude"], downcast="float")
dfm1["latitude"] = pd.to_numeric(dfm1["latitude"], downcast="float")


for i, series in dfm1.iterrows():
    if series.longitude > 300:
        dfm1.drop(i, inplace=True)
for i, series in dfm1.iterrows():
    if (isnull(series.Unpublished)) is False:
        dfm1.drop(i, inplace=True)

PI = []
for i, series in dfm1.iterrows():
    if (isnull(series.From_PI)) is False:
      PI.append(series)
for i, series in dfm1.iterrows():
    if (isnull(series.From_PI)) is False:
        dfm1.drop(i, inplace=True)
PI = pd.DataFrame(PI)

gdf2 = gpd.GeoDataFrame(PI, geometry=gpd.points_from_xy(PI.longitude, PI.latitude))
gfd1 = gpd.GeoDataFrame(dfm1, geometry=gpd.points_from_xy(dfm1.longitude, dfm1.latitude))

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
base = world.plot(color='white', edgecolor='k')
gfd1.plot(ax=base, marker='o', color='blue', markersize=5, label='From Literature Search')
gdf2.plot(ax=base, marker='*', color='green', markersize=5, label='From PI')
plt.legend(prop={'size': 5})
# get layers of data points for maps, make it different colors

