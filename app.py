"""
app.py — MediQuery Login Page
Fixed: no st.switch_page, uses session state + st.rerun() instead
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

# Load API key from Streamlit secrets
try:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
except Exception:
    pass

# ── User store ────────────────────────────────────────────
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

# Session defaults
for k,v in [("logged_in",False),("username",""),("auth_tab","login"),("auth_error",""),("auth_success","")]:
    if k not in st.session_state: st.session_state[k] = v

# ── CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&family=Jost:wght@300;400;500&display=swap');
html,body,[data-testid="stAppViewContainer"]{background:#0D1117;font-family:'Jost',sans-serif;color:#E8E0D0;}
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="collapsedControl"]{display:none!important;}
[data-testid="block-container"]{padding:3rem 1rem 2rem!important;max-width:480px!important;margin:0 auto!important;}

.brand{text-align:center;margin-bottom:2.5rem;}
.brand-mark{width:56px;height:56px;border:1.5px solid rgba(200,180,140,0.5);border-radius:14px;display:inline-flex;align-items:center;justify-content:center;font-family:'Cormorant Garamond',serif;font-size:1.6rem;color:#C8B47A;margin-bottom:1rem;}
.brand-name{font-family:'Cormorant Garamond',serif;font-size:1.8rem;color:#F5EFE4;font-weight:300;}
.brand-sub{font-size:0.68rem;letter-spacing:0.2em;text-transform:uppercase;color:#3A4A58;margin-top:0.2rem;}

.card{background:rgba(255,255,255,0.025);border:1px solid rgba(200,180,140,0.1);border-radius:16px;padding:2rem;margin-bottom:1rem;animation:fadeUp 0.6s ease forwards;opacity:0;}
@keyframes fadeUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}

.tab-row{display:flex;border-bottom:1px solid rgba(200,180,140,0.1);margin-bottom:1.5rem;gap:0;}
.tab-active{font-size:0.75rem;letter-spacing:0.1em;text-transform:uppercase;color:#C8B47A;padding:0 1rem 0.7rem;border-bottom:2px solid #C8B47A;font-weight:500;}
.tab-inactive{font-size:0.75rem;letter-spacing:0.1em;text-transform:uppercase;color:#2A3A48;padding:0 1rem 0.7rem;border-bottom:2px solid transparent;}

.stTextInput input{background:rgba(255,255,255,0.04)!important;border:1px solid rgba(200,180,140,0.15)!important;border-radius:8px!important;color:#E8E0D0!important;font-family:'Jost',sans-serif!important;}
.stTextInput input:focus{border-color:rgba(200,180,140,0.4)!important;box-shadow:0 0 0 3px rgba(200,180,140,0.06)!important;}
.stTextInput label{color:#3A4A58!important;font-size:0.68rem!important;letter-spacing:0.1em!important;text-transform:uppercase!important;}

.stButton>button{background:linear-gradient(135deg,#1C2B3A,#243647)!important;border:1px solid rgba(200,180,140,0.25)!important;color:#C8B47A!important;border-radius:8px!important;font-family:'Jost',sans-serif!important;font-size:0.78rem!important;letter-spacing:0.12em!important;text-transform:uppercase!important;width:100%!important;padding:0.7rem!important;transition:all 0.2s!important;}
.stButton>button:hover{border-color:rgba(200,180,140,0.5)!important;transform:translateY(-1px)!important;}

.err{background:rgba(180,60,60,0.1);border:1px solid rgba(180,60,60,0.25);border-radius:6px;padding:0.7rem 1rem;font-size:0.8rem;color:#E89090;margin-bottom:1rem;}
.suc{background:rgba(60,180,100,0.08);border:1px solid rgba(60,180,100,0.2);border-radius:6px;padding:0.7rem 1rem;font-size:0.8rem;color:#80D8A0;margin-bottom:1rem;}
.hint{font-size:0.7rem;color:#2A3A48;margin-top:1rem;text-align:center;padding:0.6rem;border:1px solid rgba(200,180,140,0.07);border-radius:6px;line-height:1.6;}
.hint strong{color:#3A4A58;}

.stats-footer{display:flex;justify-content:center;gap:2.5rem;margin-top:1.5rem;padding-top:1.5rem;border-top:1px solid rgba(200,180,140,0.07);}
.sf-item{text-align:center;}
.sf-val{font-family:'Cormorant Garamond',serif;font-size:1.3rem;color:#8A9AA8;}
.sf-lbl{font-size:0.6rem;letter-spacing:0.12em;text-transform:uppercase;color:#2A3A48;margin-top:0.1rem;}

/* bg stars */
.stars{position:fixed;inset:0;z-index:-1;background:radial-gradient(ellipse at 20% 50%,rgba(180,140,100,0.05) 0%,transparent 60%),#0D1117;}
</style>
<div class="stars"></div>
""", unsafe_allow_html=True)

# Brand header
st.markdown("""
<div class="brand">
    <div class="brand-mark">M</div>
    <div class="brand-name">MediQuery</div>
    <div class="brand-sub">AI Medical Knowledge Assistant</div>
</div>
""", unsafe_allow_html=True)

# ── If logged in show a redirect button (safe, no switch_page) ──
if st.session_state.logged_in:
    st.success(f"Signed in as {st.session_state.username}. Use the sidebar to navigate.")
    st.stop()

# Tab buttons
c1, c2 = st.columns(2)
with c1:
    if st.button("Sign In", key="t1"):
        st.session_state.auth_tab="login"; st.session_state.auth_error=""; st.rerun()
with c2:
    if st.button("Register", key="t2"):
        st.session_state.auth_tab="register"; st.session_state.auth_error=""; st.rerun()

tab = st.session_state.auth_tab
login_active   = "tab-active"   if tab=="login"    else "tab-inactive"
reg_active     = "tab-active"   if tab=="register"  else "tab-inactive"
st.markdown(f'<div class="tab-row"><span class="{login_active}">Sign In</span><span class="{reg_active}">Register</span></div>', unsafe_allow_html=True)

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
            st.session_state.logged_in = True
            st.session_state.username  = username
            st.session_state.auth_error = ""
            st.session_state.auth_success = ""
        st.rerun()
    st.markdown('<div class="hint">Demo &nbsp;·&nbsp; <strong>user:</strong> demo &nbsp;<strong>pass:</strong> demo123</div>', unsafe_allow_html=True)
else:
    nu  = st.text_input("Username", key="ru", placeholder="choose a username")
    np  = st.text_input("Password", type="password", key="rp",  placeholder="min 6 characters")
    np2 = st.text_input("Confirm",  type="password", key="rp2", placeholder="repeat password")
    if st.button("Create Account  →", key="do_reg"):
        if not nu or not np:  st.session_state.auth_error = "All fields required."
        elif len(np)<6:       st.session_state.auth_error = "Password must be 6+ characters."
        elif np!=np2:         st.session_state.auth_error = "Passwords don't match."
        elif nu in users:     st.session_state.auth_error = "Username taken."
        else:
            users[nu]=hash_pw(np); save_users(users)
            st.session_state.auth_success = f"Account created! Sign in as {nu}."
            st.session_state.auth_tab="login"; st.session_state.auth_error=""
        st.rerun()

st.markdown("""
<div class="stats-footer">
    <div class="sf-item"><div class="sf-val">759</div><div class="sf-lbl">Source pages</div></div>
    <div class="sf-item"><div class="sf-val">7,470</div><div class="sf-lbl">Passages</div></div>
    <div class="sf-item"><div class="sf-val">&lt;2s</div><div class="sf-lbl">Response</div></div>
</div>
""", unsafe_allow_html=True)
