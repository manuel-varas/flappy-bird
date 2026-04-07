import streamlit as st
import random
import time
import streamlit.components.v1 as components

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Flappy Bird", layout="centered")

# ---------------- RERUN COMPAT (NOVO/ANTIGO) ----------------
def do_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

# ---------------- SESSION STATE ----------------
if "init" not in st.session_state:
    st.session_state.init = True
    st.session_state.y = 250.0
    st.session_state.vy = 0.0
    st.session_state.pipe_x = 400.0
    st.session_state.gap_y = float(random.randint(120, 300))
    st.session_state.score = 0
    st.session_state.game_over = False

# ---------------- CONSTANTS ----------------
WIDTH = 400
HEIGHT = 500
BIRD_X = 100
BIRD_R = 12
PIPE_W = 60
GAP = 150
GRAVITY = 1.1
FLAP = -9.0
PIPE_SPEED = 4.0
FPS = 0.03  # 0.02 mais rápido, 0.05 mais lento

# ---------------- ACTIONS ----------------
def flap():
    if not st.session_state.game_over:
        st.session_state.vy = FLAP

def reset():
    st.session_state.y = 250.0
    st.session_state.vy = 0.0
    st.session_state.pipe_x = 400.0
    st.session_state.gap_y = float(random.randint(120, 300))
    st.session_state.score = 0
    st.session_state.game_over = False

# ---------------- GAME TICK ----------------
if not st.session_state.game_over:
    st.session_state.vy += GRAVITY
    st.session_state.y += st.session_state.vy
    st.session_state.pipe_x -= PIPE_SPEED

    if st.session_state.pipe_x < -PIPE_W:
        st.session_state.pipe_x = float(WIDTH)
        st.session_state.gap_y = float(random.randint(120, 300))
        st.session_state.score += 1

# ---------------- COLLISION ----------------
top_pipe_h = st.session_state.gap_y
bottom_pipe_y = st.session_state.gap_y + GAP

# colisão no cano (x dentro do cano e y fora do gap)
if (st.session_state.pipe_x < BIRD_X < st.session_state.pipe_x + PIPE_W) and (
    st.session_state.y < top_pipe_h or st.session_state.y > bottom_pipe_y
):
    st.session_state.game_over = True

# colisão no teto/chão
if st.session_state.y < 0 or st.session_state.y > HEIGHT:
    st.session_state.game_over = True

# ---------------- UI ----------------
st.title("🐦 Flappy Bird")
st.markdown("### 🏆 Pontuação: **{}**".format(st.session_state.score))

# Render SVG dentro de iframe (forma correta)
html = """
<div style="display:flex; justify-content:center;">
  <svg width="{w}" height="{h}" style="background:#87CEEB; border-radius:10px;">
    <circle cx="{bx}" cy="{by}" r="{br}" fill="yellow"></circle>
    <rect x="{px}" y="0" width="{pw}" height="{th}" fill="green"></rect>
    <rect x="{px}" y="{by2}" width="{pw}" height="{h}" fill="green"></rect>
  </svg>
</div>
""".format(
    w=WIDTH,
    h=HEIGHT,
    bx=BIRD_X,
    by=st.session_state.y,
    br=BIRD_R,
    px=st.session_state.pipe_x,
    pw=PIPE_W,
    th=top_pipe_h,
    by2=bottom_pipe_y,
)

frame = st.empty()
with frame:
    components.html(html, height=HEIGHT + 20)

c1, c2 = st.columns(2)
with c1:
    st.button("⬆️ FLAP", on_click=flap, use_container_width=True)
with c2:
    st.button("🔄 RESET", on_click=reset, use_container_width=True)

if st.session_state.game_over:
    st.error("💥 GAME OVER 💥")
else:
    time.sleep(FPS)
    do_rerun()
``
