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
    st.markdown("""
         <style>
             .block-container {
                 padding-top: 0rem !important;
                 padding-bottom: 0rem !important;

             }
         </style>
     """, unsafe_allow_html=True)
    with st.container():
        st.markdown("""
             <style>
                 .block-container {
                     padding-top: 1rem !important;
                     padding-bottom: 0rem !important;
                 }
             </style>
         """, unsafe_allow_html=True)

        # We use raw HTML instead of st.columns to prevent Streamlit's default mobile squashing
        st.markdown("""
             <div style="
                 display: flex;
                 flex-direction: column;
                 align-items: center;
                 justify-content: center;
                 width: 100%;
                 margin-bottom: 10px;
             ">
                 <h1 style="
                     margin: 0;
                     line-height: 1.1;
                     text-align: center;
                     /* clamp(MIN, PREFERRED, MAX) */
                     /* This makes it huge on desktop (5rem) but stays readable on phone (2.5rem) */
                     font-size: clamp(2.5rem, 12vw, 5rem);
                     color: white;
                     font-weight: 900;
                 ">
                     Banter Cave: PL Prediction Championship
                 </h1>
             </div>
         """, unsafe_allow_html=True)
    json_path = os.path.join(project_root, "..", "dataset", "pl_season_data.json")
    with open(json_path, 'r') as f:
        data = json.load(f)
        matches = data.get("matches", [])
    current_matchday = matches[0].get("season").get("currentMatchday")
    show_leaderboard(supabase=supabase, current_matchday=current_matchday)
