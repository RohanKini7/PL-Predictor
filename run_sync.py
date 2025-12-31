import streamlit as st
import json
import os
from datetime import datetime, timedelta, timezone
from supabase import create_client

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def show_home():
    # Centered Header
    _, center_col, _ = st.columns([1, 4, 1])
    with center_col:
        st.title("⚽ Match Center")
        st.caption("Grouped by Matchday • 1-hour lock rule active")

    # 1. Load Data
    mock_path = os.path.join("mock", "mock_matches.json")
    if not os.path.exists(mock_path):
        st.error("Data file not found. Please run the sync script first.")
        return

    with open(mock_path, 'r') as f:
        data = json.load(f)
        matches = data.get("matches", [])

    if not matches:
        st.write("No matches found.")
        return

    # 2. Identify Current Matchday & Group Matches
    # Grab currentMatchday from the first match's season info
    current_matchday = matches[0]['season']['currentMatchday']
    
    grouped_matches = {}
    for m in matches:
        md = m['matchday']
        if md not in grouped_matches:
            grouped_matches[md] = []
        grouped_matches[md].append(m)

    # Sort matchdays (1 to 38)
    sorted_matchdays = sorted(grouped_matches.keys())

    # 3. Iterate Through Matchdays
    now = datetime.now(timezone.utc)

    for md in sorted_matchdays:
        matches_in_md = grouped_matches[md]
        
        # Determine if this dropdown should be open
        # Rule: Expand if it's the current matchday OR contains a live game
        has_live = any(m['status'] in ['IN_PLAY', 'PAUSED'] for m in matches_in_md)
        should_expand = (md == current_matchday) or has_live

        # Center the Expander
        _, center_col, _ = st.columns([1, 4, 1])
        
        with center_col:
            # Create the dropdown (Expander)
            expander_label = f"Matchday {md}"
            if md == current_matchday: expander_label += " (Current)"
            if has_live: expander_label += " • 🔴 LIVE"

            with st.expander(expander_label, expanded=should_expand):
                for m in matches_in_md:
                    display_match_card(m, now)

def display_match_card(m, now):
    """Renders a single match row with prediction buttons."""
    kickoff = datetime.fromisoformat(m['utcDate'].replace('Z', '+00:00'))
    # Lock rule: 1 hour before kickoff
    is_locked = (kickoff - now) < timedelta(hours=1)
    
    # Check if match is finished or live for score display
    home_score = m['score']['fullTime']['home']
    away_score = m['score']['fullTime']['away']
    score_text = f"{home_score} - {away_score}" if home_score is not None else "vs"
    
    if m['status'] in ['IN_PLAY', 'PAUSED']:
        score_text = f"🔴 {score_text}"

    # Visual Layout for the specific match
    with st.container(border=True):
        c1, c2, c3 = st.columns([2, 1, 2])
        with c1:
            st.write(f"**{m['homeTeam']['shortName']}**")
        with c2:
            st.write(f"**{score_text}**")
        with c3:
            st.write(f"**{m['awayTeam']['shortName']}**")
        
        st.caption(f"🕒 {kickoff.strftime('%d %b, %H:%M UTC')} | Status: {m['status']}")

        # Prediction Logic
        if m['status'] == 'FINISHED':
            st.info(f"Result: {m['score']['winner']}")
        elif is_locked:
            st.warning("🔒 Predictions Locked")
        else:
            # Three-way prediction buttons
            p1, p2, p3 = st.columns(3)
            if p1.button("Home", key=f"h_{m['id']}"):
                save_to_supabase(m['id'], "HOME_WIN")
            if p2.button("Draw", key=f"d_{m['id']}"):
                save_to_supabase(m['id'], "DRAW")
            if p3.button("Away", key=f"a_{m['id']}"):
                save_to_supabase(m['id'], "AWAY_WIN")

def save_to_supabase(fixture_id, prediction):
    user_id = st.session_state.user['id']
    try:
        data = {
            "user_id": user_id,
            "fixture_id": fixture_id,
            "predicted_score": prediction
        }
        supabase.table("predictions").upsert(data).execute()
        st.toast(f"Saved: {prediction}!", icon="✅")
    except Exception as e:
        st.error("Failed to save prediction.")