import streamlit as st
import time
from datetime import datetime, timedelta
import random
import pandas as pd  # Using pandas to create a table
import requests
from config import API_KEY

def make_clickable(name, link):
    return f'<a href="{link}" target="_blank">{name}</a>'

enemyFactionId = 39580

api_response = requests.get("https://api.torn.com/faction/" + str(enemyFactionId)+ "?selections=&key=" + API_KEY).json()
# Title of the tab and inapp title

faction_name = api_response["name"]
st.set_page_config(page_title=faction_name)
st.title(f"Ranked War Tracker: {faction_name}")

# compile all the relevant data into an array
member_data = [
    [
        api_response["members"][key]["name"],
        api_response["members"][key]["level"],
        api_response["members"][key]["status"]["state"],
        int(api_response["members"][key]["status"]["until"]),
        f"https://www.torn.com/loader2.php?sid=getInAttack&user2ID={key}"
    ]
    for key in api_response["members"]
]

# Create a placeholder to hold the countdown table
table_placeholder = st.empty()

# Function to format the remaining time
def format_remaining_time(remaining_time):
    return "{:02d}:{:02d}:{:02d}".format(
        remaining_time.seconds // 3600,
        (remaining_time.seconds // 60) % 60,
        remaining_time.seconds % 60,
    ) if remaining_time.total_seconds() > 0 else " "

# intialize the dataframe and an array of shape(number of members, 4)
table_rows = [[0 for _ in range(4)] for _ in range(len(member_data))]
df = pd.DataFrame(table_rows, columns=["Name","lvl","Status","Time Remaining"])

# add a serial number column in the table
df.index = pd.RangeIndex(start=1, stop=len(df) + 1, step=1)

css = """
<style>
table {
    width: 100%;
    table-layout: auto;
}
th, td {
    padding: 10px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}
</style>
"""

# Continuously update the countdown timers
def update_countdown_table():
    while True:
        current_time = datetime.now()
        
        # Create a list to store the rows of the table,
        # Iterate over the timestamps and calculate the remaining time
        table_rows = [
            [
                make_clickable(member_data[j][0],member_data[j][4]),
                member_data[j][1],
                member_data[j][2],
                format_remaining_time(
                    datetime.fromtimestamp(member_data[j][3]) - current_time
                ) if member_data[j][3] != 0 else " "
            ] for j in range(len(member_data))
        ]
        table_rows.sort(key=lambda x: (x[3] == " ", x[1]))
        
        # Update the dataframe
        df.loc[:, :] = table_rows

        # Display the table
        #table_placeholder.table(df)
        st.markdown(css, unsafe_allow_html=True)
        table_placeholder.write(df.to_html(escape=False, index=True), unsafe_allow_html=True)

        # Sleep for 1 second before updating the timers
        time.sleep(1)

update_countdown_table()