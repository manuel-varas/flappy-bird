import streamlit as st
import random
import streamlit.components.v1 as components

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Flappy Bird - Streamlit",
    layout="centered"
)

# ---------------- SESSION STATE ----------------
if "y" not in st.session_state:
    st.session_state.y = 250
    st.session_state.velocity = 0
    st.session_state.pipe_x = 400
    st.session_state.pipe_gap_y = random.randint(120, 300)
    st.session_state.score = 0
    st.session_state.game_over = False

# ---------------- CONSTANTS ----------------
WIDTH = 400
HEIGHT = 500
PIPE_WIDTH = 60
PIPE_GAP = 150
GRAVITY = 1.2
FLAP_STRENGTH = -10
PIPE_SPEED = 5

