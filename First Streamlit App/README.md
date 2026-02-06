How to Run the Application:
streamlit run "First Streamlit App/main.py"

# IMDB Movies Dataset Explorer

## Overview

This project creates an interactive Streamlit dashboard for exploring patterns and relationships in 10,000 movies from The MOvie Database (TMDB). With this applicaiton you can analyze movie data through a sortable tables, a scatter plots with trendline analysis, and categorical bar chart.

**Dataset**: The IMDB dataset contains 10,000 movies (late 1900s–2024) with 20 variables including budget, revenue, popularity, ratings, genres, languages, and production companies.

## Features

- **Interactive Data Table**: You can browse and sort movies by any variable.
- **Scatter Plots**: You can visualize relationships between numerical variables with optional trendlines and regression statistics (slope, intercept, R²).
- **Bar Charts**: You can compare average metrics across categories like genre, language, and production company.
- **Smart Filtering**: The tool automatically removes outliers and low-frequency categories for cleaner visualizations

## Installation

**Prerequisites**: Python

Ensure your dataset is located at `data/trimmed_movies.csv`.

## Usage

**Data Table**: Use the "Sort by" dropdown to reorder movies by any column.

**Scatter Plots**: 
- Select a predefined comparison or choose a "Custom Comparison" to pick your own variables
- Check "Show trendline" to add trendline analysis
- Hover over points for movie details; click and drag to zoom

**Bar Charts**:
- Choose categorical comparisons to see average performance by category or select "Custom Comparison" for custom groupings
- Hover over bars for exact values and sample counts

**Note**: The app filters to the top 10,000 movies by popularity and removes extreme outliers for better visualization.

## Project Structure

```
imdb-movies-explorer/
├── app.py                    # Main Streamlit application
├── data/
│   └── trimmed_movies.csv    # TMDB dataset (10,000 movies)
└── README.md                 # Documentation
```

## Technologies

- **Streamlit**: Web framework for data apps
- **Pandas**: Data manipulation
- **Altair**: Statistical visualization
- **NumPy**: Regression calculations