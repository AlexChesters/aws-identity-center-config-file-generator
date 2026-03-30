import os
import sys

def validate_environment():
    profile_name = os.getenv("AWS_PROFILE")
    region_name = os.getenv("AWS_REGION")
    identity_store_id = os.getenv("IDENTITY_STORE_ID")

    if not profile_name or not region_name or not identity_store_id:
        print(f"[ERROR] Missing required environment variables (AWS_PROFILE={profile_name}, AWS_REGION={region_name}, IDENTITY_STORE_ID={identity_store_id}).")
        sys.exit(1)
