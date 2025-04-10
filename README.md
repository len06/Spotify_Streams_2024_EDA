# 📊 Exploratory Data Analysis on Most Streamed Songs on Spotify in 2024 dataset

This project explores the most streamed songs on spotify in 2024 dataset containing metadata of over 4500 songs. The goal is to understand the structure of the data, identify patterns and visualize relationships between various music platforms.

---

## 📦 Dataset 

- **Source**: [Most Streamed Spotify Songs 2024](https://www.kaggle.com/datasets/nelgiriyewithana/most-streamed-spotify-songs-2024/data)
- **Rows**: ~4600
- **Columns**: 29
- **Description**: Each row represents a unique track on Spotify and information about the number of streams and popularity of the song across various music platforms

### 🔑 Key Features:

-`Track`: Name of the song
-`Artist`: Artist of the song
-`Spotify Streams, YouTube Views, TikTok Views`: Streams/Views amassed by the specific song
-`Explicit Track`: Gives information of wether a song is explicit or not

---

## 🎯 Objectives

- Handle missing values and data inconsistencies of columns 
- Analyze distributions of key numerical features
- Explore pouplarity trends by artist
- Visualize insights using Seaborn and Matplotlib

---

## 📊 Key Findings

- Cover of songs takes the first 2 spots of the top 5 most streamed songs for Spotify 
- The majority of the top 100 songs on Spotifty in 2024 are non-explicit songs (74%)
- The distribution of views on platforms such as TikTok and YouTube are skewed heavily to the right due to extremely large outliers
