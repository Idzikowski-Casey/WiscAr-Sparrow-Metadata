from Statisitcal_Analysis import *
import json
# figuring out how to add back on columns from og excel. Make it easier to search for stuff?
# It's easy, append the entire series when a condition is met

indexs = []

for i, series in dfm.iterrows():
    for ele in MetaMissing:
        if series.sample_name == ele:
            indexs.append(series)


indexs = pd.DataFrame(indexs)

writer = pd.ExcelWriter('MissingMetadata.xlsx', engine='xlsxwriter')
indexs.to_excel(writer, sheet_name='MissingMetadata')
writer.save()

Upindexs = []

for i, series in dfm.iterrows():
    for ele in Uploadable:
        if series.sample_name == ele:
            Upindexs.append(series)


Upindexs = pd.DataFrame(Upindexs)

j = Upindexs.groupby(['Title', 'author', 'year'], as_index=False).apply(
    lambda x: x[['sample_name', 'lithology', 'latitude', 'longitude', 'elevation_m', 'depth_m', 'Formation', 'Member']].
    to_dict('r')).reset_index().rename(columns={0: 'Sample_Data'}).to_json(orient='records')
data = json.loads(j)

with open('upload.json', 'w') as f:
    json.dump(data, f, indent=2)
