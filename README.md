# Ranked War Tracker

A real-time Streamlit web application designed for the browser-based MMORPG [Torn](https://www.torn.com/). This tool allows you to actively monitor the status of any faction's members during Ranked Wars, chaining, or general gameplay. 

It provides an auto-updating dashboard showing member levels, current statuses (Hospital, Travel, Jail, etc.), and precise countdown timers for when members will be out of their current state.

## Features

- **Real-Time Polling:** Automatically fetches fresh data from the Torn API every 5 seconds to ensure you always have the latest statuses during fast-paced wars.
- **Dynamic Countdown Timers:** Calculates and displays precise countdowns (HH:MM:SS) for members in the Hospital, traveling, or in Federal Jail, updating locally every second.
- **Secure Setup:** Enter your Torn API key and target Faction ID directly through the UI. The API key is masked and stored securely in your local session state, eliminating the need to hardcode sensitive information.
- **Quick Attack Links:** Player names are rendered as clickable links that instantly open the Torn "Attack" page for that specific user, allowing for rapid deployment.
- **Smart Sorting:** Automatically sorts the faction roster to prioritize targets. Members who are "Okay" (ready to be attacked) are grouped together, and it sorts by level and remaining time for efficient target selection.
- **Clean Interface:** Built with Streamlit and Pandas for a clean, easy-to-read tabular layout.

## Prerequisites

Before running this application, make sure you have the following installed:
- Python 3.7 or higher
- `pip` (Python package installer)

You will also need a valid **Torn API Key** with public access permissions to retrieve faction data.

## Installation

1. Clone or download this repository to your local machine.
2. Open your terminal or command prompt and navigate to the project directory:
   ```bash
   cd "path/to/Ranked war tracker"
   ```
3. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(If you don't have a `requirements.txt`, you can install the dependencies directly: `pip install streamlit pandas requests`)*

## Usage

1. Start the Streamlit application by running the following command in your terminal:
   ```bash
   streamlit run main.py
   ```
2. Your default web browser should automatically open the app at `http://localhost:8501`.
3. On the Setup Screen, enter your **Torn API Key** and the **Target Faction ID** you wish to track.
4. Click **Start Tracking**.
5. The dashboard will load the faction snapshot. You can leave this page open, and it will continuously refresh the timers and player statuses in the background!
6. If you need to track a different faction or change your API key, simply click the **Change Settings** button in the top right corner.

## Disclaimer

This is a third-party application developed for the Torn community. It is not affiliated with, endorsed, or sponsored by Torn Ltd. Please ensure you comply with Torn's API usage rules and rate limits (the app naturally respects the 100 requests/minute limit by polling every 5 seconds).