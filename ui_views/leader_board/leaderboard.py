import streamlit as st
import os
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

from src.utils import PL_CREST
from .lead_components import show_leaderboard


def show_leaderboard_view(supabase):

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
    json_path = os.path.join(project_root, "..", "dataset", "pl_season_data.json")
    with open(json_path, 'r') as f:
        data = json.load(f)
        matches = data.get("matches", [])
    current_matchday = matches[0].get("season").get("currentMatchday")
    show_leaderboard(supabase=supabase, current_matchday=current_matchday)
