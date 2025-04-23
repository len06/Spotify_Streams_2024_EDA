import pandas as pd

def load_data():
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
    return df

def get_top5_tracks(df):
    # Top 5 streamed songs in Spotify data frame
    df_top_tracks = df[['Track','Spotify Streams']].copy()

    # Combine all the streams for the same songs
    df_top_tracks = df_top_tracks.groupby(['Track'],as_index=False).sum()
    df_top_tracks = df_top_tracks.sort_values(by='Spotify Streams',ascending=False)


    df_top_tracks = df_top_tracks.reset_index()
    df_top_tracks.drop(columns='index',inplace=True)
    df_top5_tracks = df_top_tracks[:5].copy()

    return df_top5_tracks

def get_top10_artists(df):
    # Top 10 Spotify Artists dataframe
    df_artists = df[['Artist','Spotify Streams']].copy()

    # Combine all the streams for the same artists
    df_artists = df_artists.groupby(['Artist']).sum()
    df_artists = df_artists.sort_values(by='Spotify Streams',ascending=False)
    df_artists = df_artists.reset_index()
    df_artists = df_artists[:10].copy()

    return df_artists

def get_explicit_songs(df):
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

    return df_explicit_count

def get_platforms_distribution(df):
    # Getting the data across the three most prominent platforms for streaming/viewing music
    df_platforms = df[['Spotify Streams','YouTube Views', 'TikTok Views']].copy()
    # Convert the values back to NaN to avoid affecting the min of the distribution
    df_platforms = df_platforms[['Spotify Streams', 'YouTube Views', 'TikTok Views']].replace(0,pd.NA)
    df_platforms = df_platforms.dropna()

    df_platforms = df_platforms[['Spotify Streams', 'YouTube Views', 'TikTok Views']].astype(int)
    df_platforms_melted = df_platforms.melt(var_name='Platforms', value_name='Value')

    return df_platforms_melted