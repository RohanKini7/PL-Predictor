import streamlit as st
from src.logic.match_processor import is_match_locked

def render_match_card(match, user_pick, on_save_func):
    """
    Renders a single match row with team names, scores, and prediction logic.
    """
    # 1. Logic Check (using your logic module)
    locked = is_match_locked(match['kickoff_time'])
    status = match['status']
    
    # 2. Score Formatting
    score_display = "vs"
    if status in ['FINISHED', 'IN_PLAY', 'PAUSED']:
        score_display = f"{match.get('home_score', 0)} - {match.get('away_score', 0)}"

    # 3. UI Container
    with st.container(border=True):
        cols = st.columns([2, 1, 2])
        
        with cols[0]:
            st.markdown(f"<div style='text-align: right;'><b>{match['home_team']}</b></div>", unsafe_all_html=True)
        
        with cols[1]:
            st.markdown(f"<div style='text-align: center; background-color: #f0f2f6; border-radius: 5px;'>{score_display}</div>", unsafe_all_html=True)
            
        with cols[2]:
            st.markdown(f"<b>{match['away_team']}</b>", unsafe_all_html=True)

        # Meta info
        st.caption(f"🕒 {match['kickoff_time']} | Status: {status}")

        # 4. Prediction Logic UI
        if status == 'FINISHED':
            st.info(f"Final Result: **{match.get('final_score', 'TBD')}**")
            if user_pick:
                color = "green" if user_pick == match.get('final_score') else "red"
                st.markdown(f"Your Pick: <span style='color:{color}; font-weight:bold;'>{user_pick}</span>", unsafe_all_html=True)
        
        elif locked:
            st.warning(f"🔒 Locked. Your pick: **{user_pick or 'None'}**")
        
        else:
            # Interactive prediction section
            options = ["HOME_WIN", "DRAW", "AWAY_WIN"]
            default_idx = options.index(user_pick) if user_pick in options else None
            
            # Using a radio for the pick
            pick = st.radio(
                f"Prediction for {match['fixture_id']}",
                options,
                index=default_idx,
                horizontal=True,
                key=f"radio_{match['fixture_id']}",
                label_visibility="collapsed"
            )
            
            # Button to trigger the save function passed from orchestrator
            if st.button("Save Prediction", key=f"btn_{match['fixture_id']}", use_container_width=True):
                on_save_func(match['fixture_id'], pick)

def render_matchday_header(matchday, is_current):
    """Simple helper for the header inside the expander."""
    text = f"📅 Matchday {matchday}"
    if is_current:
        text += " (Current Active Matchday)"
    st.markdown(f"### {text}")