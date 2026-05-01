"""
app.py — MediQuery Login · Fixed post-login navigation
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
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&family=Jost:wght@300;400;500&display=swap');
html,body,[data-testid="stAppViewContainer"]{background:#0D1117;font-family:'Jost',sans-serif;color:#E8E0D0;}
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="collapsedControl"]{display:none!important;}
[data-testid="block-container"]{padding:3rem 1rem 2rem!important;max-width:460px!important;margin:0 auto!important;}

.brand{text-align:center;margin-bottom:2.5rem;}
.bmark{width:60px;height:60px;border:1.5px solid rgba(200,180,140,0.5);border-radius:14px;display:inline-flex;align-items:center;justify-content:center;font-family:'Cormorant Garamond',serif;font-size:1.8rem;color:#C8B47A;margin-bottom:1rem;}
.bname{font-family:'Cormorant Garamond',serif;font-size:2rem;color:#F5EFE4;font-weight:300;}
.bsub{font-size:0.65rem;letter-spacing:0.22em;text-transform:uppercase;color:#2A3A48;margin-top:0.3rem;}

.tab-row{display:flex;border-bottom:1px solid rgba(200,180,140,0.1);margin-bottom:1.5rem;}
.tab-a{font-size:0.72rem;letter-spacing:0.1em;text-transform:uppercase;color:#C8B47A;padding:0 1rem 0.6rem;border-bottom:2px solid #C8B47A;}
.tab-i{font-size:0.72rem;letter-spacing:0.1em;text-transform:uppercase;color:#2A3A48;padding:0 1rem 0.6rem;border-bottom:2px solid transparent;}

.stTextInput input{background:rgba(255,255,255,0.04)!important;border:1px solid rgba(200,180,140,0.15)!important;border-radius:8px!important;color:#E8E0D0!important;font-family:'Jost',sans-serif!important;}
.stTextInput input:focus{border-color:rgba(200,180,140,0.4)!important;box-shadow:0 0 0 3px rgba(200,180,140,0.06)!important;}
.stTextInput label{color:#3A4A58!important;font-size:0.68rem!important;letter-spacing:0.1em!important;text-transform:uppercase!important;}
.stButton>button{background:linear-gradient(135deg,#1C2B3A,#243647)!important;border:1px solid rgba(200,180,140,0.25)!important;color:#C8B47A!important;border-radius:8px!important;font-family:'Jost',sans-serif!important;font-size:0.78rem!important;letter-spacing:0.12em!important;text-transform:uppercase!important;width:100%!important;padding:0.7rem!important;transition:all 0.2s!important;}
.stButton>button:hover{border-color:rgba(200,180,140,0.5)!important;transform:translateY(-1px)!important;}
.err{background:rgba(180,60,60,0.1);border:1px solid rgba(180,60,60,0.25);border-radius:6px;padding:0.7rem 1rem;font-size:0.8rem;color:#E89090;margin-bottom:1rem;}
.suc{background:rgba(60,180,100,0.08);border:1px solid rgba(60,180,100,0.2);border-radius:6px;padding:0.7rem 1rem;font-size:0.8rem;color:#80D8A0;margin-bottom:1rem;}
.hint{font-size:0.68rem;color:#2A3A48;margin-top:1rem;text-align:center;padding:0.6rem;border:1px solid rgba(200,180,140,0.07);border-radius:6px;line-height:1.6;}
.hint strong{color:#3A4A58;}
.nav-card{background:rgba(255,255,255,0.025);border:1px solid rgba(200,180,140,0.12);border-radius:12px;padding:1.5rem;margin-top:1rem;text-align:center;}
.nav-title{font-family:'Cormorant Garamond',serif;font-size:1.1rem;color:#C8B47A;margin-bottom:1rem;}
.nav-links{display:flex;flex-direction:column;gap:0.6rem;}
.stars{position:fixed;inset:0;z-index:-1;background:radial-gradient(ellipse at 20% 50%,rgba(180,140,100,0.05) 0%,transparent 60%),#0D1117;}
</style>
<div class="stars"></div>
""", unsafe_allow_html=True)

# Brand
st.markdown("""
<div class="brand">
    <div class="bmark">M</div>
    <div class="bname">MediQuery</div>
    <div class="bsub">AI Medical Knowledge Assistant</div>
</div>
""", unsafe_allow_html=True)

# ── If already logged in: show navigation card ────────────
if st.session_state.logged_in:
    st.markdown(f'<div class="suc">Signed in as <strong>{st.session_state.username}</strong>. Navigate using the links below.</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-card"><div class="nav-title">Go to</div><div class="nav-links">', unsafe_allow_html=True)
    st.page_link("pages/1_Home.py",    label="Home — Dashboard",      icon="○")
    st.page_link("pages/2_Query.py",   label="Query — Ask a question", icon="◇")
    st.page_link("pages/3_Metrics.py", label="Metrics — Performance",  icon="△")
    st.markdown('</div></div>', unsafe_allow_html=True)
    if st.button("Sign Out"):
        st.session_state.logged_in=False; st.session_state.username=""; st.rerun()
    st.stop()

# ── Tab switcher ──────────────────────────────────────────
c1,c2 = st.columns(2)
with c1:
    if st.button("Sign In",  key="t1"): st.session_state.auth_tab="login";    st.session_state.auth_error=""; st.rerun()
with c2:
    if st.button("Register", key="t2"): st.session_state.auth_tab="register"; st.session_state.auth_error=""; st.rerun()

tab = st.session_state.auth_tab
la = "tab-a" if tab=="login"    else "tab-i"
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
            st.session_state.logged_in   = True
            st.session_state.username    = username
            st.session_state.auth_error  = ""
            st.session_state.auth_success= ""
        st.rerun()
    st.markdown('<div class="hint">Demo &nbsp;·&nbsp; <strong>user:</strong> demo &nbsp;<strong>pass:</strong> demo123</div>', unsafe_allow_html=True)
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

st.markdown("""
<div style="display:flex;justify-content:center;gap:2.5rem;margin-top:2rem;padding-top:1.5rem;border-top:1px solid rgba(200,180,140,0.07);">
    <div style="text-align:center;"><div style="font-family:'Cormorant Garamond',serif;font-size:1.3rem;color:#5A6A78;">759</div><div style="font-size:0.58rem;letter-spacing:0.12em;text-transform:uppercase;color:#1A2A38;margin-top:0.1rem;">Pages</div></div>
    <div style="text-align:center;"><div style="font-family:'Cormorant Garamond',serif;font-size:1.3rem;color:#5A6A78;">7,470</div><div style="font-size:0.58rem;letter-spacing:0.12em;text-transform:uppercase;color:#1A2A38;margin-top:0.1rem;">Passages</div></div>
    <div style="text-align:center;"><div style="font-family:'Cormorant Garamond',serif;font-size:1.3rem;color:#5A6A78;">&lt;2s</div><div style="font-size:0.58rem;letter-spacing:0.12em;text-transform:uppercase;color:#1A2A38;margin-top:0.1rem;">Response</div></div>
</div>
""", unsafe_allow_html=True)
