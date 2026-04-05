import streamlit as st
import time
from datetime import datetime
import pandas as pd  # Using pandas to create a table
import requests
from config import API_KEY

def extended_status(key):
    if "hospital" not in api_response["members"][key]["status"]["description"]: 
        return api_response["members"][key]["status"]["description"] 
    else:
        return api_response["members"][key]["status"]["state"]

# Function to format the remaining time
def format_remaining_time(total_seconds):
    total_seconds = int(total_seconds)
    if total_seconds > 0:
        return "{:02d}:{:02d}:{:02d}".format(
            total_seconds // 3600,
            (total_seconds // 60) % 60,
            total_seconds % 60,
        )
    return " "

def make_clickable(link, name):
    return f'<a href="{link}" target="_blank">{name}</a>'

enemyFactionId = 20659

api_response = requests.get("https://api.torn.com/faction/" + str(enemyFactionId)+ "?selections=&key=" + API_KEY).json()
# Title of the tab and inapp title

faction_name = api_response["name"]
st.set_page_config(page_title=faction_name)
st.markdown(f"<h1>Faction snapshot: <a href='https://www.torn.com/factions.php?step=profile&ID={enemyFactionId}' target='_blank' style='color: red; text-decoration: none;'>{faction_name}</a></h1>", unsafe_allow_html=True)

# compile all the relevant data into an array
member_data = [
    [
        api_response["members"][key]["name"],
        api_response["members"][key]["level"],
        extended_status(key),
        int(api_response["members"][key]["status"]["until"]),
        f"https://www.torn.com/loader2.php?sid=getInAttack&user2ID={key}"
    ]
    for key in api_response["members"]
]

# Create a placeholder to hold the data table
table_placeholder = st.empty()

# dataframe will be initialized in the update loop

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
    global api_response, member_data
    last_api_fetch = time.time()
    
    while True:
        current_time = time.time()
        
        # Fetch fresh data from API every 5 seconds to stay updated
        if current_time - last_api_fetch > 5:
            try:
                new_response = requests.get("https://api.torn.com/faction/" + str(enemyFactionId)+ "?selections=&key=" + API_KEY).json()
                if "error" not in new_response:
                    api_response = new_response
                    member_data = [
                        [
                            api_response["members"][key]["name"],
                            api_response["members"][key]["level"],
                            extended_status(key),
                            int(api_response["members"][key]["status"]["until"]),
                            f"https://www.torn.com/loader2.php?sid=getInAttack&user2ID={key}"
                        ]
                        for key in api_response["members"]
                    ]
                last_api_fetch = current_time
            except Exception:
                pass # Fallback to existing data if the request fails
                
        # Create a list to store the rows of the table,
        # Iterate over the timestamps and calculate the remaining time
        table_rows = [
            [
                make_clickable(member_data[j][4],member_data[j][0]),
                member_data[j][1],
                member_data[j][2],
                format_remaining_time(member_data[j][3] - current_time) if member_data[j][3] != 0 else " "
            ] for j in range(len(member_data))
        ]
        table_rows.sort(key=lambda x: ((x[2] == "Okay", x[2]), (x[3] == " ", x[3]), -x[1]))
        
        # Update the dataframe
        df = pd.DataFrame(table_rows, columns=["Name", "lvl", "Status", "Time Remaining"])
        df.index = pd.RangeIndex(start=1, stop=len(df) + 1, step=1)

        # Display the table
        st.markdown(css, unsafe_allow_html=True)
        table_placeholder.write(df.to_html(escape=False, index=True), unsafe_allow_html=True)

        # Sleep for 1 second before updating the timers
        time.sleep(1)

update_countdown_table()