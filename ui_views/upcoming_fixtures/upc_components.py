import streamlit as st
from src.match_processor import handle_prediction_save, get_user_pick_for_fixture
from src.utils import get_team_name, get_team_badge
from datetime import datetime

def render_match_card(supabase, match: dict, locked: bool, user_pick: str, user_id: str, fixture_id: str ):
    """
    Renders a single match row with team names, scores, and prediction logic.
    """
    # 1. Logic Check (using your logic module)
    status = match['status']
    home_team = get_team_name(match=match, team="HOME")
    away_team = get_team_name(match=match, team="AWAY")

    home_badge = get_team_badge(match=match, team="HOME")
    away_badge = get_team_badge(match=match, team="AWAY")

    kick_off_time = datetime.fromisoformat(match["utcDate"].replace('Z', '+00:00')).strftime("%d %b %H:%M")
    user_team = get_user_pick_for_fixture(user_pick=user_pick, home_team=home_team, away_team=away_team)

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
                                {kick_off_time}
                            </div>
                    """, unsafe_allow_html=True)

        with cols[2]:
            st.markdown(f"""
                        <div style="display: flex; align-items: center; justify-content: flex-start; height: 100%;">
                            <img src="{away_badge}" width="35" style="margin-right: 10px;">
                            <span style="font-weight: bold;">{away_team}</span>
                        </div>
                    """, unsafe_allow_html=True)

        # 3. Prediction UI Layer
        if status == 'FINISHED':
            # Using markdown to center the text and add a bit of styling
            st.markdown(f"""
                <div style="text-align: center; padding: 10px; opacity: 0.8; font-size: 0.9em;">
                    Match Finished. Your pick: <b>{user_team or 'No prediction'}</b>
                </div>
            """, unsafe_allow_html=True)
        elif locked:
            # Show locked symbol and previous prediction

            st.markdown(f"""
                <div style="text-align: center; padding: 10px; opacity: 0.8; font-size: 0.9em;">
                🔒 Locked. Your prediction: {user_team}</b>
            </div>
                """, unsafe_allow_html=True)


        else:
            # Game is OPEN - Show 3 buttons for Home, Draw, Away
            st.write("Make your prediction:")
            btn_cols = st.columns(3)

            # Options mapping
            options = {
                "HOME_TEAM": f" {home_team}",
                "DRAW": "🤝 Draw",
                "AWAY_TEAM": f" {away_team}"
            }

            for i, (choice_code, display_name) in enumerate(options.items()):
                with btn_cols[i]:
                    # Highlight the button if it matches the current saved user_pick
                    is_selected = (user_pick == choice_code)
                    button_type = "primary" if is_selected else "secondary"
                    if st.button(display_name, key=f"pred_{fixture_id}_{choice_code}",
                                 type=button_type, use_container_width=True):
                        handle_prediction_save(
                            supabase=supabase,user_id=user_id,fixture_id=fixture_id, user_choice=choice_code
                        )
                        st.rerun()

def render_matchday_header(matchday, is_current):
    """Simple helper for the header inside the expander."""
    text = f"📅 Matchday {matchday}"
    if is_current:
        text += " (Current Active Matchday)"
    st.markdown(f"### {text}")