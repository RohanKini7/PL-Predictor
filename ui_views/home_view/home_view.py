import streamlit as st
from src.logic.match_processor import process_fixtures, is_match_locked
from .components import render_match_card

def show_home(supabase):
    # 1. Data Fetch
    data = supabase.table("mock_fixtures").select("*").execute().data
    
    # 2. Use the "Brain" from src/
    grouped, current_md = process_fixtures(data)
    
    # 3. Just Render
    for md, matches in grouped.items():
        with st.expander(f"Matchday {md}", expanded=(md == current_md)):
            for m in matches:
                # Use shared logic to check locking
                locked = is_match_locked(m['kickoff_time'])
                render_match_card(m, locked)