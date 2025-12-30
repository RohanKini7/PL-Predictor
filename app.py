import streamlit as st
from ui_views import login_view

def main():
    # Check if user is already logged in
    if 'user' not in st.session_state:
        login_view.show_login()
    else:
        # Show the actual game dashboard
        st.sidebar.success(f"User: {st.session_state.user.email}")
        if st.sidebar.button("Logout"):
            from src.auth_service import logout_user
            logout_user()
            del st.session_state.user
            st.rerun()
            
        # Navigation
        page = st.sidebar.radio("Navigation", ["Matches", "Leaderboard"])
        st.write(f"Displaying {page} view...")
        # (We will build match_view and leader_view next)

if __name__ == "__main__":
    main()