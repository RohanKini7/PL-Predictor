
import streamlit as st
from dotenv import load_dotenv


import os


from ui_views.upcoming_fixtures import upcoming_fixtures
from ui_views.login import login_view
from ui_views.previous_predictions import previous_predictions
from ui_views.leader_board import leaderboard
from supabase import create_client

load_dotenv()

def main():
    # 1. Page Config MUST be the very first Streamlit command

    st.set_page_config(page_title="PL Predictor 2025", layout="wide")

    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]

    # 2. Initialize Supabase
    supabase = create_client(url, key)

    # 3. Auth Check
    if 'user' not in st.session_state:
        login_view.show_login()
        st.stop() # Stops execution so the code below doesn't run for guests
    # --- EVERYTHING BELOW RUNS ONLY FOR LOGGED-IN USERS ---
    user = st.session_state.user

    # 4. Normalize User ID in Session State
    if 'user_id' not in st.session_state:
        # Check if user is a dict or object
        st.session_state.user_id = user['id'] if isinstance(user, dict) else user.id
    # Safely get username from metadata
    username = (user.user_metadata.
                get('username', 'User')
                ) \
        if not isinstance(user, dict) \
        else user.get('user_metadata', {}).get('username', 'User')
    st.sidebar.markdown(f"""
        <div style="
            background-color: #4E0055; 
            color: white; 
            padding: 15px; 
            margin-bottom: 20px;
        ">
            <span style="font-size: 1.2em;"></span> 
            <b style="margin-left: 10px;">Welcome, {username}!</b>
        </div>
    """, unsafe_allow_html=True)
    
    nav = st.sidebar.radio("Go To", ["Upcoming Fixtures", "My Previous Predictions", "Leaderboard"])

    if st.sidebar.button("Logout"):
        # Clear specific keys or just clear everything
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    # 5. Routing to Views
    if nav == "Upcoming Fixtures":
        upcoming_fixtures.show_upcoming_fixtures(supabase=supabase, user_id=st.session_state.user_id)
    elif nav == "My Previous Predictions":
        previous_predictions.show_previous_fixtures(supabase=supabase, user_id=st.session_state.user_id)
    elif nav == "Leaderboard":
        leaderboard.show_leaderboard_view(supabase=supabase)

if __name__ == "__main__":
    main()