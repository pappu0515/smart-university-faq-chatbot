import streamlit as st
import requests
from google.cloud import firestore
from google.oauth2 import service_account

def _secrets():
    try:
        return st.secrets
    except Exception:
        return {}

def firebase_ready():
    s = _secrets()
    firebase = s.get("firebase", {})
    cloud = s.get("gcp_service_account", {})
    return bool(firebase.get("api_key") and firebase.get("project_id") and cloud), "configured"

def sign_in(email, password):
    s = _secrets().get("firebase", {})
    api_key = s.get("api_key", "")
    if not api_key:
        return False, "Firebase API key is not configured in Streamlit Secrets."
    if not email or not password:
        return False, "Enter your email and password."
    try:
        response = requests.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}",
            json={"email": email, "password": password, "returnSecureToken": True}, timeout=15)
        data = response.json()
        if response.ok:
            return True, data
        return False, data.get("error", {}).get("message", "Login failed.")
    except Exception as e:
        return False, f"Could not contact Firebase: {e}"

def sign_up(email, password):
    s = _secrets().get("firebase", {})
    api_key = s.get("api_key", "")
    if not api_key:
        return False, "Firebase API key is not configured in Streamlit Secrets."
    if not email or len(password or "") < 6:
        return False, "Enter an email and a password with at least 6 characters."
    try:
        response = requests.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}",
            json={"email": email, "password": password, "returnSecureToken": True}, timeout=15)
        data = response.json()
        if response.ok:
            return True, data
        return False, data.get("error", {}).get("message", "Registration failed.")
    except Exception as e:
        return False, f"Could not contact Firebase: {e}"

def sign_out():
    return

def get_firestore():
    s = _secrets()
    service_account_info = dict(s.get("gcp_service_account", {}))
    if not service_account_info:
        return None
    try:
        credentials = service_account.Credentials.from_service_account_info(service_account_info)
        return firestore.Client(project=service_account_info.get("project_id"), credentials=credentials)
    except Exception:
        return None
