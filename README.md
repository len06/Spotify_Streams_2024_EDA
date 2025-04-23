# 📊 Exploratory Data Analysis on Most Streamed Songs on Spotify in 2024 dataset

This project explores the most streamed songs on Spotify in 2024, using a dataset containing metadata for over 4500 songs. The goal is to understand the structure of the data, identify patterns, and visualize relationships between various music platforms.

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
-`Explicit Track`: Gives information on whether a song is explicit or not

---

## 🎯 Objectives

- Handle missing values and data inconsistencies in columns 
- Analyze distributions of key numerical features
- Explore popularity trends by artist
- Visualize insights using Seaborn and Matplotlib

---

## 📊 Key Findings

- Cover of songs takes the first 2 spots of the top 5 most streamed songs for Spotify 
- The majority of the top 100 songs on Spotify in 2024 are non-explicit songs (74%)
- The distribution of views on platforms such as TikTok and YouTube is skewed heavily to the right due to extremely large outliers

  ---

## 📈 Dashboard view

To launch the interactive dashboard and explore the visualizations:
  1. Navigate to the `scripts` directory:
      cd scripts
  2. Run the dashboard script:
      python dashboard.py
  3. Open your browser and go to:
      http://127.0.0.1:8050/
  4. Make sure you have all the required libraries and frameworks installed
