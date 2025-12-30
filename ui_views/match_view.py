import streamlit as st
import os
from supabase import create_client
from src.rules import is_prediction_locked

# Initialize Supabase client
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def show_matches():
    st.title("⚽ Premier League Fixtures")
    st.markdown("---")

    # 1. Fetch upcoming matches (NS = Not Started)
    # We order by kickoff_time so the next game is always at the top
    try:
        response = supabase.table("mock_fixtures").select("*").eq("status", "NS").order("kickoff_time").execute()
        matches = response.data
    except Exception as e:
        st.error(f"Error fetching fixtures: {e}")
        return

    if not matches:
        st.info("No upcoming matches found. Try running your sync script!")
        return

    # 2. Iterate through matches and create UI cards
    for match in matches:
        with st.container(border=True):
            col_info, col_action = st.columns([3, 1])
            
            with col_info:
                st.subheader(f"{match['home_team']} vs {match['away_team']}")
                st.caption(f"📅 Kickoff: {match['kickoff_time']}")
            
            # 3. Check the 24-hour lock rule
            locked = is_prediction_locked(match['kickoff_time'])
            
            with col_action:
                if locked:
                    st.error("🔒 Locked")
                else:
                    # Dropdown for user prediction
                    user_choice = st.selectbox(
                        "Pick Winner",
                        ["HOME_WIN", "DRAW", "AWAY_WIN"],
                        key=f"select_{match['fixture_id']}"
                    )
                    
                    if st.button("Save Prediction", key=f"btn_{match['fixture_id']}"):
                        save_user_prediction(match['fixture_id'], user_choice)

def save_user_prediction(fixture_id, choice):
    """Saves or updates the user's prediction in Supabase."""
    user_id = st.session_state.user.id  # Get current user from Auth session
    
    payload = {
        "user_id": user_id,
        "fixture_id": fixture_id,
        "prediction": choice
    }
    
    try:
        # 'upsert' automatically handles 'update' if user has already voted
        supabase.table("predictions").upsert(payload).execute()
        st.toast(f"✅ Prediction saved for Match {fixture_id}!", icon='🔥')
    except Exception as e:
        st.error(f"Failed to save prediction: {e}")