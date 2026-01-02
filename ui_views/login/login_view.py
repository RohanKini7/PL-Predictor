import streamlit as st
from src.auth_service import sign_up_user, login_user, is_username_taken

def show_login():
    st.title("🔐 PL Predictor")
    tab1, tab2 = st.tabs(["Login", "Create Account"])

    with tab1:
        email = st.text_input("Email", key="l_email")
        password = st.text_input("Password", type="password", key="l_pass")
        if st.button("Login", type="primary"):
            try:
                res = login_user(email, password)
                if res.user:
                    st.session_state.user = res.user
                    st.rerun()
            except Exception:
                st.error("Login failed. Check your email and password.")

    with tab2:
        new_email = st.text_input("Email", key="r_email")
        new_user = st.text_input("Choose a Username", key="r_user")
        new_pass = st.text_input("Password", type="password", key="r_pass")
        
        if st.button("Sign Up"):
            if not new_email or not new_user or not new_pass:
                st.error("Please fill in all fields.")
            elif is_username_taken(new_user):
                st.error(f"⚠️ The username '{new_user}' is already taken. Try another!")
            else:
                try:
                    # Supabase handles "Email already taken" automatically with an exception
                    sign_up_user(new_email, new_pass, new_user)
                    st.success("Success! Please check your email to confirm your account.")
                except Exception as e:
                    # This catches 'User already registered' errors
                    error_msg = str(e).lower()
                    if "already registered" in error_msg or "400" in error_msg:
                        st.error("⚠️ An account with this email already exists.")
                    else:
                        st.error(f"An error occurred: {e}")