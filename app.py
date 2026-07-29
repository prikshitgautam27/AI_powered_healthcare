"""
app.py — MediQuery Login · Fixed: visible nav links + sidebar always open after login
"""
import streamlit as st
import hashlib, json, os
from pathlib import Path

st.set_page_config(
    page_title="MediQuery — AI Medical Assistant",
    page_icon="M",
    layout="wide",
    initial_sidebar_state="expanded",
)

try:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
except Exception:
    pass

USERS_FILE = Path("users.json")

def load_users():
    if USERS_FILE.exists():
        return json.loads(USERS_FILE.read_text())
    defaults = {
        "demo":  hashlib.sha256("demo123".encode()).hexdigest(),
        "admin": hashlib.sha256("admin123".encode()).hexdigest(),
    }
    USERS_FILE.write_text(json.dumps(defaults))
    return defaults

def save_users(u): USERS_FILE.write_text(json.dumps(u))
def hash_pw(pw):   return hashlib.sha256(pw.encode()).hexdigest()

for k,v in [("logged_in",False),("username",""),("auth_tab","login"),("auth_error",""),("auth_success","")]:
    if k not in st.session_state: st.session_state[k] = v

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: #F8F6F2 !important;
    font-family: 'Inter', sans-serif;
    color: #1A1A2E;
}
#MainMenu, footer, header, [data-testid="stToolbar"] { display: none !important; }

/* ── Sidebar always styled ── */
[data-testid="stSidebar"] { background: #FFFFFF !important; border-right: 1px solid #EDE8E0 !important; }
[data-testid="stSidebar"] * { color: #1A1A2E !important; }
[data-testid="stSidebar"] label { color: #8A9BB0 !important; font-size: 0.68rem !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; font-weight: 500 !important; }
[data-testid="stSidebar"] hr { border-color: #EDE8E0 !important; }
/* Fix page_link text color — this is the key fix */
[data-testid="stSidebar"] [data-testid="stPageLink"] a,
[data-testid="stSidebar"] [data-testid="stPageLink"] a span,
[data-testid="stSidebar"] [data-testid="stPageLink"] p {
    color: #1B4332 !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    text-decoration: none !important;
}
[data-testid="stSidebar"] [data-testid="stPageLink"]:hover a {
    color: #2D6A4F !important;
}
[data-testid="stSidebar"] .stButton button {
    background: #1B4332 !important;
    border: none !important;
    color: #FFFFFF !important;
    border-radius: 8px !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    width: 100% !important;
    margin-bottom: 0.3rem !important;
    box-shadow: 0 2px 6px rgba(27,67,50,0.2) !important;
}

/* ── Main content ── */
[data-testid="block-container"] { padding: 2rem 2.5rem !important; max-width: 700px; margin: 0 auto; }

.brand { text-align: center; margin-bottom: 2.5rem; padding-top: 1rem; }
.bmark { width: 64px; height: 64px; border: 2px solid #2D6A4F; border-radius: 16px; display: inline-flex; align-items: center; justify-content: center; font-family: 'Playfair Display', serif; font-size: 1.8rem; color: #1B4332; margin-bottom: 1rem; background: #F0FDF4; }
.bname { font-family: 'Playfair Display', serif; font-size: 2rem; color: #1A1A2E; font-weight: 400; }
.bsub { font-size: 0.65rem; letter-spacing: 0.22em; text-transform: uppercase; color: #A0ADB8; margin-top: 0.3rem; }

.card { background: #FFFFFF; border: 1px solid #EDE8E0; border-radius: 16px; padding: 2rem; box-shadow: 0 2px 12px rgba(0,0,0,0.04); }

.tab-row { display: flex; border-bottom: 2px solid #F0EDE8; margin-bottom: 1.8rem; }
.tab-a { font-size: 0.72rem; letter-spacing: 0.1em; text-transform: uppercase; color: #1B4332; padding: 0 1.2rem 0.7rem; border-bottom: 2px solid #1B4332; margin-bottom: -2px; font-weight: 600; }
.tab-i { font-size: 0.72rem; letter-spacing: 0.1em; text-transform: uppercase; color: #C0C8D8; padding: 0 1.2rem 0.7rem; border-bottom: 2px solid transparent; margin-bottom: -2px; }

.stTextInput input { background: #F8F6F2 !important; border: 1.5px solid #E2DDD6 !important; border-radius: 8px !important; color: #1A1A2E !important; font-family: 'Inter', sans-serif !important; font-size: 0.9rem !important; }
.stTextInput input:focus { border-color: #2D6A4F !important; box-shadow: 0 0 0 3px rgba(45,106,79,0.1) !important; background: #FFFFFF !important; }
.stTextInput label { color: #6A7A8A !important; font-size: 0.7rem !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; font-weight: 500 !important; }

.stButton > button { background: #1B4332 !important; border: none !important; color: #FFFFFF !important; border-radius: 8px !important; font-family: 'Inter', sans-serif !important; font-size: 0.8rem !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; font-weight: 500 !important; width: 100% !important; padding: 0.75rem !important; transition: all 0.2s !important; box-shadow: 0 2px 8px rgba(27,67,50,0.25) !important; }
.stButton > button:hover { background: #2D6A4F !important; transform: translateY(-1px) !important; }

.err { background: #FEF2F2; border: 1px solid #FECACA; border-radius: 8px; padding: 0.75rem 1rem; font-size: 0.82rem; color: #DC2626; margin-bottom: 1rem; }
.suc { background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 8px; padding: 0.75rem 1rem; font-size: 0.82rem; color: #16A34A; margin-bottom: 1rem; }
.hint { font-size: 0.72rem; color: #A0ADB8; margin-top: 1.2rem; text-align: center; padding: 0.75rem; background: #F8F6F2; border-radius: 8px; line-height: 1.7; }
.hint strong { color: #6A7A8A; }

/* Nav links after login — dark text on light bg */
.nav-card { background: #F8F6F2; border: 1px solid #E2DDD6; border-radius: 12px; padding: 1.2rem 1.5rem; margin-top: 1rem; }
.nav-card-title { font-size: 0.7rem; letter-spacing: 0.14em; text-transform: uppercase; color: #A0ADB8; margin-bottom: 1rem; font-weight: 500; }

/* Fix page_link in main area too */
[data-testid="stPageLink"] a,
[data-testid="stPageLink"] a span,
[data-testid="stPageLink"] p {
    color: #1B4332 !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    text-decoration: none !important;
}
[data-testid="stPageLink"]:hover a { color: #2D6A4F !important; }

.stats-row { display: flex; justify-content: center; gap: 3rem; margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid #EDE8E0; }
.sr-item { text-align: center; }
.sr-val { font-family: 'Playfair Display', serif; font-size: 1.4rem; color: #2D6A4F; }
.sr-lbl { font-size: 0.6rem; letter-spacing: 0.12em; text-transform: uppercase; color: #B0BDC8; margin-top: 0.2rem; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar (always visible) ──────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1.2rem 0 0.8rem;">
        <div style="font-family:'Playfair Display',serif;font-size:1.4rem;color:#1A1A2E;font-weight:400;">MediQuery</div>
        <div style="font-size:0.62rem;color:#A0ADB8;letter-spacing:0.14em;text-transform:uppercase;margin-top:0.2rem;">AI Health Assistant</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    if st.session_state.logged_in:
        st.markdown(f"<div style='font-size:0.78rem;color:#2D6A4F;font-weight:600;margin-bottom:1rem;'>Signed in as {st.session_state.username}</div>", unsafe_allow_html=True)
        st.page_link("pages/1_Home.py",    label="Home")
        st.page_link("pages/2_Query.py",   label="Query")
        st.page_link("pages/3_Metrics.py", label="Metrics")
        st.markdown("---")
        if st.button("Sign Out"):
            st.session_state.logged_in=False; st.session_state.username=""; st.rerun()
    else:
        st.markdown("<div style='font-size:0.8rem;color:#A0ADB8;line-height:1.6;'>Sign in to access the Medical Query Engine, Performance Metrics, and your personalised health dashboard.</div>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("""
        <div style="font-size:0.7rem;color:#B0BDC8;line-height:1.8;">
            <div style="margin-bottom:0.4rem;"> &nbsp;Semantic search over 7,470 passages</div>
            <div style="margin-bottom:0.4rem;"> &nbsp;Sub-2s responses via Groq</div>
            <div style="margin-bottom:0.4rem;">&nbsp;Gale Encyclopedia of Medicine</div>
            <div> &nbsp;Secure, session-based login</div>
        </div>
        """, unsafe_allow_html=True)

# ── Main content ──────────────────────────────────────────
st.markdown("""
<div class="brand">
    <div class="bmark">M</div>
    <div class="bname">MediQuery</div>
    <div class="bsub">AI Medical Knowledge Assistant</div>
</div>
""", unsafe_allow_html=True)

# If logged in show nav
if st.session_state.logged_in:
    st.markdown(f'<div class="suc">Signed in as <strong>{st.session_state.username}</strong>. Navigate below.</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-card"><div class="nav-card-title">Where would you like to go?</div>', unsafe_allow_html=True)
    st.page_link("pages/1_Home.py",    label="Home — Dashboard" )
    st.page_link("pages/2_Query.py",   label="Query — Ask a question" )
    st.page_link("pages/3_Metrics.py", label="Metrics — Performance" )
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# Auth card
st.markdown('<div class="card">', unsafe_allow_html=True)

c1,c2 = st.columns(2)
with c1:
    if st.button("Sign In",  key="t1"): st.session_state.auth_tab="login";    st.session_state.auth_error=""; st.rerun()
with c2:
    if st.button("Register", key="t2"): st.session_state.auth_tab="register"; st.session_state.auth_error=""; st.rerun()

tab = st.session_state.auth_tab
la = "tab-a" if tab=="login" else "tab-i"
ra = "tab-a" if tab=="register" else "tab-i"
st.markdown(f'<div class="tab-row"><span class="{la}">Sign In</span><span class="{ra}">Register</span></div>', unsafe_allow_html=True)

if st.session_state.auth_error:
    st.markdown(f'<div class="err">{st.session_state.auth_error}</div>', unsafe_allow_html=True)
if st.session_state.auth_success:
    st.markdown(f'<div class="suc">{st.session_state.auth_success}</div>', unsafe_allow_html=True)

users = load_users()

if tab == "login":
    username = st.text_input("Username", key="li_u", placeholder="your username")
    password = st.text_input("Password", type="password", key="li_p", placeholder="••••••••")
    if st.button("Sign In  →", key="do_login"):
        if not username or not password:
            st.session_state.auth_error = "Please fill in both fields."
        elif username not in users or users[username] != hash_pw(password):
            st.session_state.auth_error = "Invalid username or password."
        else:
            st.session_state.logged_in=True; st.session_state.username=username
            st.session_state.auth_error=""; st.session_state.auth_success=""
        st.rerun()
    st.markdown('<div class="hint">Demo access &nbsp;·&nbsp; <strong>Username:</strong> demo &nbsp;&nbsp;<strong>Password:</strong> demo123</div>', unsafe_allow_html=True)
else:
    nu  = st.text_input("Username", key="ru",  placeholder="choose a username")
    np  = st.text_input("Password", type="password", key="rp",  placeholder="min 6 characters")
    np2 = st.text_input("Confirm password", type="password", key="rp2", placeholder="repeat password")
    if st.button("Create Account  →", key="do_reg"):
        if not nu or not np:  st.session_state.auth_error="All fields required."
        elif len(np)<6:       st.session_state.auth_error="Password must be 6+ characters."
        elif np!=np2:         st.session_state.auth_error="Passwords don't match."
        elif nu in users:     st.session_state.auth_error="Username already taken."
        else:
            users[nu]=hash_pw(np); save_users(users)
            st.session_state.auth_success=f"Account created! Sign in as {nu}."
            st.session_state.auth_tab="login"; st.session_state.auth_error=""
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="stats-row">
    <div class="sr-item"><div class="sr-val">759</div><div class="sr-lbl">Source pages</div></div>
    <div class="sr-item"><div class="sr-val">7,470</div><div class="sr-lbl">Passages</div></div>
    <div class="sr-item"><div class="sr-val">&lt;2s</div><div class="sr-lbl">Response time</div></div>
</div>
""", unsafe_allow_html=True)
