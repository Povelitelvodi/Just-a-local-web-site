import streamlit as st
import time
import random
import base64
import os
from datetime import datetime

st.set_page_config(page_title="Personal web site", page_icon="👀", layout="wide")


def play_sound(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
                <audio autoplay="true">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
            st.markdown(md, unsafe_allow_html=True)

if "habits" not in st.session_state:
    st.session_state.habits = {
        "Rest for 30 mins": [False] * 7,
        "Drink 2L of water": [False] * 7,
        "Do a warm-up": [False] * 7
    }


VIBES = [
    "⚡ Hard code becomes simple when you break it into a cup of coffee and three breaks.",
    "👾 Your code doesn't work? Congratulations, you're an official programmer. Go take a 5-minute walk.",
    "🌊 Daily vibe: Write code as if the person who will maintain it is you in six months.",
    "🚀 Small steps every day create big results. Just make one commit.",
    "🪵 An error in the code is not a failure. It's a feature you haven't fully understood yet."
]

st.title("⚡ Personal web site")
st.markdown(f"uhh just a random local site lol. Today: **{datetime.now().strftime('%d.%m.%Y')}**")
st.markdown("---")


col1, col2 = st.columns(2, gap="large")

# ================= TIMER =================
with col1:
    st.header("⏱️ Timer")
    st.caption("Timer with cool sound in the end")
    
    duration = st.slider("Set timer for how long?", min_value=1, max_value=60, value=25)
    
    timer_placeholder = st.empty()
    progress_bar = st.progress(0)
    
    if st.button("🏁 Start timer", use_container_width=True):
        seconds = duration * 60
        total_seconds = seconds
        
        while seconds > 0:
            mins, secs = divmod(seconds, 60)
            timer_placeholder.metric(label="Time remaining", value=f"{mins:02d}:{secs:02d}")
            
            progress_percent = int(((total_seconds - seconds) / total_seconds) * 100)
            progress_bar.progress(progress_percent)
            
            time.sleep(1)
            seconds -= 1
            
        timer_placeholder.success("🎉 Time's up!")
        
        # that one sound.mp3
        play_sound("sound.mp3")
        
        st.balloons() 

# ================= tracker =================
with col2:
    st.header("📅 Tracker")
    st.caption("Mark the checkboxes each day. Progress is saved while the app is running.")
    
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    for habit, progress in st.session_state.habits.items():
        st.write(f"**{habit}**")
        cols = st.columns(7)
        for i, day in enumerate(days_of_week):
            with cols[i]:
                st.session_state.habits[habit][i] = st.checkbox(
                    day, 
                    value=st.session_state.habits[habit][i], 
                    key=f"{habit}_{day}"
                )
                
    st.markdown("---")
    
    st.header("🔮 Thought of the day (made without ai 100%)")
    if st.button("🎲 Catch a new idea"):
        st.session_state.current_vibe = random.choice(VIBES)
        
    if "current_vibe" not in st.session_state:
        st.session_state.current_vibe = VIBES[0]
        
    st.info(st.session_state.current_vibe)
