import streamlit as st

from src.utils import get_team_name, get_team_badge
from src.logic.match_processor import is_match_locked, get_score_display, handle_prediction_save



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

    # 2. Score Formatting
    score_display = "vs"
    if status in ['FINISHED', 'IN_PLAY', 'PAUSED']:
        score_display = get_score_display(match=match)

    st.divider()  # A clean line to separate the title from the fixtures
        # 2. UI Container (The Match Card)
    with st.container(border=True):
        cols = st.columns([2, 1, 2])

        with cols[0]:
            st.markdown(f"""
                        <div style="display: flex; align-items: center; justify-content: flex-end; height: 100%;">
                            <span style="font-weight: bold; margin-right: 10px;">{home_team}</span>
                            <img src="{home_badge}" width="35">
                        </div>
                    """, unsafe_allow_html=True)

        with cols[1]:
            st.markdown(f"""
                        <div style="text-align: center;">
                            <div  color: white; padding: 5px; border-radius: 5px; font-weight: bold;">
                                {score_display}
                            </div>
                            <div style="font-size: 0.7em; margin-top: 2px; color: #666;">{status if status != 'FINISHED' else 'FT'}</div>
                        </div>
                    """, unsafe_allow_html=True)

        with cols[2]:
            st.markdown(f"""
                        <div style="display: flex; align-items: center; justify-content: flex-start; height: 100%;">
                            <img src="{away_badge}" width="35" style="margin-right: 10px;">
                            <span style="font-weight: bold;">{away_team}</span>
                        </div>
                    """, unsafe_allow_html=True)

        st.markdown(f"""
            <div style="text-align: center; padding: 10px; opacity: 0.8; font-size: 0.9em;">
                My pick: <b>{user_pick}</b>
            </div>
        """, unsafe_allow_html=True)

