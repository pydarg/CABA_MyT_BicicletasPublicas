import pandas as pd

#map tools
import folium
from folium.plugins import MeasureControl, MarkerCluster, MiniMap, MousePosition, Draw, Fullscreen

def draw_map(df, cluster_marks=True):
    
    m = folium.Map(location = [df['lat'].mean(), df['long'].mean()],
               zoom_start = 15,
               control_scale=True)
    
    if cluster_marks == True:
        
        mc = MarkerCluster()
        
        for row in df.iterrows():
            mc.add_child( folium.Marker( location = [row[1]['lat'],row[1]['long']], popup = row[1]['nombre']))
        m.add_child(mc)
    else:
        for row in df.iterrows():
            folium.Marker(location = [row[1]['lat'],row[1]['long']], popup = row[1]['nombre']).add_to(m)
    
    
    #OPTIONAL PLUGGINS
    #minimaps
    minimap = MiniMap(toggle_display=True)
    m.add_child(minimap)
    
    #measure tool
    m.add_child(MeasureControl())
    #show de coordinates from cursor position
    MousePosition().add_to(m)
    
    #draw tools
    draw = Draw(export=True)
    draw.add_to(m)
    
    #full screen
    Fullscreen(
        position='topright',
        title='Expand me',
        title_cancel='Exit me',
        force_separate_button=True).add_to(m)
      
    return m

def draw_mult_map(df_a, df_b):
    
    m = folium.Map(location = [df_a['lat'].mean(), df_b['long'].mean()],
               zoom_start = 15,
               control_scale=True)
    
    feature_group_estaciones = folium.FeatureGroup(name='Estaciones de Bicicletas')
    feature_group_tiendas = folium.FeatureGroup(name='Tiendas')
    
    marker_cluster_estaciones = MarkerCluster()
    marker_cluster_tiendas = MarkerCluster()
    
    for row in df_a.iterrows():
        marker_estaciones = folium.Marker(location = [row[1]['lat'],row[1]['long']], popup = str(row[1]['nro_est']) + '. '+ str(row[1]['nombre']), icon = folium.Icon(color='green'))
        marker_cluster_estaciones.add_child(marker_estaciones)

    for row in df_b.iterrows():
        marker_tiendas = folium.Marker(location = [row[1]['lat'],row[1]['long']], popup = row[1]['nombre'], icon = folium.Icon(color='red'))
        marker_cluster_tiendas.add_child(marker_tiendas)
    
    feature_group_estaciones.add_child(marker_cluster_estaciones)
    feature_group_tiendas.add_child(marker_cluster_tiendas)
    
    m.add_child(feature_group_estaciones)
    m.add_child(feature_group_tiendas)
    m.add_child(folium.LayerControl())
    
    #OPTIONAL PLUGGINS
    #minimaps
    minimap = MiniMap(toggle_display=True)
    m.add_child(minimap)
    
    #measure tool
    m.add_child(MeasureControl())
    #show de coordinates from cursor position
    MousePosition().add_to(m)
    
    #draw tools
    draw = Draw(export=True)
    draw.add_to(m)
    
    #full screen
    Fullscreen(
        position='topright',
        title='Expand me',
        title_cancel='Exit me',
        force_separate_button=True).add_to(m)
    return m