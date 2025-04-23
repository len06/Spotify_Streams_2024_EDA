from dash import Dash, dcc, Input, Output
from dash_bootstrap_templates import load_figure_template
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

df = pd.read_csv('../data/Most_Streamed_Spotify_Songs_2024.csv',encoding='latin1')

#We drop the column for the TIDAL popularity since it containts mostly missing values
df = df.drop('TIDAL Popularity',axis=1)

#Filling missing columns of Spotify Streams, Spotify Playlist Count and Spotify Playlist Reach with 0s
df[['Spotify Streams','Spotify Playlist Count', 'Spotify Playlist Reach']] = df[['Spotify Streams','Spotify Playlist Count', 'Spotify Playlist Reach']].fillna('0')

#Converting the columns of Spotify Streams, Spotify Playlist Count and Spotify Playlist Reach from strings to integersdf[['Spotify Streams','Spotify Playlist Count', 'Spotify Playlist Reach']] = df[['Spotify Streams','Spotify Playlist Count', 'Spotify Playlist Reach']].str.replace(',','').astype(int)
df['Spotify Streams'] = df['Spotify Streams'].str.replace(',','').astype(int)
df['Spotify Playlist Count'] = df['Spotify Playlist Count'].str.replace(',','').astype('int')
df['Spotify Playlist Reach'] = df['Spotify Playlist Reach'].str.replace(',','').astype('int')

#We do this for the columns of Youtube and Tiktok Views as well
df[['YouTube Views', 'TikTok Views']] = df[['YouTube Views', 'TikTok Views']].fillna('0')
df['YouTube Views'] = df['YouTube Views'].str.replace(',','').astype(int)
df['TikTok Views'] = df['TikTok Views'].str.replace(',','').astype(int)

#Drop duplicates in the df
df.drop_duplicates(inplace=True)

# Top 5 streamed songs in Spotify data frame
df_top_tracks = df[['Track','Spotify Streams']].copy()

# Combine all the streams for the same songs
df_top_tracks = df_top_tracks.groupby(['Track'],as_index=False).sum()
df_top_tracks = df_top_tracks.sort_values(by='Spotify Streams',ascending=False)


df_top_tracks = df_top_tracks.reset_index()
df_top_tracks.drop(columns='index',inplace=True)
df_top5_tracks = df_top_tracks[:5].copy()
print(df_top5_tracks)

# Top 10 Spotify Artists dataframe
df_artists = df[['Artist','Spotify Streams']].copy()

# Combine all the streams for the same artists
df_artists = df_artists.groupby(['Artist']).sum()
df_artists = df_artists.sort_values(by='Spotify Streams',ascending=False)
df_artists = df_artists.reset_index()
df_artists = df_artists[:10].copy()
print(df_artists)

# Top 100 Tracks explicit?
df_top100_tracks = df[['Track','Spotify Streams','Explicit Track']].copy()
#We First get the top 100 tracks from the dataset
df_top100_tracks = df_top100_tracks.groupby(['Track','Explicit Track'],as_index=False)['Spotify Streams'].sum()
df_top100_tracks.sort_values(inplace=True,by='Spotify Streams',ascending=False)
df_top100_tracks = df_top100_tracks[:100]

#Then we get the total count of explicit and non-explicit tracks from the top 100 tracks
df_explicit_count = df_top100_tracks['Explicit Track'].value_counts()
df_explicit_count = df_explicit_count.reset_index()
df_explicit_count.replace(to_replace={0:'Non-Explicit',1:"Explicit"},inplace=True)
print(df_explicit_count)


# Getting the data across the three most prominent platforms for streaming/viewing music
df_platforms = df[['Spotify Streams','YouTube Views', 'TikTok Views']].copy()
# Convert the values back to NaN to avoid affecting the min of the distribution
df_platforms = df_platforms[['Spotify Streams', 'YouTube Views', 'TikTok Views']].replace(0,pd.NA)
df_platforms = df_platforms.dropna()

df_platforms = df_platforms[['Spotify Streams', 'YouTube Views', 'TikTok Views']].astype(int)
df_platforms_melted = df_platforms.melt(var_name='Platforms', value_name='Value')

@app.callback(
    Output(dashboard_title,component_property='children'),
    Output(dashboard_graph,component_property='figure'),
    Input(dashboard_input,component_property='value')
)

def dashboard_update(input_value):
    if input_value == 'Top 5 Spotify Tracks of 2024':
        fig = px.bar(data_frame=df_top5_tracks,
               x='Track',
               y='Spotify Streams'
               )
        
    elif input_value == "Spotify's Top 10 Most Streamed Artists in 2024":
        fig = px.bar(data_frame=df_artists,
                     x='Artist',
                     y='Spotify Streams'
                    )
    
    elif input_value == "How many of the top 100 Songs in 2024 of Spotify are Explicit?":
        fig = px.pie(data_frame=df_explicit_count,
                     values='count',
                     hole=.3,
                     names='Explicit Track'
                    )
    
    elif input_value == "Distribution of Streams/Views across Different Platforms":
        fig = px.box(data_frame=df_platforms_melted,
                     x='Value',
                     y='Platforms'
            )
        fig.update_xaxes(range=[0,15000000000])

    return f'# {input_value}', fig

if __name__ == '__main__':
    app.run(debug=True)