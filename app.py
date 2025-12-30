import streamlit as st
from supabase import create_client
import os
from dotenv import load_dotenv
from src.rules import is_prediction_locked

load_dotenv()

# Initialize Supabase
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

st.title("Banter Cave Premier League Predictor")

# 1. Sidebar for User Login (Simple version)
user_id = st.sidebar.text_input("Enter your User ID (UUID)", help="For now, use your ID from the Supabase profiles table.")

if not user_id:
    st.warning("Please enter your User ID in the sidebar to start.")
else:
    # 2. Fetch upcoming matches
    st.subheader("Upcoming Matches")
    matches = supabase.table("fixtures").select("*").eq("status", "NS").order("kickoff_time").execute()

    for match in matches.data:
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.write(f"**{match['home_team']} vs {match['away_team']}**")
            st.caption(f"Starts: {match['kickoff_time']}")
        
        # Check 24h lock rule
        locked = is_prediction_locked(match['kickoff_time'])
        
        with col2:
            if locked:
                st.error("🔒 Locked")
            else:
                choice = st.selectbox("Your Prediction", ["HOME_WIN", "AWAY_WIN", "DRAW"], key=match['fixture_id'])
        
        with col3:
            if not locked:
                if st.button("Submit", key=f"btn_{match['fixture_id']}"):
                    # Save prediction to Supabase
                    data = {
                        "user_id": user_id,
                        "fixture_id": match['fixture_id'],
                        "prediction": choice
                    }
                    supabase.table("predictions").upsert(data).execute()
                    st.success("Saved!")