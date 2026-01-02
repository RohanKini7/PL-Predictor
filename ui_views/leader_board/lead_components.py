import pandas as pd
import streamlit as st

def get_leaderboard_data(supabase):
    # Fetch from the view we just created
    response = supabase.table("leaderboard").select("*").execute()
    return response.data

def show_leaderboard(supabase, current_matchday: int ):
    data = get_leaderboard_data(supabase)
    if data:
        df = pd.DataFrame(data)

        # Rename columns for the UI
        df["Matchday"] = current_matchday
        cols = ['Rank', 'Player', 'Matchday', 'Played', 'Points']
        df = df[cols]
        # Display the table
        st.markdown("""
            <style>
            /* Hides the index column in st.table */
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """, unsafe_allow_html=True)
        st.table(df)
    else:
        st.info("No finished matches yet. Check back soon!")