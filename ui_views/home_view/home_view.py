import streamlit as st
import os
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

from src.logic.match_processor import process_fixtures, is_match_locked, get_user_predictions
from .components import render_match_card


def show_home(supabase, user_id:str):
    # 1. Data Fetch
    json_path = os.path.join(project_root, "..", "mock", "mock_matches.json")
    user_predictions = get_user_predictions(supabase=supabase, user_id=user_id)
    with open(json_path, 'r') as f:
        data = json.load(f)
        matches = data.get("matches", [])
    # 2. Use the "Brain" from src/
    grouped, current_md = process_fixtures(matches)
    
    # 3. Just Render
    for md, matches in grouped.items():
        with st.expander(f"Matchday {md}", expanded=(md == current_md)):
            for m in matches:
                # Use shared logic to check locking
                fixture_id = m["id"]
                user_pick = user_predictions.get(fixture_id, None)
                locked = is_match_locked(m["utcDate"])

                render_match_card(
                    supabase=supabase,
                    match=m,
                    locked=locked,
                    user_pick=user_pick,
                    fixture_id=fixture_id,
                    user_id=user_id,
                )

