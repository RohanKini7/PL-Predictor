import streamlit as st
from ui_views import login_view, match_view

def main():
    # 1. Set Page Configuration (Browser Tab Title/Icon)
    st.set_page_config(page_title="PL Predictor", page_icon="⚽")

    # 2. Check Auth Status in Session State
    if 'user' not in st.session_state:
        # If not logged in, only show the Login UI
        login_view.show_login()
    else:
        # 3. Sidebar Navigation for Logged-in Users
        st.sidebar.title("🏆 PL Predictor")
        st.sidebar.write(f"Logged in: **{st.session_state.user.email}**")
        
        page = st.sidebar.radio("Navigation", ["Matches", "Leaderboard", "Profile"])
        
        # Logout logic
        if st.sidebar.button("Logout"):
            from src.auth_service import logout_user
            logout_user()
            del st.session_state.user
            st.rerun()

        # 4. Routing to the appropriate View
        if page == "Matches":
            match_view.show_matches()
        elif page == "Leaderboard":
            st.title("📊 Leaderboard")
            st.info("Leaderboard coming soon! (We'll build this next)")
        elif page == "Profile":
            st.title("👤 Your Profile")
            st.write(f"Email: {st.session_state.user.email}")
            st.write(f"User ID: `{st.session_state.user.id}`")

if __name__ == "__main__":
    main()