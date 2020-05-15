import pandas as pd

# reads online metadata, and both sheets of my searched for metadata, all into different pandas dataframes
df1 = pd.read_excel('online_metadata.xls')
df2 = pd.read_excel('WiscAr_metadata(thisone).xlsx')
dfa = pd.read_excel('WiscAr_metadata(thisone).xlsx', sheet_name='Additional')

# Splitting the geometry column into a Latitude and Longitude column
new = df1["geometry"].str.split("[", n=1, expand=True)
df1["Split1"] = new[0]
df1["LocationSplit"] = new[1]

neww = df1["LocationSplit"].str.split(" ", n=1, expand=True)
df1["Longitude"] = neww[0]
df1["Latitude"] = neww[1]

# Removing extra characters not removed from the splitting
df1["Longitude"] = df1["Longitude"].str.rstrip(to_strip=",")
df1["Latitude"] = df1["Latitude"].str.rstrip(to_strip="]}")

# dropping unwanted columns including the new ones from splitting
df1 = df1.drop(['id', 'igsn', 'location_precision', 'project_id', 'project_name', 'Split1',
                'LocationSplit', 'geometry'], axis=1)

# combining the first and second sheet of my searched metadata by concat function, it stacks the data by column name
dfm = pd.concat([dfa, df2], ignore_index=True, axis=0, sort=False)
dfmd = dfm.drop(['sparrow order', 'id', 'technique', 'Irradiation', 'phase', 'sample_name.1', 'GeoDeepDive ping?',
                'Comments', 'Notes'], axis=1)
writer = pd.ExcelWriter('fullmetadata.xlsx', engine='xlsxwriter')
dfmd.to_excel(writer, sheet_name='Full_Metadata')
writer.save()

# setting indexes for merging
df1.set_index('name')
dfmd.set_index('sample_name')

# merging dataframes
df3 = df1.merge(dfmd, how='outer', on=None, left_on=None, right_on=None, left_index=True, right_index=True)

# Saving as a excel sheet
writer2 = pd.ExcelWriter('Comparison_Sheet.xlsx', engine='xlsxwriter')
df3.to_excel(writer2, sheet_name='Sheet_1')
writer2.save()

