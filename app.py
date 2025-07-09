# ───────────────────────────────────────────────────────────────

# py -m streamlit run news_ranked_secrets_app.py

#bash
#cd ~/Documents/PYTHON_STREAMLIT/NEWSRANKER_CLOUD
# py -m streamlit run app.py

# ───────────────────────────────────────────────────────────────
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
#from pathlib import Path
import pandas as pd


#https://github.com/ikatyang/emoji-cheat-sheet

# ── 1. Custom Styling ───────────────────────────────────────────

# ── 2. Load credentials ─────────────────────────────────────────

#BASE_DIR = Path(__file__).resolve().parent
#path_to_save = BASE_DIR
file_path =  "credentials.yaml"

#config = yaml.safe_load(st.secrets["credentials"])
with open(file_path) as file:
   config = yaml.load(file, Loader=SafeLoader)

# ── 3. Create authenticator ────────────────────────────────────
authenticator = stauth.Authenticate(
    credentials=config["credentials"],
    cookie_name=config["cookie"]["name"],
    key=config["cookie"]["key"],
    expiry_days=config["cookie"]["expiry_days"],
)

# ── 4. Login Form ──────────────────────────────────────────────
try:
    authenticator.login()
except Exception as e:
    st.error(e)

# ── 5. Main App ────────────────────────────────────────────────
if st.session_state.get("authentication_status"):

    # App Header and Description
    st.header("📰 NewsRanker Application")
    """
    Welcome to Ranked News, your intelligent news-ranking platform powered by Machine Learning.

    Our app continuously analyzes and ranks the latest news articles based on advanced models that learn from evolving trends and key topics. Using a dynamic keyword-based ranking system enhanced with machine learning techniques, Ranked News prioritizes the most relevant and impactful articles from recent days.

    Whether it's about energy, technology, or market shifts, our app ensures that you see the most important news first—automatically adapting as new stories emerge.
    """    
    
            
    # Sidebar Layout
    st.sidebar.image("imagines/logo-wavetransition_long.png")  # Logo at top
    # Welcome message (sidebar)
    st.sidebar.success(f"Welcome {st.session_state.get('name')}!")
    # Logout at bottom (you may need to adjust authenticator object)
    authenticator.logout("Logout", "sidebar")
    
    st.sidebar.title("News Ranker")  # App title below logo
    st.sidebar.subheader("Articles prioritized based on Machine Learning.")
    # Space filler to push logout to the bottom (you can adjust)
    for _ in range(2):
        st.sidebar.markdown(" ")  # Adds vertical space

    # --- Main Area ---
    # Centered Date Input
    #st.markdown("<h2 style='text-align: center;'>Select Date:</h2>", unsafe_allow_html=True)
    #st.date_input("Today", key="date_input", label_visibility="collapsed")
  
    #st.subheader("Articles prioritized based on Machine Learning.")

    try:
        df = pd.read_csv("daily_ranked.csv")
        df['date'] = pd.to_datetime(df['date'], utc=True, format='ISO8601')
        min_datetime = df['date'].min()
        max_datetime = df['date'].max()
        min_display = min_datetime.strftime('%Y-%m-%d %H:%M')
        max_display = max_datetime.strftime('%Y-%m-%d %H:%M')
        #timezone_name = df['date'].dt.tz.zone  # Get timezone name from datetime column
        st.info(f"🕒 News covered from **{min_display}** to **{max_display}** (Timezone: UTC)")
                
        filtered_df = df[df["ranking"].isin([1, 2,3,4,5])]

        if filtered_df.empty:
            st.warning("No news articles found.")
        else:
            #st.sidebar.title("News Ranking Options")
            #max_items = st.sidebar.slider("Max articles per source", 1, 20, 5)
            grouped = filtered_df.groupby("ranking")

        for rank, group in grouped:
            group_sorted = group.sort_values(by='date', ascending=False)
            with st.expander(f"📰 Ranking: 🏷️ {rank}", expanded=False):
                with st.container():
                    for _, row in group_sorted.iterrows():
                        st.markdown(
                            f"• **[{row['title']}]({row['link']})** "
                            f"<br><sup>📅 {row['date']} | 🌐 {row['source']} | 🔤 {row['lang']}</sup>",
                            unsafe_allow_html=True,
                )
                        
         
                    


                    


    except Exception as e:
        st.error(f"Error loading news data: {e}")

# ── 6. Login Feedback ──────────────────────────────────────────
elif st.session_state.get("authentication_status") is False:
    st.error("Username or password incorrect.")
elif st.session_state.get("authentication_status") is None:
    st.warning("Please enter your username and password.")



# ───────────────────────────────────────────────────────────────
# 5.  Feedback when login fails or form not yet submitted
# ───────────────────────────────────────────────────────────────
elif st.session_state.get("authentication_status") is False:
    st.error("Username or password incorrect.")
elif st.session_state.get("authentication_status") is None:
    st.warning("Please enter your username and password.")
