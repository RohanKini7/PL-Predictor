import streamlit as st

from src.utils import get_team_name, get_team_badge
from src.match_processor import (
    get_score_display, get_user_pick_for_fixture, get_prediction_color
)



def render_finished_match_card(supabase, match: dict, locked: bool, user_pick: str, user_id: str, fixture_id: str):
    """
    Renders a single match row with team names, scores, and prediction logic.
    """
    # 1. Logic Check (using your logic module)
    status = match['status']
    home_team = get_team_name(match=match, team="HOME")
    away_team = get_team_name(match=match, team="AWAY")

    home_badge = get_team_badge(match=match, team="HOME")
    away_badge = get_team_badge(match=match, team="AWAY")

    user_team = get_user_pick_for_fixture(user_pick=user_pick, home_team=home_team, away_team=away_team)

    # 2. Score Formatting
    score_display = "vs"
    if status in ['FINISHED', 'IN_PLAY', 'PAUSED']:
        score_display = get_score_display(match=match)

    st.divider()  # A clean line to separate the title from the fixtures
        # 2. UI Container (The Match Card)
    with st.container(border=True):
        # Main Flexbox Container for the Match Details
        st.markdown(f"""
            <div style="
                display: flex; 
                align-items: center; 
                justify-content: space-between; 
                width: 100%; 
                padding: 5px 0;
                gap: 5px;
            ">
                <div style="flex: 1; display: flex; align-items: center; justify-content: flex-end; gap: 8px;">
                    <span style="font-weight: bold; font-size: clamp(0.85rem, 3vw, 1.1rem); text-align: right;">
                        {home_team}
                    </span>
                    <img src="{home_badge}" width="35" style="flex-shrink: 0;">
                </div>
                <div style="flex: 0.7; text-align: center; min-width: 70px;">
                    <div style="font-weight: bold; font-size: 1.2rem; color: white;">
                        {score_display}
                    </div>
                    <div style="font-size: 0.7rem; color: #aaa; margin-top: -2px;">
                        {status if status != 'FINISHED' else 'FT'}
                    </div>
                </div>
                <div style="flex: 1; display: flex; align-items: center; justify-content: flex-start; gap: 8px;">
                    <img src="{away_badge}" width="35" style="flex-shrink: 0;">
                    <span style="font-weight: bold; font-size: clamp(0.85rem, 3vw, 1.1rem); text-align: left;">
                        {away_team}
                    </span>
                </div>
            </div>
            <div style="
                text-align: center; 
                padding-top: 10px; 
                margin-top: 5px;
                border-top: 1px solid rgba(255,255,255,0.1);
                font-size: 0.9rem; 
                color: {get_prediction_color};
            ">
                My pick: <b>{user_team}</b>
            </div>
        """, unsafe_allow_html=True)
