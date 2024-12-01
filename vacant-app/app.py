import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from shiny import App, render, ui, reactive
import folium
from folium import Marker

# Load the vacancy data from CSV file
vacancy_data = pd.read_csv('C:/Users/EM/Documents/GitHub/DAPII_final/vacant.csv')

# Convert issued_date to datetime and create a year column
vacancy_data['issued_date'] = pd.to_datetime(vacancy_data['issued_date'])
vacancy_data['year'] = vacancy_data['issued_date'].dt.year

# Create a geometry column from the coordinates
vacancy_data['geometry'] = vacancy_data.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)

# Transform vacancy location column into readable geographic data
vacancy_gdf = gpd.GeoDataFrame(vacancy_data, geometry='geometry')

app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_slider(
                "year",
                "Select Year",
                min=vacancy_gdf['year'].min(),
                max=vacancy_gdf['year'].max(),
                value=vacancy_gdf['year'].min(),
                step=1
            )
        ),
        ui.output_ui("map")
    )
)

def create_map(year):
    filtered_gdf = vacancy_gdf[vacancy_gdf['year'] == year]
    m = folium.Map(location=[41.85, -87.65], zoom_start=10)
    
    for _, row in filtered_gdf.iterrows():
        Marker(
            location=[row['geometry'].y, row['geometry'].x],
            popup=row['property_address']
        ).add_to(m)
    
    return m

def server(input, output, session):
    @output
    @render.ui
    @reactive.event(input.year)
    def map():
        selected_year = input.year()
        m = create_map(selected_year)
        map_html = m._repr_html_()
        return ui.HTML(map_html)

app = App(app_ui, server)
