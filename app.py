import streamlit as st
from firebase_config import firebase_ready, get_firestore, sign_in, sign_up, sign_out
from chatbot import find_answer
from faq_data import DEMO_FAQS

st.set_page_config(page_title="UniAssist | Smart University Helpdesk", page_icon="🎓", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] {font-family: Inter, sans-serif;}
.stApp {background: linear-gradient(135deg,#f7faff 0%,#eef4ff 55%,#f9fbff 100%);}
.block-container {padding-top: 1.8rem; max-width: 1200px;}
.hero {padding: 28px 30px; border-radius: 24px; color: white;
background: linear-gradient(115deg,#102a56,#1756a9 65%,#3d82e8);
box-shadow: 0 16px 40px rgba(20,70,140,.18); margin-bottom: 22px;}
.hero h1 {font-size: 2.25rem; margin: 0 0 8px 0; font-weight: 800;}
.hero p {font-size: 1rem; opacity: .9; margin: 0;}
.pill {display:inline-block; padding:5px 10px; border-radius:999px; background:#d9fbe8;
color:#12633a; font-weight:700; font-size:.78rem; margin-bottom:10px;}
.metric-card {background:white;border:1px solid #e2eaf6;border-radius:18px;padding:18px;
box-shadow:0 8px 22px rgba(30,65,120,.05);}
.answer-card {background:#fff;border:1px solid #dfe8f5;border-left:5px solid #2671d9;
padding:18px;border-radius:14px;margin:10px 0 18px;}
.small-muted {color:#64748b;font-size:.88rem;}
div[data-testid="stChatMessage"] {border-radius:16px;}
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "user" not in st.session_state:
    st.session_state.user = None
if "id_token" not in st.session_state:
    st.session_state.id_token = None

st.markdown("""
<div class="hero">
  <div class="pill">CLOUD-READY • STUDENT SUPPORT</div>
  <h1>🎓 UniAssist</h1>
  <p>Your smart university helpdesk for admissions, academics, examinations and student services.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## UniAssist")
    st.caption("Smart University FAQ Assistant")
    if st.session_state.user:
        st.success(f"Signed in: {st.session_state.user}")
        if st.button("Sign out", use_container_width=True):
            sign_out()
            st.session_state.user = None
            st.session_state.id_token = None
            st.session_state.messages = []
            st.rerun()
    else:
        tab_login, tab_signup = st.tabs(["Login", "Register"])
        with tab_login:
            login_email = st.text_input("Email", key="login_email")
            login_password = st.text_input("Password", type="password", key="login_password")
            if st.button("Login", type="primary", use_container_width=True):
                ok, result = sign_in(login_email, login_password)
                if ok:
                    st.session_state.user = result.get("email", login_email)
                    st.session_state.id_token = result.get("idToken")
                    st.rerun()
                else:
                    st.error(result)
        with tab_signup:
            new_email = st.text_input("Email address", key="new_email")
            new_password = st.text_input("Password (6+ characters)", type="password", key="new_password")
            if st.button("Create account", use_container_width=True):
                ok, result = sign_up(new_email, new_password)
                if ok:
                    st.success("Account created. You can now sign in.")
                else:
                    st.error(result)

    st.divider()
    st.markdown("### Explore topics")
    for topic in ["Admissions", "Courses", "Fees & Scholarships", "Examinations", "Library", "Student Support"]:
        st.write("• " + topic)
    st.caption("Use official university sources to verify dates, fees and policy details.")

ready, status = firebase_ready()
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="metric-card"><div class="small-muted">Knowledge base</div><h2>FAQ Search</h2><div class="small-muted">Find relevant answers</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="metric-card"><div class="small-muted">Account</div><h2>Cloud Login</h2><div class="small-muted">Firebase Authentication</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="metric-card"><div class="small-muted">Storage</div><h2>Cloud FAQ</h2><div class="small-muted">Firestore when configured</div></div>', unsafe_allow_html=True)

st.write("")
if not ready:
    st.info("Preview mode is active. Add Firebase credentials in Streamlit Cloud Secrets to enable cloud login and Firestore. Demo FAQ answers are available now.")
else:
    st.success("Firebase configuration detected.")

st.markdown("## Ask UniAssist")
st.caption("Try asking about admissions, scholarships, exam timetable, library hours, courses, or student ID cards.")

suggestions = ["How can I apply for admission?", "What scholarships are available?", "How do I check exam results?"]
cols = st.columns(len(suggestions))
for i, prompt in enumerate(suggestions):
    with cols[i]:
        if st.button(prompt, key=f"suggest_{i}", use_container_width=True):
            st.session_state.messages.append({"role":"user", "content":prompt})
            answer, source = find_answer(prompt, get_firestore() if ready else None, DEMO_FAQS)
            st.session_state.messages.append({"role":"assistant", "content":answer, "source":source})
            st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("source"):
            st.caption(f"Source: {msg['source']}")

question = st.chat_input("Type your university question…")
if question:
    st.session_state.messages.append({"role":"user", "content":question})
    answer, source = find_answer(question, get_firestore() if ready else None, DEMO_FAQS)
    st.session_state.messages.append({"role":"assistant", "content":answer, "source":source})
    st.rerun()

st.divider()
st.caption("UniAssist academic project prototype • Replace sample FAQs with verified university information before submission.")
