# Import modules
import matplotlib.pyplot as plt
from pandas.core import base
import streamlit as st
import seaborn as sns
import pandas as pd
import numpy as np
import base64

st.title("NFL Footbal Stats Explorer")

st.markdown("""
This app simple scraping of NFL Football player stats data (Rushing only)\n
Source: [Pro-Football-Reference](https://www.pro-football-reference.com/)
""")

st.sidebar.header("User Input Features")
selected_year = st.sidebar.selectbox("Year", list(reversed(range(1990, 2021))))


@st.cache
def load_data(year):
    url = "https://www.pro-football-reference.com/years/" + \
        str(year) + "/rushing.htm"
    html = pd.read_html(url, header=1)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index)
    raw = raw.fillna(0)
    player_stats = raw.drop(['Rk'], axis=1)
    return player_stats


player_stats = load_data(selected_year)

# Sidebar - Team Selection
sorted_unique_team = sorted(player_stats.Tm.unique())
selected_team = st.sidebar.multiselect(
    "Team", sorted_unique_team, sorted_unique_team)

# Sidebar - Position Selection
unique_pos = ['RB', 'QB', 'WR', 'FB', 'TE']
selected_pos = st.sidebar.multiselect("Position", unique_pos, unique_pos)

# Filtering Data
df_selected_team = player_stats[(player_stats.Tm.isin(
    selected_team)) & (player_stats.Pos.isin(selected_pos))]

st.header("Display Player Stats of Selected Team(s)")
st.write("Data Dimension: " + str(df_selected_team.shape[0]) + ' rows and ' + str(
    df_selected_team.shape[1]) + ' columns')
st.dataframe(df_selected_team)


def filedownload(df):
    csv = df.to_csv(index=False)
    # string <-> bytes conversion
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href


st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

# Heatmap
if st.button("Intercorrelation Heatmap"):
    st.header("Intercorrelation Matrix Heatmap")
    df_selected_team.to_csv("output.csv", index=False)
    df = pd.read_csv("output.csv")

    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(10, 8))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot(f)
