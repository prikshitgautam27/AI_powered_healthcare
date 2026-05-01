"""
app.py — MediQuery Entry Point
Handles animated landing + login/register on same page.
"""
import streamlit as st
import hashlib, time, json
from pathlib import Path

st.set_page_config(
    page_title="MediQuery — AI Medical Assistant",
    page_icon="M",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── User store (JSON file, simple auth) ──────────────────
USERS_FILE = Path("users.json")

def load_users():
    if USERS_FILE.exists():
        return json.loads(USERS_FILE.read_text())
    # Default demo accounts
    defaults = {
        "demo": hashlib.sha256("demo123".encode()).hexdigest(),
        "admin": hashlib.sha256("admin123".encode()).hexdigest(),
    }
    USERS_FILE.write_text(json.dumps(defaults))
    return defaults

def save_users(users):
    USERS_FILE.write_text(json.dumps(users))

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# ── Session defaults ──────────────────────────────────────
if "logged_in"   not in st.session_state: st.session_state.logged_in   = False
if "username"    not in st.session_state: st.session_state.username    = ""
if "auth_tab"    not in st.session_state: st.session_state.auth_tab    = "login"
if "auth_error"  not in st.session_state: st.session_state.auth_error  = ""
if "auth_success"not in st.session_state: st.session_state.auth_success= ""

# ── If already logged in, redirect ───────────────────────
if st.session_state.logged_in:
    st.switch_page("1_Home.py")

# ── Full-page CSS ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Jost:wght@300;400;500&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: #0D1117;
    font-family: 'Jost', sans-serif;
    color: #E8E0D0;
}
#MainMenu, footer, header, [data-testid="stToolbar"],
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="block-container"] {
    padding: 0 !important;
    max-width: 100% !important;
}
section.main > div { padding: 0 !important; }

/* ── Animated background ── */
.bg-canvas {
    position: fixed; inset: 0; z-index: 0;
    background: radial-gradient(ellipse at 20% 50%, rgba(180,140,100,0.06) 0%, transparent 60%),
                radial-gradient(ellipse at 80% 20%, rgba(100,160,200,0.05) 0%, transparent 60%),
                #0D1117;
    overflow: hidden;
}
.bg-canvas::before {
    content: '';
    position: absolute; inset: 0;
    background-image:
        radial-gradient(1px 1px at 20% 30%, rgba(200,180,140,0.3) 0%, transparent 0%),
        radial-gradient(1px 1px at 60% 70%, rgba(200,180,140,0.2) 0%, transparent 0%),
        radial-gradient(1px 1px at 80% 15%, rgba(200,180,140,0.25) 0%, transparent 0%),
        radial-gradient(1px 1px at 40% 85%, rgba(200,180,140,0.15) 0%, transparent 0%),
        radial-gradient(1px 1px at 90% 50%, rgba(200,180,140,0.2) 0%, transparent 0%);
    background-size: 300px 300px, 400px 400px, 250px 250px, 350px 350px, 200px 200px;
    animation: starfield 40s linear infinite;
}
@keyframes starfield { from { transform: translateY(0); } to { transform: translateY(-300px); } }

/* ── Split layout ── */
.page-wrap {
    position: relative; z-index: 1;
    min-height: 100vh;
    display: grid;
    grid-template-columns: 1fr 1fr;
}

/* ── Left panel ── */
.left-panel {
    display: flex; flex-direction: column;
    justify-content: center; padding: 4rem 3rem 4rem 4rem;
    border-right: 1px solid rgba(200,180,140,0.1);
    animation: fadeSlideLeft 0.8s ease forwards;
    opacity: 0;
}
@keyframes fadeSlideLeft {
    from { opacity: 0; transform: translateX(-30px); }
    to   { opacity: 1; transform: translateX(0); }
}
.brand-mark {
    width: 52px; height: 52px;
    border: 1.5px solid rgba(200,180,140,0.5);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.4rem; color: #C8B47A;
    margin-bottom: 2.5rem;
    position: relative;
}
.brand-mark::after {
    content: '';
    position: absolute; inset: -4px;
    border: 1px solid rgba(200,180,140,0.15);
    border-radius: 15px;
}
.left-tagline {
    font-size: 0.68rem; letter-spacing: 0.2em;
    text-transform: uppercase; color: #C8B47A;
    margin-bottom: 1.2rem; font-weight: 400;
}
.left-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3.2rem; line-height: 1.1;
    color: #F5EFE4; font-weight: 300;
    margin-bottom: 1.5rem;
}
.left-title em { font-style: italic; color: #C8B47A; }
.left-desc {
    font-size: 0.88rem; color: #7A8590;
    line-height: 1.75; font-weight: 300;
    margin-bottom: 2.5rem; max-width: 380px;
}
.feature-list { display: flex; flex-direction: column; gap: 0.9rem; }
.feature-item {
    display: flex; align-items: flex-start; gap: 0.8rem;
    animation: fadeSlideLeft 0.8s ease forwards; opacity: 0;
}
.feature-item:nth-child(1) { animation-delay: 0.3s; }
.feature-item:nth-child(2) { animation-delay: 0.45s; }
.feature-item:nth-child(3) { animation-delay: 0.6s; }
.feature-item:nth-child(4) { animation-delay: 0.75s; }
.feature-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #C8B47A; margin-top: 6px; flex-shrink: 0;
}
.feature-text { font-size: 0.82rem; color: #8A9AA8; line-height: 1.5; }
.feature-text strong { color: #C0CEDB; font-weight: 500; }

/* ── Stats row ── */
.stats-row {
    display: flex; gap: 2rem;
    margin-top: 2.5rem; padding-top: 2rem;
    border-top: 1px solid rgba(200,180,140,0.1);
}
.stat-item strong {
    display: block;
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.6rem; color: #F5EFE4; font-weight: 300;
}
.stat-item span { font-size: 0.68rem; color: #4A5A68; letter-spacing: 0.1em; text-transform: uppercase; }

/* ── Right panel (auth) ── */
.right-panel {
    display: flex; flex-direction: column;
    justify-content: center; padding: 4rem 4rem 4rem 3rem;
    animation: fadeSlideRight 0.8s ease 0.2s forwards;
    opacity: 0;
}
@keyframes fadeSlideRight {
    from { opacity: 0; transform: translateX(30px); }
    to   { opacity: 1; transform: translateX(0); }
}
.auth-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2rem; color: #F5EFE4; font-weight: 300;
    margin-bottom: 0.4rem;
}
.auth-sub { font-size: 0.82rem; color: #4A5A68; margin-bottom: 2rem; }

/* ── Tab switcher ── */
.tab-row { display: flex; gap: 0; margin-bottom: 1.8rem; border-bottom: 1px solid rgba(200,180,140,0.1); }
.tab-btn {
    padding: 0.5rem 1.2rem; cursor: pointer;
    font-size: 0.8rem; letter-spacing: 0.08em;
    text-transform: uppercase; color: #4A5A68;
    border-bottom: 2px solid transparent;
    transition: all 0.2s; background: transparent; border-top: none; border-left: none; border-right: none;
}
.tab-btn.active { color: #C8B47A; border-bottom-color: #C8B47A; }

/* ── Form inputs ── */
.stTextInput input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(200,180,140,0.2) !important;
    border-radius: 8px !important;
    color: #E8E0D0 !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 0.88rem !important;
    padding: 0.7rem 1rem !important;
    transition: border-color 0.2s !important;
}
.stTextInput input:focus {
    border-color: rgba(200,180,140,0.5) !important;
    box-shadow: 0 0 0 3px rgba(200,180,140,0.06) !important;
    background: rgba(255,255,255,0.06) !important;
}
.stTextInput label {
    color: #6A7A88 !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}

/* ── Submit button ── */
.stButton > button {
    background: linear-gradient(135deg, #1C2B3A, #243647) !important;
    border: 1px solid rgba(200,180,140,0.3) !important;
    color: #C8B47A !important;
    border-radius: 8px !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 0.7rem 1.5rem !important;
    width: 100% !important;
    transition: all 0.25s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #243647, #2E4459) !important;
    border-color: rgba(200,180,140,0.6) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.3) !important;
}

/* ── Messages ── */
.msg-error {
    background: rgba(180,60,60,0.12);
    border: 1px solid rgba(180,60,60,0.3);
    border-radius: 6px; padding: 0.7rem 1rem;
    font-size: 0.82rem; color: #E89090;
    margin-bottom: 1rem;
}
.msg-success {
    background: rgba(60,180,100,0.1);
    border: 1px solid rgba(60,180,100,0.25);
    border-radius: 6px; padding: 0.7rem 1rem;
    font-size: 0.82rem; color: #80D8A0;
    margin-bottom: 1rem;
}
.demo-hint {
    font-size: 0.72rem; color: #3A4A58;
    margin-top: 1.2rem; text-align: center;
    padding: 0.7rem; border: 1px solid rgba(200,180,140,0.08);
    border-radius: 6px; line-height: 1.6;
}
.demo-hint strong { color: #5A6A78; }
</style>
<div class="bg-canvas"></div>
""", unsafe_allow_html=True)

# ── Layout HTML ───────────────────────────────────────────
st.markdown("""
<div class="page-wrap">
  <div class="left-panel">
    <div class="brand-mark">M</div>
    <div class="left-tagline">Evidence-Based Medical Intelligence</div>
    <div class="left-title">Know your<br>health with<br><em>precision</em></div>
    <div class="left-desc">
      MediQuery delivers context-aware medical answers grounded in the
      Gale Encyclopedia of Medicine — not the open internet.
    </div>
    <div class="feature-list">
      <div class="feature-item">
        <div class="feature-dot"></div>
        <div class="feature-text"><strong>RAG Pipeline</strong> — Semantic retrieval over 7,470 indexed passages</div>
      </div>
      <div class="feature-item">
        <div class="feature-dot"></div>
        <div class="feature-text"><strong>Personalised context</strong> — Answers adapt to your health parameters</div>
      </div>
      <div class="feature-item">
        <div class="feature-dot"></div>
        <div class="feature-text"><strong>Source transparency</strong> — Every answer shows its encyclopedia passages</div>
      </div>
      <div class="feature-item">
        <div class="feature-dot"></div>
        <div class="feature-text"><strong>Sub-2s responses</strong> — Powered by Llama 3.1 via Groq</div>
      </div>
    </div>
    <div class="stats-row">
      <div class="stat-item"><strong>759</strong><span>Source pages</span></div>
      <div class="stat-item"><strong>7,470</strong><span>Passages</span></div>
      <div class="stat-item"><strong>&lt; 2s</strong><span>Response</span></div>
    </div>
  </div>
  <div class="right-panel">
""", unsafe_allow_html=True)

# ── Auth form (rendered inside right panel) ───────────────
st.markdown(f"""
    <div class="auth-title">{"Welcome back" if st.session_state.auth_tab == "login" else "Create account"}</div>
    <div class="auth-sub">{"Sign in to access MediQuery" if st.session_state.auth_tab == "login" else "Join MediQuery — it's free"}</div>
    <div class="tab-row">
      <button class="tab-btn {'active' if st.session_state.auth_tab == 'login' else ''}"
        onclick="window.location.href='?tab=login'">Sign In</button>
      <button class="tab-btn {'active' if st.session_state.auth_tab == 'register' else ''}"
        onclick="window.location.href='?tab=register'">Register</button>
    </div>
""", unsafe_allow_html=True)

# Tab switcher via query params
params = st.query_params
if "tab" in params:
    st.session_state.auth_tab = params["tab"]

col1, col2 = st.columns([1,1])
with col1:
    if st.button("Sign In", key="tab_login"):
        st.session_state.auth_tab = "login"
        st.session_state.auth_error = ""
        st.rerun()
with col2:
    if st.button("Register", key="tab_register"):
        st.session_state.auth_tab = "register"
        st.session_state.auth_error = ""
        st.rerun()

# Error / success messages
if st.session_state.auth_error:
    st.markdown(f'<div class="msg-error">{st.session_state.auth_error}</div>', unsafe_allow_html=True)
if st.session_state.auth_success:
    st.markdown(f'<div class="msg-success">{st.session_state.auth_success}</div>', unsafe_allow_html=True)

users = load_users()

if st.session_state.auth_tab == "login":
    username = st.text_input("Username", key="li_user", placeholder="your username")
    password = st.text_input("Password", type="password", key="li_pass", placeholder="••••••••")
    if st.button("Sign In  →", key="do_login"):
        if not username or not password:
            st.session_state.auth_error = "Please fill in both fields."
        elif username not in users or users[username] != hash_pw(password):
            st.session_state.auth_error = "Invalid username or password."
        else:
            st.session_state.logged_in = True
            st.session_state.username  = username
            st.session_state.auth_error = ""
            st.switch_page("1_Home.py")
        st.rerun()
    st.markdown("""
    <div class="demo-hint">
      Demo access &nbsp;·&nbsp;
      <strong>Username:</strong> demo &nbsp;&nbsp;
      <strong>Password:</strong> demo123
    </div>""", unsafe_allow_html=True)

else:
    new_user = st.text_input("Choose username", key="reg_user", placeholder="yourname")
    new_pass = st.text_input("Choose password", type="password", key="reg_pass", placeholder="min 6 characters")
    new_pass2= st.text_input("Confirm password", type="password", key="reg_pass2", placeholder="repeat password")
    if st.button("Create Account  →", key="do_register"):
        if not new_user or not new_pass:
            st.session_state.auth_error = "All fields are required."
        elif len(new_pass) < 6:
            st.session_state.auth_error = "Password must be at least 6 characters."
        elif new_pass != new_pass2:
            st.session_state.auth_error = "Passwords do not match."
        elif new_user in users:
            st.session_state.auth_error = "Username already taken."
        else:
            users[new_user] = hash_pw(new_pass)
            save_users(users)
            st.session_state.auth_success = f"Account created! Sign in as {new_user}."
            st.session_state.auth_tab = "login"
            st.session_state.auth_error = ""
        st.rerun()

st.markdown("</div></div>", unsafe_allow_html=True)
