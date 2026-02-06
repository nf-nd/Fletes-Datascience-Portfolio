import streamlit as st

st.title("Hello, Streamlit!")
st.write("This is my first streamlit app.")

if st.button("Click me!"):
    st.write("You clicked a button!")
else:
    st.write("You haven't clicked the button yet.")

import pandas as pd

### Loading our csv file
st.subheader("Exploring Out Dataset")

#Load the CSV file
df = pd.read_csv("data/sample_data-1.csv")

st.write("Full Dataset:")
st.dataframe(df)

st.write("Select a city")

st.markdown("""
    <style>
    div[data-baseweb="select"] > div {
        border-color: blue !important;
    }
    </style>
    """, unsafe_allow_html=True)

city = st.selectbox("Select a city", df['City'].unique())
filtered_df = df[df["City"] == city]

st.write(f"People in [{city}]:")
st.dataframe(filtered_df)

st.write(df.describe())
st.bar_chart(df["Salary"])

import seaborn as sns

box_plot = sns.boxplot(x=df["City"], y=df["Salary"])
st.pyplot(box_plot.get_figure())

