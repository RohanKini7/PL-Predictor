import os
from dotenv import load_dotenv
from supabase import create_client

# 1. Load the keys from your .env file
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

def check_supabase():
    try:
        # 2. Initialize the client
        supabase = create_client(url, key)
        
        # 3. Try a simple query
        response = supabase.table("predictions").select("*").limit(1).execute()
        response = supabase.table("profiles").select("*").limit(1).execute()

        print("Connection established")
        print(f"Data found: {response.data}")
    
    except Exception as e:
        print("Connection failed")
        print(f"Error: {e}")

if __name__ == "__main__":
    check_supabase()