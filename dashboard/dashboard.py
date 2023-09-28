import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime
import base64
from pathlib import Path

# Fungsi pembuatan DataFrame berdasarkan atribut dan Grafik
def create_and_plot_attribute(df, attribute, title):
    by_attribute_df = df.groupby(by=attribute).instant.nunique().reset_index()
    by_attribute_df.rename(columns={"instant": "count"}, inplace=True)

    st.subheader(title)
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.barplot(
        x=attribute,
        y="count",
        data=by_attribute_df.sort_values(by=by_attribute_df.columns[1], ascending=False),
        ax=ax
    )
    ax.set_title(title, loc="center", fontsize=30)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis="y", labelsize=20)
    ax.tick_params(axis="x", labelsize=15)
    st.pyplot(fig)

# Fungsi untuk menampilkan sidebar
def sidebar(df):
    df["datetime"] = pd.to_datetime(df["datetime"])
    min_date = df["datetime"].min()
    max_date = df["datetime"].max()

    with st.sidebar:
        if 'logo' not in st.session_state:
            file_ = open("dashboard/logo.gif", "rb")
            contents = file_.read()
            data_url = base64.b64encode(contents).decode("utf-8")
            file_.close()
            st.session_state.logo = data_url

        centered_image = f'<div style="display: flex; justify-content: center; margin-bottom: 50px;"><img src="data:image/gif;base64,{st.session_state.logo}" alt="cat gif"></div>'
        st.markdown(centered_image, unsafe_allow_html=True)

        def on_change():
            st.session_state.date = date

        date = st.date_input(
            label="Start Date - End Date", 
            min_value=min_date, 
            max_value=max_date,
            value=[min_date, max_date],
            on_change=on_change
        )

    return date

if __name__ == "__main__":
    st.header("Dashboard Bike Sharing :man-biking:")

    # Memanggil file days_clean.csv
    days_df_csv = Path(__file__).parents[1] / 'dashboard/days_clean.csv'
    days_df = pd.read_csv(days_df_csv)

    date = sidebar(days_df)

    if len(date) == 2:
        selected_date_range = (str(date[0]), str(date[1]))
    else:
        selected_date_range = (str(st.session_state.date[0]), str(st.session_state.date[1]))

    main_df = days_df[(days_df["datetime"] >= selected_date_range[0]) & (days_df["datetime"] <= selected_date_range[1])]

    st.subheader('Daily Rent Bike Sharing')
    col1, col2, col3 = st.columns(3)

    st.markdown("""
    <style>
    div[data-testid="metric-container"] {
    background-color: rgba(201,234,184, 0.4);
    border: 1px solid rgba(201,234,184, 0.5);
    padding: 5% 5% 5% 10%;
    border-radius: 5px;
    color: rgb(30, 103, 119);
    overflow-wrap: break-word;
    }

    /* breakline for metric text         */
    div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
    overflow-wrap: break-word;
    white-space: break-spaces;
    color: red;
    }
    </style>
    """
    , unsafe_allow_html=True)

    with col1:
        daily_rent_casual = main_df['casual'].sum()
        st.metric('Casual user', value=f'{daily_rent_casual:,}')

    with col2:
        daily_rent_registered = main_df['registered'].sum()
        st.metric('Registered user', value=f'{daily_rent_registered:,}')

    with col3:
        daily_rent_total = main_df['count'].sum()
        st.metric('Total order', value=f'{daily_rent_total:,}')
        
    attributes = ["season", "weather_condition", "weekday","month", "year"]

    for attribute in attributes:
        create_and_plot_attribute(main_df, attribute, f"Number of Bike Sharing by {attribute.capitalize()}")

    year_copyright = datetime.date.today().year
    copyright_dashboard = f"Copyright © {year_copyright} All Rights Reserved [Ahmad Ikhsan Maulana](https://www.linkedin.com/in/ahmadikhsanmaulana/)"
    st.caption(copyright_dashboard)