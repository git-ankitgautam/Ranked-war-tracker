import streamlit as st
import time
from datetime import datetime
import pandas as pd
import requests

st.set_page_config(page_title="Ranked War Tracker")

def extended_status(key, api_response):
    if "hospital" not in api_response["members"][key]["status"]["description"]: 
        s = api_response["members"][key]["status"]["description"] 
    else:
        s = api_response["members"][key]["status"]["state"]
        
    # Prepend invisible zero-width characters to force Streamlit frontend sorting
    # \u200b (Okay) -> \u200c (Travel) -> \u200d (Hospital) -> \u200e (Other)
    s_lower = s.lower()
    if s == "Okay":
        return "\u200b" + s
    elif "travel" in s_lower or "return" in s_lower or s_lower.startswith("in "):
        return "\u200c" + s
    elif s == "Hospital":
        return "\u200d" + s
    else:
        return "\u200e" + s

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
    # We append the name as a URL fragment so Streamlit's LinkColumn can extract it
    return f"{link}#name={name}"

def update_countdown_table(enemy_faction_id, api_key, initial_api_response):
    table_placeholder = st.empty()
    api_response = initial_api_response
    
    if "members" not in api_response:
        st.error("No members found or invalid response.")
        return

    member_data = [
        [
            api_response["members"][key]["name"],
            api_response["members"][key]["level"],
            extended_status(key, api_response),
            int(api_response["members"][key]["status"]["until"]),
                            f"https://www.torn.com/loader2.php?name={api_response['members'][key]['name']}&sid=getInAttack&user2ID={key}"
        ]
        for key in api_response["members"]
    ]
    
    last_api_fetch = time.time()
    
    while True:
        current_time = time.time()
        
        # Fetch fresh data from API every 3 seconds to stay updated
        if current_time - last_api_fetch > 3:
            try:
                new_response = requests.get("https://api.torn.com/faction/" + str(enemy_faction_id)+ "?selections=&key=" + api_key).json()
                if "error" not in new_response and "members" in new_response:
                    api_response = new_response
                    member_data = [
                        [
                            api_response["members"][key]["name"],
                            api_response["members"][key]["level"],
                            extended_status(key, api_response),
                            int(api_response["members"][key]["status"]["until"]),
                            f"https://www.torn.com/loader2.php?name={api_response['members'][key]['name']}&sid=getInAttack&user2ID={key}"
                        ]
                        for key in api_response["members"]
                    ]
                last_api_fetch = current_time
            except Exception:
                pass # Fallback to existing data if the request fails
                
        # Create a list to store the rows of the table
        table_rows = [
            [
                make_clickable(member_data[j][4],member_data[j][0]),
                member_data[j][1],
                member_data[j][2],
                format_remaining_time(member_data[j][3] - current_time) if member_data[j][3] != 0 else " "
            ] for j in range(len(member_data))
        ]
        table_rows.sort(key=lambda x: (x[2], (x[3] == " ", x[3]), -x[1]))
        
        # Update the dataframe
        df = pd.DataFrame(table_rows, columns=["Name", "lvl", "Status", "Time Remaining"])
        df.index = pd.RangeIndex(start=1, stop=len(df) + 1, step=1)

        # Display the table natively to allow column sorting
        table_placeholder.dataframe(
            df,
            use_container_width=True,
            column_config={
                "Name": st.column_config.LinkColumn(
                    "Name",
                    display_text=r"#name=(.*)$"
                )
            }
        )

        # Sleep for 1 second before updating the timers
        time.sleep(1)

# Main app flow
if 'api_key' not in st.session_state or 'faction_id' not in st.session_state:
    st.title("Ranked War Tracker Setup")
    with st.form("setup_form"):
        api_key_input = st.text_input("Enter your Torn API Key:", type="password")
        faction_id_input = st.text_input("Enter Target Faction ID:")
        submitted = st.form_submit_button("Start Tracking")
        
        if submitted:
            if api_key_input and faction_id_input:
                st.session_state['api_key'] = api_key_input
                st.session_state['faction_id'] = faction_id_input
                if hasattr(st, 'rerun'):
                    st.rerun()
                else:
                    st.experimental_rerun()
            else:
                st.error("Please provide both API Key and Faction ID.")
else:
    api_key = st.session_state['api_key']
    faction_id = st.session_state['faction_id']
    
    col1, col2 = st.columns([0.8, 0.2])
    with col2:
        if st.button("Change Settings", use_container_width=True):
            del st.session_state['api_key']
            del st.session_state['faction_id']
            if hasattr(st, 'rerun'):
                st.rerun()
            else:
                st.experimental_rerun()
        
    try:
        response = requests.get("https://api.torn.com/faction/" + str(faction_id)+ "?selections=&key=" + api_key).json()
        if "error" in response:
            st.error(f"Error from API: {response['error'].get('error', 'Invalid API Key or Faction ID')}")
        else:
            faction_name = response.get("name", "Unknown Faction")
            with col1:
                st.markdown(f"<h1>Faction snapshot: <a href='https://www.torn.com/factions.php?step=profile&ID={faction_id}' target='_blank' style='color: red; text-decoration: none;'>{faction_name}</a></h1>", unsafe_allow_html=True)
            
            # Start loop
            update_countdown_table(faction_id, api_key, response)
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")
