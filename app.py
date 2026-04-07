import streamlit as st
import random
import time
import streamlit.components.v1 as components

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Flappy Bird", layout="centered")

# ---------------- RERUN COMPAT (NOVO/ANTIGO) ----------------
def do_rerun():
    # Streamlit novo: st.rerun()
    if hasattr(st, "rerun"):
        st.rerun()
    # Streamlit antigo: st.experimental_rerun()
    else:
        st.experimental_rerun()

# ---------------- SESSION STATE ----------------
if "started" not in st.session_state:
    st.session_state.started = True
    st.session_state.y = 250.0
    st.session_state.velocity = 0.0
    st.session_state.pipe_x = 400.0
    st.session_state.pipe_gap_y = float(random.randint(120, 300))
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.running = True  # permite pausar se quiser

# ---------------- CONSTANTS ----------------
WIDTH = 400
HEIGHT = 500
PIPE_WIDTH = 60
PIPE_GAP = 150
GRAVITY = 1.1
FLAP_STRENGTH = -9.0
PIPE_SPEED = 4.0
FPS = 0.03  # menor = mais rápido (0.02 a 0.05 é bom)

# ---------------- CONTROLS ----------------
def flap():
    if not st.session_state.game_over:
        st.session_state.velocity = FLAP_STRENGTH

def reset():
    st.session_state.y = 250.0
    st.session_state.velocity = 0.0
    st.session_state.pipe_x = 400.0
    st.session_state.pipe_gap_y = float(random.randint(120, 300))
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.running = True

# ---------------- GAME LOOP (1 "tick" por rerun) ----------------
if (not st.session_state.game_over) and st.session_state.running:
    st.session_state.velocity += GRAVITY
    st.session_state.y += st.session_state.velocity
    st.session_state.pipe_x -= PIPE_SPEED

    if st.session_state.pipe_x < -PIPE_WIDTH:
        st.session_state.pipe_x = float(WIDTH)
        st.session_state.pipe_gap_y = float(random.randint(120, 300))
        st.session_state.score += 1

# ---------------- COLLISION ----------------
bird_x = 100
bird_radius = 12

top_pipe_bottom = st.session_state.pipe_gap_y
bottom_pipe_top = st.session_state.pipe_gap_y + PIPE_GAP

# colisão com os canos
if (
    st.session_state.pipe_x < bird_x < st.session_state.pipe_x + PIPE_WIDTH
    and (st.session_state.y < top_pipe_bottom or st.session_state.y > bottom_pipe_top)
):
    st.session_state.game_over = True
    st.session_state.running = False

# colisão chão/teto
if st.session_state.y < 0 or st.session_state.y > HEIGHT:
    st.session_state.game_over = True
    st.session_state.running = False

# ---------------- UI ----------------
st.title("🐦 Flappy Bird")
st.markdown(f"### 🏆 Pontuação: **{st.session_state.score}**")

# Render com SVG (HTML correto no Streamlit)
game_html = f"""
<div style="display:flex; justify-content:center;">
  <svg width="{WIDTH}" height="{HEIGHT}" style="background:#87CEEB; border-radius:10px;">
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

# Use container para reduzir "ghosting" em reruns
view = st.empty()
with view:
    components.html(game_html, height=HEIGHT + 20)

# ---------------- CONTROLS ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.button("⬆️ FLAP", on_click=flap, use_container_width=True)

with col2:
    st.button("🔄 RESET", on_click=reset, use_container_width=True)

with col3:
    # opcional: pausa/continua
    if st.session_state.running:
        if st.button("⏸️ PAUSAR", use_container_width=True):
            st.session_state.running = False
            do_rerun()
    else:
        if (not st.session_state.game_over) and st.button("▶️ CONT.", use_container_width=True):
            st.session_state.running = True
            do_rerun()

if st.session_state.game_over:
    st.error("💥 GAME OVER 💥")
else:
    # auto-rodar o jogo
    time.sleep(FPS)
    do_rerun()
``
