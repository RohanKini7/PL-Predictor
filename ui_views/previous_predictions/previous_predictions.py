import streamlit as st
import os
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

from src.logic.match_processor import (
    process_fixtures, is_match_locked, get_user_predictions, get_finished_matches)
from .prev_components import render_finished_match_card
from src.utils import PL_CREST


def show_home(supabase, user_id: str):
    # 1. Data Fetch
    user_predictions = get_user_predictions(supabase=supabase, user_id=user_id)

    json_path = os.path.join(project_root, "..", "mock", "mock_matches.json")
    with open(json_path, 'r') as f:
        data = json.load(f)
        matches = data.get("matches", [])

    finished_matches = get_finished_matches(matches)
    grouped, current_md = process_fixtures(finished_matches)

    st.markdown("""
        <style>
            .block-container {
                padding-top: 0rem !important;
                padding-bottom: 0rem !important;

            }
        </style>
    """, unsafe_allow_html=True)
    with st.container():
        st.markdown('<div style="display: flex; align-items: center; ">', unsafe_allow_html=True)
        # Use columns to align the PL Lion and your custom title side-by-side
        head_left, head_right = st.columns([1, 5], vertical_alignment='center')

        with head_left:
            # High-quality PL Crest
            st.image(PL_CREST, width=200)

        with head_right:
            st.markdown("""
                        <h1 style='margin-bottom: 0; line-height: 1.2; text-align: center; font-size: 2.75rem;'>
                            Banter Cave: PL Prediction Championship  
                        </h1>
                    """, unsafe_allow_html=True)

    # 3. Just Render
    for md, matches in grouped.items():
        with st.expander(f"Matchday {md}", expanded=(md == current_md)):
            for m in matches:
                # Use shared logic to check locking
                fixture_id = m["id"]
                user_pick = user_predictions.get(fixture_id, None)
                locked = is_match_locked(m["utcDate"])

                render_finished_match_card(
                    supabase=supabase,
                    match=m,
                    locked=locked,
                    user_pick=user_pick,
                    fixture_id=fixture_id,
                    user_id=user_id,
                )

