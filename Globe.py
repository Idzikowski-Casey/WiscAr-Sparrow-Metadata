import folium
from folium.features import Template
from folium.plugins import MarkerCluster
from pandas import isnull
from Comparing import *



class Map3d(folium.folium.Map):

    def __init__(self, location=None, width='100%', height='100%', left='0%',
                 top='0%', position='relative', tiles='OpenStreetMap', API_key=None,
                 max_zoom=18, min_zoom=1, zoom_start=10, attr=None, min_lat=-90,
                 max_lat=90, min_lon=-180, max_lon=180, detect_retina=False, crs='EPSG3857'):
        self.marker = self.Marker3D(location=location)
        super().__init__(
            location=location, width=width, height=height,
            left=left, top=top, position=position, tiles=tiles,
            API_key=API_key, max_zoom=max_zoom, min_zoom=min_zoom,
            zoom_start=zoom_start, attr=attr, min_lat=min_lat,
            max_lat=max_lat, min_lon=min_lon, max_lon=max_lon,
            detect_retina=detect_retina, crs=crs
        )
        self._template = Template(u"""
                {% macro header(this, kwargs) %}
        <html>
          <head>
            <script src="http://www.webglearth.com/v2/api.js"></script>
            <script>
              function initialize() 
              {
                var earth = new WE.map('earth_div');
                WE.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
                  attribution: '© OpenStreetMap contributors'
                }).addTo(earth);
              }
            </script>
            <style>
              html, body{padding: 0; margin: 0;}
              #earth_div{top: 0; right: 0; bottom: 0; left: 0; position: absolute !important;}
            </style>
            <title>WiscAr Samples on Globe</title>
          </head>
          <body onload="initialize()">
            <div id="earth_div"></div>
          </body>

                {% endmacro %}
                {% macro html(this, kwargs) %}
                    <div class="folium-map" id="{{this.get_name()}}" ></div>
                {% endmacro %}

                {% macro script(this, kwargs) %}

                    var southWest = L.latLng({{ this.min_lat }}, {{ this.min_lon }});
                    var northEast = L.latLng({{ this.max_lat }}, {{ this.max_lon }});
                    var bounds = L.latLngBounds(southWest, northEast);

                    var {{this.get_name()}} = WE.map('{{this.get_name()}}', {
                                                   center:[{{this.location[0]}},{{this.location[1]}}],
                                                   zoom: {{this.zoom_start}},
                                                   maxBounds: bounds,
                                                   layers: [],
                                                   crs: L.CRS.{{this.crs}}
                                                 });
                    
                                                 {% endmacro %}
                                                 </html>
        """)
    class Marker3D(folium.Marker):
        def __init__(self, location, popup=None,
                        tooltip=None, icon=None, draggable=False):
            super().__init__(location=location, popup=popup,
                        tooltip=tooltip, icon=icon, draggable=draggable)
            self._template = Template(u"""
        
         {% macro header(this, kwargs) %}
         <html>
         <head>
         <script>
          <script src="http://www.webglearth.com/v2/api.js"></script>
             function initialize() 
             {
             vars marker = WE.marker(this.location()).addTo(earth);
             }
            </script 
            </head>
             {% endmacro %}
             
        {% macro header(this, kwargs) %}
        
                    var {{this.get_name()}} = WE.marker(
                    '{{this.marker}}',
                    {
                    position : {{this.location}}
                    }
                                                      
                    ).addTo({{this._parent.get_name()}});
                    
                    {{this.get_name()}}.bindPopup({{this.popup}})
            
            {% endmacro %}
        </html>
        """)



m = Map3d(location=[60.25, 24.8], zoom_start=1)

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


for i, series in dfmdropna.iterrows():
    Map3d.Marker3D([series.latitude, series.longitude],
                  tooltip=series.sample_name,
                  popup=['Name:', series.sample_name, 'Title:', series.Title]).add_to(m)

for i, series in PI.iterrows():
    Map3d.Marker3D([series.latitude, series.longitude],
                  tooltip=series.sample_name,
                  popup=['Name:', series.sample_name, 'Title:', series.Title],
                  icon=folium.Icon(color='green')).add_to(m)



m.save('globetest.html')

