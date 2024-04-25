import streamlit as st
import pandas as pd 
import numpy as np
import plotly.express as px
# import matplotlib.pyplot as plt
# import seaborn as sns
# %matplotlib inline

epl_df = pd.read_csv("EPL_20_21.csv")

st.title("EPL 20-21 Football stats analysis")

st.subheader("1. Header of csv file:")
st.write(epl_df.head())


st.subheader("2. Info about csv file:")
st.write(epl_df.describe())


st.subheader("3. Two more columns created Min/match and Goals/match:")
epl_df['MinsPerMatch']=(epl_df['Mins']/epl_df['Matches']).astype(int)
epl_df['GoalsPerMatch']=(epl_df['Goals']/epl_df['Matches']).astype(float)
st.write(epl_df.head())


st.subheader("4. Total goals scored in EPL: ")
Total_Goals = epl_df['Goals'].sum()
st.title(Total_Goals)


st.subheader("4. Total penalty attemps in EPL: ")
Total_penaltyAttempts = epl_df['Penalty_Attempted'].sum()
st.title(Total_penaltyAttempts)


st.subheader("5. Total Penalty Goals: ")
Total_penaltyGoals = epl_df['Penalty_Goals'].sum()
st.title(Total_penaltyGoals)


st.subheader("6. Pie chart of penaltiy outcome: ")
pl_not_scored = epl_df['Penalty_Attempted'].sum() - Total_penaltyGoals
data = [pl_not_scored, Total_penaltyGoals]
labels = ['Penalties Missed', 'Penalties Scored']
fig = px.pie(values=data, names=labels, 
             title="Penalty Outcomes in Premier League")  # color palette
st.plotly_chart(fig)


st.subheader("7. Uniques positions of players: ")
st.write(epl_df['Position'].unique())


st.subheader("8. Find players by their playing position: ")
posIp = st.text_input("Enter playing position")
playerPosList = epl_df[epl_df['Position']==posIp]
st.write(playerPosList)


st.subheader("9. Nationality of players playing in Premier League:")
nationality = epl_df.groupby('Nationality').size().sort_values(ascending=False)
top_10_nationality = nationality.head(10)
fig = px.bar(top_10_nationality,
             x=top_10_nationality.index,  # Set x-axis as nationality labels
             y=top_10_nationality.values,  # Set y-axis as nationality counts
             title="Top 10 Nationalities (Players)"
             )
st.plotly_chart(fig)


st.subheader("10. Club with maximun number of player: ")
top_5_clubs = epl_df['Club'].value_counts().nlargest(5)
fig = px.bar(top_5_clubs,
             x=top_5_clubs.index,  # Set x-axis as club names
             y=top_5_clubs.values,  # Set y-axis as player counts
             title="Top 5 Clubs by Player Count"
             )
st.plotly_chart(fig)


st.subheader("11. Clubs with minimum number of players: ")
bottom_5_clubs = epl_df['Club'].value_counts().nsmallest(5)
fig = px.bar(bottom_5_clubs,
             x=bottom_5_clubs.index,  # Set x-axis as club names
             y=bottom_5_clubs.values,  # Set y-axis as player counts
             title="Bottom 5 Clubs by Player Count"
             )
st.plotly_chart(fig)


st.subheader("12. Pie chart of age group of players:")
age_groups = {
    "<=20": (epl_df["Age"] <= 20),
    ">20 & <=25": (epl_df["Age"] > 20) & (epl_df["Age"] <= 25),
    ">25 & <=30": (epl_df["Age"] > 25) & (epl_df["Age"] <= 30),
    ">30": epl_df["Age"] > 30
}
player_counts = {group: epl_df[filter_condition]["Name"].count() for group, filter_condition in age_groups.items()}
fig = px.pie(player_counts.items(),
             names=player_counts.keys(),
             values=player_counts.values(),
             title="Total Players by Age Group",
             labels=player_counts.keys()  # Set labels explicitly
             )
st.plotly_chart(fig)


st.subheader("13. Distribution of players under 20: ")
players_under_20 = epl_df[epl_df['Age'] < 20]
club_counts = players_under_20['Club'].value_counts()
fig = px.bar(club_counts,
             x=club_counts.index,  # Set x-axis as club names
             y=club_counts.values,  # Set y-axis as player counts
             )
st.plotly_chart(fig)


st.subheader("14. Under 20 player in clubs: ")
clubName = st.text_input("Enter name of club:")
under20_players = epl_df[(epl_df['Club'] == clubName) & (epl_df['Age'] < 20)]
if not under20_players.empty:  # Check if there are any players
    st.header("Under 20 player in ", clubName)
    st.dataframe(under20_players)  # Display DataFrame
else:
    st.info("No players under age 20 found ")


st.subheader("15. Average age of players in each club: ")
fig = px.box(epl_df, x="Club", y="Age", title="Age Distribution Across Clubs")
st.plotly_chart(fig)


st.subheader("16. Average of of players in each club: ")
average_age = (epl_df.groupby('Club')['Age'].sum()) / epl_df.groupby('Club').size()
average_age = average_age.sort_values(ascending=False)
st.dataframe(average_age)


st.subheader("17. Total assists by each club:")
Assists_by_clubs = pd.DataFrame(epl_df.groupby('Club', as_index=False)['Assists'].sum())
Assists_by_clubs = Assists_by_clubs.sort_values(by="Assists", ascending=False)
fig = px.bar(Assists_by_clubs, x="Club", y="Assists", title="Total Assists by Club")
fig.update_layout(
    xaxis_title="Club",
    yaxis_title="Total Assists"
)
st.plotly_chart(fig)


st.subheader("18. Total goals by each club:")
Goals_by_clubs = pd.DataFrame(epl_df.groupby('Club', as_index=False)['Goals'].sum())
Goals_by_clubs = Goals_by_clubs.sort_values(by="Goals", ascending=False)
fig = px.bar(Goals_by_clubs, x="Club", y="Goals", title="Total Goals by Club")
fig.update_layout(
    xaxis_title="Club",
    yaxis_title="Total Goals",
)
st.plotly_chart(fig)

st.subheader("19. Pie chart of goals with or without assist:")
total_goals = epl_df['Goals'].sum()
assists = epl_df['Assists'].sum()
goals_without_assists = total_goals - assists
data = [goals_without_assists, assists]
labels = ['Goals without Assists', 'Goals with Assists']
fig = px.pie(values=data, names=labels, title="Goals Distribution (With/Without Assists)")
st.plotly_chart(fig)


st.subheader("20. Find top players by stats:")
field = st.text_input("Enter which stat you want to find", "Eg. Goals, Assists, Yellow_Cards, Red_Cards")
if field in epl_df.columns:
  topPlayers = epl_df[['Name','Club',field,'Matches']].nlargest(n=10, columns=field)
  st.write(topPlayers)
else:
  st.error(f"Stat '{field}' not found in data. Please try again.")



# test