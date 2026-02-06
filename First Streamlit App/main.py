# Import required libraries
import streamlit as st  # Web app framework
import pandas as pd  # Data manipulation and analysis
import altair as alt  # Declarative visualization library
import numpy as np  # Numerical computing


# ============================================================================
# PAGE HEADER AND INTRODUCTION
# ============================================================================

# Set up page title and introduction
st.title("IMDB Movies — Dataset Explorer")
st.title("Interactive Exploratory Analysis")
st.title("Project 1 — MDSC 20009")
st.write("This interactive dashboard provides tools to explore the IMDB Movies dataset. Use the controls to filter data, compare variables, and inspect trends, distributions, and aggregated summaries.")

# Provide dataset description
st.write("This dataset is a collection of 10000 movies pulled from The Movie Database (TMDB) API, packaged into a single 196MB CSV file . It includes 20 different columns covering everything you'd want to know about a film—titles, genres, cast and crew, plot keywords, budgets, revenue, release dates, languages, production companies, vote counts, reviews, and recommendations . The movies span from the late 1900s to 2024, with about half being English-language films and a heavy representation of documentaries at 29 percent of the collection. The dataset is from Kaggle and was released under a public domain license, making it ideal for a school project.")


# ============================================================================
# DATA LOADING AND COLUMN DEFINITIONS
# ============================================================================

# Load the movie dataset from CSV
df = pd.read_csv("First Streamlit App/data/trimmed_movies.csv")

# Define all available columns in the complete dataset
complete_column_names = [
    'id',
    'title',
    'genres',
    'original_language',
    'overview',
    'popularity',
    'production_companies',
    'release_date',
    'budget',
    'revenue',
    'runtime',
    'status',
    'tagline',
    'vote_average',
    'vote_count',
    'credits',
    'keywords',
    'poster_path',
    'backdrop_path',
    'recommendations'
]

# Define subset of columns to display in data table
truncated_column_names = [
    'title',
    'genres',
    'original_language',
    'popularity',
    'production_companies',
    'release_date',
    'budget',
    'revenue',
    'runtime',
    'vote_average',
    'vote_count',
    'keywords'
]

# Define columns containing numerical data for quantitative analysis
numerical_column_names = [
    'popularity',
    'budget',
    'revenue',
    'runtime',
    'vote_average',
    'vote_count'
]

# Define columns containing categorical data for grouping and aggregation
categorical_column_names = [
    'original_language',
    'genres',
    'production_companies'
]


# ============================================================================
# INTERACTIVE DATA TABLE
# ============================================================================

st.write("Dataset preview — top movies by popularity:")

# Create dropdown menu to select which column to sort by
sort_column = st.selectbox(
    'Sort by:', 
    truncated_column_names, 
    index=truncated_column_names.index('popularity')  # Default to popularity
)

# Display the dataframe sorted by the selected column in descending order
st.dataframe(df[truncated_column_names].sort_values(sort_column, ascending=False))


# ============================================================================
# SCATTER PLOT VISUALIZATION
# ============================================================================

st.subheader("Scatter Plot")
st.write("Choose a pre-defined comparison or select custom numeric variables to visualize relationships between features.")

# Define predefined scatter plot comparisons (label, x-variable, y-variable)
comparison_options = [
    ("Budget vs Revenue", "budget", "revenue"),
    ("Budget vs Popularity", "budget", "popularity"),
    ("Revenue vs Popularity", "revenue", "popularity"),
    ("Runtime vs Revenue", "runtime", "revenue"),
    ("Vote Average vs Popularity", "vote_average", "popularity"),
    ("Other [Custom Comparison]", None, None)  # Custom option for user-defined axes
]

# Extract just the comparison names for the dropdown
comparison_names = [opt[0] for opt in comparison_options]

# Create dropdown for selecting scatter plot comparison
selected_comparison = st.selectbox("Select comparison:", comparison_names, index=0)

# Find the selected option and extract its preset x and y variables
selected_idx = comparison_names.index(selected_comparison)
_, preset_x, preset_y = comparison_options[selected_idx]

# If custom comparison is selected, show dropdowns for x and y axis selection
if preset_x is None and preset_y is None:
    col1, col2 = st.columns(2)
    with col1:
        x_var = st.selectbox("X-axis:", numerical_column_names, index=0)
    with col2:
        y_var = st.selectbox("Y-axis:", numerical_column_names, index=min(1, len(numerical_column_names)-1))
else:
    # Use preset values from the selected comparison, with fallback defaults
    x_var = preset_x if preset_x in numerical_column_names else numerical_column_names[0]
    y_var = preset_y if preset_y in numerical_column_names else numerical_column_names[0]

# Add checkbox to toggle trendline display
show_trendline = st.checkbox("Show trendline", value=False)

# ============================================================================
# DATA FILTERING FOR SCATTER PLOT
# ============================================================================

# Create a copy of the dataframe for plotting
df_plot = df.copy()

# Filter to top 10,000 movies by popularity
if 'popularity' in df_plot.columns:
    df_plot = df_plot.sort_values('popularity', ascending=False).head(10000)

# Remove top 10 outliers by budget and revenue to improve visualization scale
to_drop = set()
for col in ['budget', 'revenue']:
    if col in df_plot.columns:
        # Get indices of top 10 values for each column
        top_idx = pd.to_numeric(df_plot[col], errors='coerce').nlargest(10).index
        to_drop.update(top_idx)

# Drop the outlier indices
df_plot = df_plot.drop(index=list(to_drop), errors='ignore')

# Build plotting dataframe with selected x and y variables
plot_df = pd.DataFrame({
    x_var: pd.to_numeric(df_plot[x_var], errors='coerce') if x_var in df_plot.columns else [],
    y_var: pd.to_numeric(df_plot[y_var], errors='coerce') if y_var in df_plot.columns else []
})

# Add title column for tooltip display if available
if 'title' in df_plot.columns:
    plot_df['title'] = df_plot['title'].values

# Remove rows with missing values in x or y columns
valid_df = plot_df.dropna(subset=[x_var, y_var])
st.info(f"Plotting {len(valid_df)} datapoints")

# ============================================================================
# RENDER SCATTER PLOT
# ============================================================================

if not valid_df.empty:
    # Create base scatter plot with interactive zoom/pan
    scatter = (
        alt.Chart(valid_df)
        .mark_circle(opacity=0.6, size=60)
        .encode(
            x=alt.X(x_var, type='quantitative', title=x_var),
            y=alt.Y(y_var, type='quantitative', title=y_var),
            tooltip=['title', x_var, y_var] if 'title' in valid_df.columns else [x_var, y_var]
        )
        .interactive()
    )
    
    # Add trendline if checkbox is selected
    if show_trendline:
        # Calculate linear regression statistics manually
        x_vals = valid_df[x_var].astype(float).values
        y_vals = valid_df[y_var].astype(float).values
        
        # Check if we have enough data points for regression
        if len(x_vals) >= 2 and np.all(np.isfinite(x_vals)) and np.all(np.isfinite(y_vals)):
            # Fit linear regression: y = slope * x + intercept
            slope, intercept = np.polyfit(x_vals, y_vals, 1)
            # Calculate correlation coefficient and R-squared
            corr = np.corrcoef(x_vals, y_vals)[0, 1]
            r_squared = float(corr ** 2) if np.isfinite(corr) else float('nan')
        else:
            # Set to NaN if insufficient data
            slope = float('nan')
            intercept = float('nan')
            r_squared = float('nan')
        
        # Display regression statistics below the plot
        st.write(f"Regression statistics — **Slope:** {slope:.4f} | **Intercept:** {intercept:.2f} | **R²:** {r_squared:.4f}")
        
        # Create trendline layer using Altair's transform_regression
        trend = (
            alt.Chart(valid_df)
            .mark_line(color='red', size=3)
            .transform_regression(x_var, y_var)
            .encode(
                x=alt.X(x_var, type='quantitative'),
                y=alt.Y(y_var, type='quantitative')
            )
        )
        # Combine scatter plot and trendline
        chart = scatter + trend
    else:
        chart = scatter
    
    # Render the final chart
    st.altair_chart(chart, use_container_width=True)


# ============================================================================
# BAR CHART VISUALIZATION
# ============================================================================

# Define predefined bar chart comparisons (label, categorical x, numerical y)
barchart_comparison_options = [
    ("Original Language vs Popularity", "original_language", "popularity"),
    ("Production Company vs Popularity", "production_companies", "popularity"),
    ("Genre vs Revenue", "genres", "revenue"),
    ("Other [Custom Comparison]", None, None)  # Custom option for user-defined comparison
]

# Extract comparison names for dropdown
barchart_comparison_names = [opt[0] for opt in barchart_comparison_options]

# Create dropdown for selecting bar chart comparison
selected_comparison = st.selectbox("Select comparison:", barchart_comparison_names, index=0, key="barchart_comparison")

# Find the selected option and extract its preset x and y variables
selected_idx = barchart_comparison_names.index(selected_comparison)
_, preset_x, preset_y = barchart_comparison_options[selected_idx]

# If custom comparison is selected, show dropdowns for x (categorical) and y (numerical) selection
if preset_x is None and preset_y is None:
    col1, col2 = st.columns(2)
    with col1:
        x_var = st.selectbox("X-axis (categorical):", categorical_column_names, index=0, key="barchart_x")
    with col2:
        y_var = st.selectbox("Y-axis (will be averaged):", numerical_column_names, index=min(1, len(numerical_column_names)-1), key="barchart_y")
else:
    # Use preset values from the selected comparison, with fallback defaults
    x_var = preset_x if preset_x in df.columns else categorical_column_names[0]
    y_var = preset_y if preset_y in numerical_column_names else numerical_column_names[0]

# ============================================================================
# DATA FILTERING FOR BAR CHART
# ============================================================================

# Create a copy of the dataframe for plotting
df_plot = df.copy()

# Filter to top 10,000 movies by popularity
if 'popularity' in df_plot.columns:
    df_plot = df_plot.sort_values('popularity', ascending=False).head(10000)

# Remove top 10 outliers by budget and revenue
to_drop = set()
for col in ['budget', 'revenue']:
    if col in df_plot.columns:
        # Get indices of top 10 values for each column
        top_idx = pd.to_numeric(df_plot[col], errors='coerce').nlargest(10).index
        to_drop.update(top_idx)

# Drop the outlier indices
df_plot = df_plot.drop(index=list(to_drop), errors='ignore')

# Build plotting dataframe with categorical x and numerical y
plot_df = pd.DataFrame({
    x_var: df_plot[x_var] if x_var in df_plot.columns else [],
    y_var: pd.to_numeric(df_plot[y_var], errors='coerce') if y_var in df_plot.columns else []
})

# Extract first value before dash for genre and production company columns
# (handles multi-genre/multi-company entries by taking primary value)
if any(keyword in x_var.lower() for keyword in ['genre', 'production']):
    plot_df[x_var] = plot_df[x_var].astype(str).str.split('-').str[0].str.strip()

# Remove Latin language entries when grouping by language (often data quality issues)
if x_var == 'original_language' and x_var in plot_df.columns:
    plot_df = plot_df[plot_df['original_language'].astype(str).str.lower().str.strip() != 'la']

# Filter out production companies with fewer than 15 movies (reduces noise)
if 'production' in x_var.lower():
    # Count occurrences of each production company
    company_counts = plot_df[x_var].value_counts()
    # Keep only companies with 15+ movies
    valid_companies = company_counts[company_counts >= 15].index
    # Filter dataframe to only include these companies
    plot_df = plot_df[plot_df[x_var].isin(valid_companies)]

# Remove rows with missing values in the numerical y column
valid_df = plot_df.dropna(subset=[y_var])
st.info(f"Plotting {len(valid_df)} datapoints")

# ============================================================================
# RENDER BAR CHART
# ============================================================================

if not valid_df.empty:
    # Group by categorical variable and calculate mean and count
    agg_df = valid_df.groupby(x_var, observed=True).agg({
        y_var: ['mean', 'count']
    }).reset_index()
    
    # Flatten multi-level column names
    agg_df.columns = ['category', 'mean_value', 'count']
    
    # Create bar chart showing average values per category
    bar_chart = (
        alt.Chart(agg_df)
        .mark_bar()
        .encode(
            x=alt.X('category:N', title=x_var, axis=alt.Axis(labelAngle=-45)),  # Angled labels for readability
            y=alt.Y('mean_value:Q', title=f"Average {y_var}"),
            tooltip=[
                alt.Tooltip('category:N', title=x_var),
                alt.Tooltip('mean_value:Q', title=f"Avg {y_var}", format='.2f'),
                alt.Tooltip('count:Q', title='Count')
            ]
        )
        .properties(height=400)
    )
    
    # Render the bar chart
    st.altair_chart(bar_chart, use_container_width=True)
    
    # Display summary statistics about the aggregated data
    st.write(f"Aggregate summary — **Total categories:** {len(agg_df)} | **Average datapoints per category:** {agg_df['count'].mean():.1f}")
