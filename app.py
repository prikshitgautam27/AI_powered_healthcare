"""
app.py — MediQuery Login · Light Mode
"""
import streamlit as st
import hashlib, json, os
from pathlib import Path

st.set_page_config(
    page_title="MediQuery — AI Medical Assistant",
    page_icon="M",
    layout="centered",
    initial_sidebar_state="collapsed",
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
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="block-container"] {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── Full page grid ── */
.login-wrap {
    min-height: 100vh;
    display: grid;
    grid-template-columns: 1fr 1fr;
    background: #F8F6F2;
}

/* ── Left panel ── */
.left {
    background: linear-gradient(160deg, #1B4332 0%, #2D6A4F 50%, #40916C 100%);
    display: flex; flex-direction: column;
    justify-content: center; padding: 4rem 3.5rem;
    position: relative; overflow: hidden;
}
.left::before {
    content: '';
    position: absolute; top: -100px; right: -100px;
    width: 350px; height: 350px;
    background: radial-gradient(circle, rgba(255,255,255,0.06) 0%, transparent 70%);
    border-radius: 50%;
}
.left::after {
    content: '';
    position: absolute; bottom: -60px; left: -60px;
    width: 250px; height: 250px;
    background: radial-gradient(circle, rgba(255,255,255,0.04) 0%, transparent 70%);
    border-radius: 50%;
}
.left-badge {
    display: inline-block;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 20px; padding: 0.3rem 0.9rem;
    font-size: 0.65rem; letter-spacing: 0.18em;
    text-transform: uppercase; color: #B7E4C7;
    margin-bottom: 1.8rem; width: fit-content;
}
.left-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem; line-height: 1.15;
    color: #FFFFFF; font-weight: 400;
    margin-bottom: 1.2rem;
}
.left-title em { font-style: italic; color: #95D5B2; }
.left-desc {
    font-size: 0.88rem; color: rgba(255,255,255,0.6);
    line-height: 1.75; margin-bottom: 2.5rem;
    font-weight: 300; max-width: 360px;
}
.feat-item {
    display: flex; align-items: flex-start;
    gap: 0.8rem; margin-bottom: 0.9rem;
}
.feat-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #95D5B2; margin-top: 6px; flex-shrink: 0;
}
.feat-text { font-size: 0.8rem; color: rgba(255,255,255,0.65); line-height: 1.5; }
.feat-text strong { color: #B7E4C7; font-weight: 500; }
.left-stats {
    display: flex; gap: 2rem;
    margin-top: 2.5rem; padding-top: 2rem;
    border-top: 1px solid rgba(255,255,255,0.12);
}
.ls-item strong {
    display: block; font-family: 'Playfair Display', serif;
    font-size: 1.5rem; color: #FFFFFF; font-weight: 400;
}
.ls-item span { font-size: 0.62rem; color: rgba(255,255,255,0.4); letter-spacing: 0.1em; text-transform: uppercase; }

/* ── Right panel ── */
.right {
    display: flex; flex-direction: column;
    justify-content: center; padding: 4rem 4rem 4rem 3.5rem;
    background: #FFFFFF;
}
.right-eyebrow {
    font-size: 0.62rem; letter-spacing: 0.18em;
    text-transform: uppercase; color: #2D6A4F;
    margin-bottom: 0.6rem; font-weight: 500;
}
.right-title {
    font-family: 'Playfair Display', serif;
    font-size: 2rem; color: #1A1A2E; font-weight: 400;
    margin-bottom: 0.4rem;
}
.right-sub { font-size: 0.82rem; color: #8A9BB0; margin-bottom: 2rem; }

/* Tab row */
.tab-row { display: flex; border-bottom: 2px solid #F0EDE8; margin-bottom: 1.8rem; }
.tab-a { font-size: 0.72rem; letter-spacing: 0.1em; text-transform: uppercase; color: #2D6A4F; padding: 0 1.2rem 0.7rem; border-bottom: 2px solid #2D6A4F; margin-bottom: -2px; font-weight: 600; }
.tab-i { font-size: 0.72rem; letter-spacing: 0.1em; text-transform: uppercase; color: #C0C8D8; padding: 0 1.2rem 0.7rem; border-bottom: 2px solid transparent; margin-bottom: -2px; }

/* Inputs */
.stTextInput input {
    background: #F8F6F2 !important;
    border: 1.5px solid #E2DDD6 !important;
    border-radius: 8px !important;
    color: #1A1A2E !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    transition: border-color 0.2s !important;
}
.stTextInput input:focus {
    border-color: #2D6A4F !important;
    box-shadow: 0 0 0 3px rgba(45,106,79,0.08) !important;
    background: #FFFFFF !important;
}
.stTextInput label {
    color: #6A7A8A !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
}

/* Button */
.stButton > button {
    background: #1B4332 !important;
    border: none !important;
    color: #FFFFFF !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
    width: 100% !important;
    padding: 0.75rem !important;
    transition: all 0.2s !important;
    box-shadow: 0 2px 8px rgba(27,67,50,0.25) !important;
}
.stButton > button:hover {
    background: #2D6A4F !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(27,67,50,0.3) !important;
}

/* Messages */
.err { background: #FEF2F2; border: 1px solid #FECACA; border-radius: 8px; padding: 0.7rem 1rem; font-size: 0.8rem; color: #DC2626; margin-bottom: 1rem; }
.suc { background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 8px; padding: 0.7rem 1rem; font-size: 0.8rem; color: #16A34A; margin-bottom: 1rem; }
.hint { font-size: 0.7rem; color: #A0ADB8; margin-top: 1.2rem; text-align: center; padding: 0.7rem; background: #F8F6F2; border-radius: 8px; line-height: 1.6; }
.hint strong { color: #6A7A8A; }

/* Nav card */
.nav-card { background: #F8F6F2; border: 1px solid #E8E2D8; border-radius: 12px; padding: 1.5rem; margin-top: 1rem; }
.nav-card-title { font-family: 'Playfair Display', serif; font-size: 1rem; color: #2D6A4F; margin-bottom: 1rem; }
[data-testid="stPageLink"] a {
    color: #1B4332 !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
}
</style>
""", unsafe_allow_html=True)

# Left panel HTML
st.markdown("""
<div class="login-wrap">
  <div class="left">
    <div class="left-badge">Evidence-Based Medical AI</div>
    <div class="left-title">Healthcare<br>knowledge at<br>your <em>fingertips</em></div>
    <div class="left-desc">MediQuery grounds every answer in the Gale Encyclopedia of Medicine — not the open internet — for reliable, sourced medical information.</div>
    <div class="feat-item"><div class="feat-dot"></div><div class="feat-text"><strong>RAG Pipeline</strong> — 7,470 indexed passages, semantic search</div></div>
    <div class="feat-item"><div class="feat-dot"></div><div class="feat-text"><strong>Personalised</strong> — Adapts to your age, BMI, blood pressure</div></div>
    <div class="feat-item"><div class="feat-dot"></div><div class="feat-text"><strong>Transparent</strong> — Every answer cites its source passages</div></div>
    <div class="feat-item"><div class="feat-dot"></div><div class="feat-text"><strong>Fast</strong> — Sub 2-second responses via Groq + Llama 3.1</div></div>
    <div class="left-stats">
      <div class="ls-item"><strong>759</strong><span>Source pages</span></div>
      <div class="ls-item"><strong>7,470</strong><span>Passages</span></div>
      <div class="ls-item"><strong>&lt;2s</strong><span>Response</span></div>
    </div>
  </div>
  <div class="right">
""", unsafe_allow_html=True)

# If logged in
if st.session_state.logged_in:
    st.markdown(f'<div class="suc">Signed in as <strong>{st.session_state.username}</strong>. Navigate below.</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-card"><div class="nav-card-title">Where would you like to go?</div>', unsafe_allow_html=True)
    st.page_link("pages/1_Home.py",    label="Home — Dashboard",       icon="🏠")
    st.page_link("pages/2_Query.py",   label="Query — Ask a question",  icon="🔍")
    st.page_link("pages/3_Metrics.py", label="Metrics — Performance",   icon="📊")
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("Sign Out"):
        st.session_state.logged_in=False; st.session_state.username=""; st.rerun()
    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# Tab switcher
c1,c2 = st.columns(2)
with c1:
    if st.button("Sign In",  key="t1"): st.session_state.auth_tab="login";    st.session_state.auth_error=""; st.rerun()
with c2:
    if st.button("Register", key="t2"): st.session_state.auth_tab="register"; st.session_state.auth_error=""; st.rerun()

tab = st.session_state.auth_tab
la = "tab-a" if tab=="login" else "tab-i"
ra = "tab-a" if tab=="register" else "tab-i"

st.markdown(f"""
    <div class="right-eyebrow">MediQuery</div>
    <div class="right-title">{"Welcome back" if tab=="login" else "Create account"}</div>
    <div class="right-sub">{"Sign in to access your medical assistant" if tab=="login" else "Join MediQuery — free forever"}</div>
    <div class="tab-row"><span class="{la}">Sign In</span><span class="{ra}">Register</span></div>
""", unsafe_allow_html=True)

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
    st.markdown('<div class="hint">Demo access &nbsp;·&nbsp; <strong>user:</strong> demo &nbsp;&nbsp;<strong>pass:</strong> demo123</div>', unsafe_allow_html=True)
else:
    nu  = st.text_input("Username", key="ru",  placeholder="choose a username")
    np  = st.text_input("Password", type="password", key="rp",  placeholder="min 6 characters")
    np2 = st.text_input("Confirm",  type="password", key="rp2", placeholder="repeat password")
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

st.markdown("</div></div>", unsafe_allow_html=True)
