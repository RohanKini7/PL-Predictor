import streamlit as st
import extra_streamlit_components as stx
from ui_views.home_view import home_view
from ui_views.login_view import login_view
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    # 1. Page Config MUST be the very first Streamlit command
    st.set_page_config(page_title="PL Predictor 2025", page_icon="⚽", layout="wide")

    # 2. Initialize Supabase
    supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

    # 3. Initialize Cookie Manager (Optional for now, but good to have)
    cookie_manager = stx.CookieManager()

    # 4. Auth Check
    if 'user' not in st.session_state:
        login_view.show_login()
        st.stop() # Stops execution so the code below doesn't run for guests

    # --- EVERYTHING BELOW RUNS ONLY FOR LOGGED-IN USERS ---
    
    user = st.session_state.user

    # 5. Normalize User ID in Session State
    if 'user_id' not in st.session_state:
        # Check if user is a dict or object
        st.session_state.user_id = user['id'] if isinstance(user, dict) else user.id

    # 6. Sidebar Navigation
    st.sidebar.title("🏆 PL Predictor")
    
    # Safely get username from metadata
    username = user.user_metadata.get('username', 'User') if not isinstance(user, dict) else user.get('user_metadata', {}).get('username', 'User')
    st.sidebar.info(f"Welcome, {username}!")
    
    nav = st.sidebar.radio("Go To", ["Home (Fixtures)", "My Predictions", "Leaderboard"])

    if st.sidebar.button("Logout"):
        # Clear specific keys or just clear everything
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    # 7. Routing to Views
    if nav == "Home (Fixtures)":
        home_view.show_home(supabase=supabase)
    elif nav == "My Predictions":
        st.title("📂 My Predictions")
        st.info("Feature coming next!")
    elif nav == "Leaderboard":
        st.title("📊 Leaderboard")
        st.info("Feature coming soon!")

if __name__ == "__main__":
    main()