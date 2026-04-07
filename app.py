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

# ---------------- FLAP ----------------
def flap():
    if not st.session_state.game_over:
        st.session_state.velocity = FLAP_STRENGTH

# ---------------- RESET ----------------
def reset():
    st.session_state.y = 250
    st.session_state.velocity = 0
    st.session_state.pipe_x = 400
    st.session_state.pipe_gap_y = random.randint(120, 300)
    st.session_state.score = 0
    st.session_state.game_over = False

# ---------------- GAME LOOP ----------------
if not st.session_state.game_over:
    st.session_state.velocity += GRAVITY
    st.session_state.y += st.session_state.velocity
    st.session_state.pipe_x -= PIPE_SPEED

    if st.session_state.pipe_x < -PIPE_WIDTH:
        st.session_state.pipe_x = WIDTH
        st.session_state.pipe_gap_y = random.randint(120, 300)
        st.session_state.score += 1

# ---------------- COLLISION ----------------
bird_x = 100
bird_radius = 12

top_pipe_bottom = st.session_state.pipe_gap_y
bottom_pipe_top = st.session_state.pipe_gap_y + PIPE_GAP

if (
    st.session_state.pipe_x < bird_x < st.session_state.pipe_x + PIPE_WIDTH
    and (st.session_state.y < top_pipe_bottom or st.session_state.y > bottom_pipe_top)
):
    st.session_state.game_over = True

if st.session_state.y < 0 or st.session_state.y > HEIGHT:
    st.session_state.game_over = True

# ---------------- UI ----------------
st.title("🐦 Flappy Bird")
st.markdown(f"### 🏆 Pontuação: **{st.session_state.score}**")

# ---------------- SVG RENDER (CORRETO) ----------------
game_html = f"""
<div style="display:flex; justify-content:center;">
<svg width="{WIDTH}" height="{HEIGHT}" style="background:#87CEEB">
    <!-- Bird -->
    <circle cx="{bird_x}" cy="{st.session_state.y}" r="{bird_radius}" fill="yellow" />

    <!-- Top Pipe -->
    <rect x="{st.session_state.pipe_x}" y="0"
        width="{PIPE_WIDTH}" height="{top_pipe_bottom}"
        fill="green"/>

    <!-- Bottom Pipe -->
    <rect x="{st.session_state.pipe_x}" y="{bottom_pipe_top}"
        width="{PIPE_WIDTH}" height="{HEIGHT}"
        fill="green"/>
</svg>
</div>
"""

components.html(game_html, height=HEIGHT + 20)

# ---------------- CONTROLS ----------------
col1, col2 = st.columns(2)

with col1:
    st.button("⬆️ FLAP", on_click=flap)

with col2:
    st.button("🔄 RESET", on_click=reset)

if st.session_state.game_over:
    st.error("💥 GAME OVER 💥")
