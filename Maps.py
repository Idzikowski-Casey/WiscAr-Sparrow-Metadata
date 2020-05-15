import folium
from folium.plugins import MarkerCluster
import json
import geopandas as gpd
from pandas import isnull
from Comparing import *

# create map
m = folium.Map()


dfm1 = dfm
dfm1["longitude"] = pd.to_numeric(dfm1["longitude"], downcast="float")
dfm1["latitude"] = pd.to_numeric(dfm1["latitude"], downcast="float")


for i, series in dfm1.iterrows():
    if series.longitude > 300:
        dfm1.drop(i, inplace=True)
for i, series in dfm1.iterrows():
    if (isnull(series.Unpublished)) is False:
        dfm1.drop(i, inplace=True)
dfmdropna = dfm1.dropna(subset=['latitude'])


PI = []
for i, series in dfm1.iterrows():
    if (isnull(series.From_PI)) is False:
      PI.append(series)
for i, series in dfm1.iterrows():
    if (isnull(series.From_PI)) is False:
        dfm1.drop(i, inplace=True)
PI = pd.DataFrame(PI)

# mcLit = folium.plugins.MarkerCluster().add_to(m)
# mcPI = folium.plugins.MarkerCluster().add_to(m)

for i, series in dfmdropna.iterrows():
    folium.Marker([series.latitude, series.longitude],
                  tooltip=series.sample_name,
                  popup=['Name:', series.sample_name, 'Title:', series.Title]).add_to(m)

for i, series in PI.iterrows():
    folium.Marker([series.latitude, series.longitude],
                  tooltip=series.sample_name,
                  popup=['Name:', series.sample_name, 'Title:', series.Title],
                  icon=folium.Icon(color='green')).add_to(m)


# save map to html file

m.save('testmap.html')

# popup='ID:'+df_counters['ID'][point]+' '+df_counters['Name'][point]