#py -m streamlit run app.py
#py -m streamlit run first_streamlit_app/app.py

# ───────────────────────────────────────────────────────────────
# authenticator_test.py   (run with:  python -m streamlit run authenticator_test.py)
# ───────────────────────────────────────────────────────────────
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# ── 1. Load credentials ────────────────────────────────────────
with open("credentials.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

# ── 2. Create authenticator instance ───────────────────────────
authenticator = stauth.Authenticate(
    credentials=config["credentials"],
    cookie_name=config["cookie"]["name"],
    key=config["cookie"]["key"],
    expiry_days=config["cookie"]["expiry_days"],
)

# ── 3. Draw the login form ─────────────────────────────────────
try:
    authenticator.login()           # defaults: form in main area, caption “Login”
except Exception as e:
    st.error(e)

# ───────────────────────────────────────────────────────────────
# 4.  APP   (only appears when authentication_status == True)
# ───────────────────────────────────────────────────────────────
if st.session_state.get("authentication_status"):

    # 4-a  Logout button (in sidebar)
    authenticator.logout("Logout", "sidebar")

    # 4-b  Greeting
    st.sidebar.success(f"Welcome {st.session_state.get('name')}!")

    st.logo("logo-wavetransition_long.png", size="medium",link="https://www.wavetransition.com/")
    
    # 4-c  Simple multi-page navigation
    def home_page():
        st.header("🏠 Home")
        st.write("Put your landing-page widgets here.")

        

#    page = st.sidebar.radio("Navigate to:", ("Home", "Data", "About"))

    if page == "Home":
        home_page()


# ───────────────────────────────────────────────────────────────
# 5.  Feedback when login fails or form not yet submitted
# ───────────────────────────────────────────────────────────────
elif st.session_state.get("authentication_status") is False:
    st.error("Username or password incorrect.")
elif st.session_state.get("authentication_status") is None:
    st.warning("Please enter your username and password.")
