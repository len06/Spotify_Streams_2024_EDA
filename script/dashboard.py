from dash import Dash, dcc, Input, Output
from dash_bootstrap_templates import load_figure_template
from data_loader import *
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#Defining the App_layout 
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
load_figure_template("darkly")
dashboard_title = dcc.Markdown(children="")
dashboard_graph = dcc.Graph(figure={})
dashboard_input = dcc.Dropdown(
                    options=['Top 5 Spotify Tracks of 2024',
                             "Spotify's Top 10 Most Streamed Artists in 2024", 
                             "How many of the top 100 Songs in 2024 of Spotify are Explicit?",
                             "Distribution of Streams/Views across Different Platforms"
                            ],
                    value='Top 5 Spotify Tracks of 2024',
                    clearable=False ,
                    style={'color':'black', 
                           'background-color':'#b9bab4'}                
)

app.layout = dbc.Container([
                dbc.Card([
                    dbc.CardHeader([dashboard_title], class_name='align-self-center',
                                   style={"width":"100%", 
                                          'font-family':'roboto',
                                          "background-color":"#2b2b2b",
                                          "color":"white",
                                          "text-align":"center",
                                          "padding":"1rem"}),
                    dbc.CardBody([dashboard_graph])
                ], class_name='mt-4 mb-4'),
                dbc.Card([
                    dbc.CardBody([dashboard_input],style={'font-family':'roboto'})
                ], class_name='mb-4')
])

# Getting all the relevant data frames to be visualized
df = load_data()
df_top5_tracks = get_top5_tracks(df)
df_artists = get_top10_artists(df)
df_explicit_count = get_explicit_songs(df)
df_platforms_melted = get_platforms_distribution(df)


@app.callback(
    Output(dashboard_title,component_property='children'),
    Output(dashboard_graph,component_property='figure'),
    Input(dashboard_input,component_property='value')
)


def dashboard_update(input_value):
    chart_config = {
        'Top 5 Spotify Tracks of 2024': lambda:
            px.bar
            (
               data_frame=df_top5_tracks,
               x='Track',
               y='Spotify Streams'
            )
        ,
        'Spotify\'s Top 10 Most Streamed Artists in 2024': lambda: 
            px.bar
            (
                data_frame=df_artists,
                x='Artist',
                y='Spotify Streams'   
            )
        ,
        'How many of the top 100 Songs in 2024 of Spotify are Explicit?': lambda:
            px.pie
            (
                data_frame=df_explicit_count,
                values='count',
                hole=.3,
                names='Explicit Track'   
            )
        ,
        'Distribution of Streams/Views across Different Platforms': lambda:
            px.box
            (
                data_frame=df_platforms_melted,
                     x='Value',
                     y='Platforms'
            )
    }

    fig = chart_config.get(input_value,lambda:None)()

    if input_value == 'Distribution of Streams/Views across Different Platforms':
        fig.update_xaxes(range=[0,15000000000])
    
    return f'# {input_value}', fig


if __name__ == '__main__':
    app.run(debug=True)