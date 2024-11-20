from shiny import App, render, ui, reactive
import pandas as pd
import json
import altair as alt
from shinywidgets import render_altair, output_widget

app_ui = ui.page_fluid(
  ui.input_select(id = "type_subtype", label = "Choose a combination:", 
                  choices = ["JAM - UNCLASSIFIED", "ACCIDENT - UNCLASSIFIED", "ROAD_CLOSED - UNCLASSIFED", 
                             "HAZARD - UNCLASSIFIED", "ACCIDENT - MAJOR", "ACCIDENT - MINOR", "HAZARD - ON_ROAD", 
                             "HAZARD - ON_SHOULDER", "HAZARD - WEATHER", "JAM - HEAVY", "JAM - MODERATE", "JAM - STAND_STILL", 
                             "ROAD_CLOSED - EVENT", "ROAD_CLOSED - CONSTRUCTION", "JAM - LIGHT", "ROAD_CLOSED - HAZARD"]),
  output_widget("map")
)

def server (input, output, session):
  @reactive.calc
  def data():
    return pd.read_csv("/Users/hallielovin/Documents/GitHub/ps6/top_alerts_map/top_alerts_map.csv")
  
  @reactive.calc
  def grouped(): 
    top_alerts_map = data()
    return top_alerts_map[top_alerts_map["type_subtype"] == input.type_subtype()]
    
  @render.table()
  def grouped_table():
    return grouped()
  
  @reactive.calc
  def map_data():
    with open("/Users/hallielovin/Documents/GitHub/ps6/top_alerts_map/Boundaries - Neighborhoods.geojson") as f:
        chicago_geojson = json.load(f)
    geo_data = alt.Data(values=chicago_geojson["features"])
    return geo_data
  
  
  @render_altair
  def map():
    top_alerts_map = grouped()
    selected_type = input.type_subtype
    geo_data = map_data()

    plot1 = alt.Chart(top_alerts_map).mark_circle().encode(
    x = alt.X("longitude:Q", scale=alt.Scale(domain = [-87.95, -87.52])),
    y = alt.Y("latitude:Q", scale=alt.Scale(domain=[41.6, 42.05])),
    size = alt.Size("count:Q", legend=alt.Legend(title="Number of Alerts"))).properties(
    title = "Ten Highest Number of Heavy Traffic Jams")

    chi_map = alt.Chart(geo_data).mark_geoshape(
    fillOpacity=0,  
    stroke="black"  
    ).encode().project(
    type="identity",
    reflectY=True
    ).properties(
    width = 600, 
    height = 600)

    combined_chart = chi_map + plot1

    return combined_chart  
  
app = App(app_ui, server)