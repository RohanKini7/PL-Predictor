import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def sign_up_user(email, password, username):
    """Signs up a new user with a custom username in metadata."""
    return supabase.auth.sign_up({
        "email": email, 
        "password": password,
        "options": {
            "data": {
                "username": username
            }
        }
    })

def is_username_taken(username):
    """Checks if a username already exists in the profiles table."""
    res = supabase.table("profiles").select("username").eq("username", username).execute()
    return len(res.data) > 0

def login_user(email, password):
    """Authenticates the user and returns a session."""
    return supabase.auth.sign_in_with_password({"email": email, "password": password})

def logout_user():
    """Clears the session."""
    return supabase.auth.sign_out()

def get_current_user():
    """Retrieves the currently logged-in user details."""
    return supabase.auth.get_user()